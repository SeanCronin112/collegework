#-----------------------initial-Helper-Functions--------------------------------------#
def to_binary_string(ip_addr):
    byte_split = ip_addr.split(".")                                                                          
    return ['{0:08b}'.format(int(x)) for x in byte_split]

def to_decimal_dot(ip_addr_list):
    return ".".join([str(int(x,2)) for x in ip_addr_list])

#--------------------Functions-for-determining-aspects-of-the-IP-Address--------------#

def determine_network_class(ip_addr):

    prefix = (to_binary_string(ip_addr))[0][:4]                                                                         # Creating a Prefix Variable, which is the first 4 binary digits of the IP address. 
    
    if prefix[0:1] == "0":                                                                                              # This series of if statements will return the correct network class.
        return "A"
    elif prefix[0:2] == "10":
        return "B"
    elif prefix[0:3] == "110":
        return "C"
    elif prefix[0:4] == "1110":
        return "D"
    else:
        return "E"

def determine_network(network_class):

    network_dictionary = {
        "A": 128,
        "B": 16384,
        "C": 65536,
        "D": "N/A",
        "E": "N/A"
    } 

    return network_dictionary[network_class]                                                                              

def determine_host(network_class):

    host_dictionary = {
        "A": 16777216,
        "B": 65536,
        "C": 256,
        "D": "N/A",
        "E": "N/A"
    }
    
    return host_dictionary[network_class]

def determine_first_address(network_class):

    first_address_dictionary= {
        "A": "0.0.0.0",
        "B": "128.0.0.0",
        "C": "192.0.0.0",
        "D": "224.0.0.0",
        "E": "240.0.0.0"
    }

    return first_address_dictionary[network_class]

def determine_last_address(network_class):

    last_address_dictionary = {
        "A": "127.255.255.255",
        "B": "191.255.255.255",
        "C": "223.255.255.255",
        "D": "239.255.255.255",
        "E": "255.255.255.255"
    }

    return last_address_dictionary[network_class]

#--------------------Functions-for-Determining-Subnet-Stats---------------------------#

def determine_subnet_index(subnet_mask):
    
    #This function takes an IP address as an argument, and calculates the Network Class for that IP.
    #It then retuns an index of the last bit of the subnet mask that isn't equal to 0. The index is then used furtherer on in the programs, to distinguish the subnet from class B and C.
    
    ip_address_list = subnet_mask.split(".")
    counter = 0

    while ip_address_list[counter] == "255":
        counter += 1

    return counter


def determine_cidr(subnet_mask):

    

    li = to_binary_string(subnet_mask)
    binary_string = "".join(li)[::-1] 

    counter = 1

    while int(binary_string[counter]) != 1 and counter < len(binary_string) - 1:
        counter += 1

    return len(binary_string) - counter

def determine_subnets(subnet_mask, index):

    host_bits = to_binary_string(subnet_mask)[index]
    counter = 0
    while (counter < len(host_bits) and host_bits[counter] == "1"):
        counter += 1
    return 2 ** counter

def determine_addressable_hosts_per_subnet(cidr_number):  

    return 2 ** (32 - cidr_number) - 2

def determine_subnet_block_size(index, subnet_mask):

    return 256 - int((subnet_mask).split(".")[index])

def determine_valid_subnets(ip_addr, block_size, index):

    ip_sample = ip_addr.split(".")[:(index - 4)]                                                   
    ip_sample = ".".join(ip_sample) + "."                                                           
                                                                                                   
    counter = 0
    valid_subnets = []

    while(counter < 256):                                                                            
        subnet_string = ip_sample + str(counter)                                                    
        if index == 2:
            subnet_string += ".0"
        valid_subnets.append(subnet_string)

        counter += block_size

    return valid_subnets
    
def determine_broadcast_addresses(valid_subnets, block_size, index):
    
    broadcast_addresses = []                                                                       
    i = 1
    for subnet in valid_subnets:
        subnet_list = subnet.split(".")                                                            
        if index == 3:                                                                              
            subnet_list[3] = str(int(subnet_list[3]) + (block_size - 1))                           
        
        elif index == 2:                                                                           
            subnet_list[2] = str(((block_size * i) - 1))                                
            subnet_list[3] = "255"
        broadcast_addresses.append(".".join(subnet_list))
        i += 1
    return broadcast_addresses
    
def determine_first_subnet_addresses (valid_subnets):

    first_addresses = []
    for subnet in valid_subnets:                                                                   
        subnet_list = subnet.split(".")                                                           
        subnet_list[3] = str(int(subnet_list[3]) + 1)                                             
        first_addresses.append(".".join(subnet_list))                                              

        
    return first_addresses

def determine_last_subnet_addresses(broadcast_addresses):



    last_addresses = []                                                                            
    for subnet in broadcast_addresses:                                                             
        subnet_list = subnet.split(".")                                                            
        subnet_list[3] = str(int(subnet_list[3]) - 1)                                            
        last_addresses.append(".".join(subnet_list))                                             
    
    return last_addresses

#--------------Functions-For-Determining-Supernet-Stats-------------------------------#

def determine_supernet_cidr(ip_addresses):

    list_binary_ips = []                                                                        

    for ip in ip_addresses:                                                                        
        binary_ip = to_binary_string(ip)
        list_binary_ips.append("".join(binary_ip))

    i = 0                                                                                         
    flag = False                                                                                   
    while i < 32:                                                                                  
        binary_index = list_binary_ips[0][i]                                                       
        if flag == True:                                                                           
            break
        j = 0
        while j <= len(list_binary_ips) - 1:
            if(list_binary_ips[j][i] == binary_index):
                pass
            else:
                flag = True
                i -= 1
            j += 1
        i += 1

    return i                                                                                      

def determine_supernet_network_mask(supernet_cidr_number):


    binary_string = ""
    i = 0
    while i < 32:
        if i < int(supernet_cidr_number):
            binary_string += "1"
        else:
            binary_string += ("0")
        if (i + 1) % 8 == 0:
            binary_string += "."
        i += 1
    
    binary_list = binary_string[:-1].split(".")
    return to_decimal_dot(binary_list)

#-------------------------Get-Class-Stats---------------------------------------------#

# The three required functions output a string, which is formed by different values of a dictionary. I made this decision for two reasons, firstly it made testing a lot easier because I could add
# or remove items as needed. Secondly, if I wanted to add another function, I could easily add it in wherever I wanted, as oppose to having to find the right spot if I was to do it through string
# formatting.

def get_class_stats(ip_addr):

    network_class = determine_network_class(ip_addr)

    network = determine_network(network_class)

    host = determine_host(network_class)

    first_address = determine_first_address(network_class)

    last_address = determine_last_address(network_class)

    final_class_values_dictionary = {
        
        "Class: ": network_class,
        "Network: ": network,
        "Host: ": host,
        "First Address: ": first_address,
        "Last Address: ": last_address
    }

    final_string = "Class information for IP address: {}\n".format(ip_addr)

    for element in final_class_values_dictionary:
        final_string += ("{} {}\n".format(element, final_class_values_dictionary[element]))
  
    return final_string

def get_subnet_stats(ip_addr, subnet_mask):

    index = determine_subnet_index(subnet_mask)

    block_size = determine_subnet_block_size(index, subnet_mask)

    cidr_number = determine_cidr(subnet_mask)

    subnets = determine_subnets(subnet_mask, index)

    addressable_hosts_per_subnet = determine_addressable_hosts_per_subnet(cidr_number)

    valid_subnets = determine_valid_subnets(ip_addr, block_size, index)

    broadcast_addresses = determine_broadcast_addresses(valid_subnets, block_size, index)

    first_addresses = determine_first_subnet_addresses(valid_subnets)

    last_addresses = determine_last_subnet_addresses(broadcast_addresses)

    final_subnet_values_dictionary = {
        "Address:": "{}/{}".format(ip_addr, cidr_number),
        "Subnets:": subnets,
        "Addressable hosts per subnet:": addressable_hosts_per_subnet,
        "Valid subnets:": valid_subnets,
        "Broadcast Addresses: ": broadcast_addresses,
        "First Addresses: ": first_addresses,
        "Last Addresses: ": last_addresses
    }

    final_string = ""

    for element in final_subnet_values_dictionary:
        final_string += "{} {}\n".format(element, final_subnet_values_dictionary[element])

    return final_string

def get_supernet_stats(ip_addresses):

    supernet_cidr_number = determine_supernet_cidr(ip_addresses)

    supernet_network_mask = determine_supernet_network_mask(supernet_cidr_number)
    
    final_supernetting_values_dictionary = {
        "Address:": "{}/{}".format(ip_addresses[0], supernet_cidr_number),
        "Network Mask:": supernet_network_mask
    }

    final_string = ""

    for element in final_supernetting_values_dictionary:
        final_string += ("{} {}\n".format(element, final_supernetting_values_dictionary[element]))

    return final_string

def main():

    # Main Program running with predefined class

    #ip_addr = "192.168.10.0"
    #ip_addr = "172.16.0.0"
    #subnet_mask = "255.225.255.192"
    #subnet_mask = "255.255.192.0"
    #ip_addresses = ["205.106.2.0", "205.106.3.0", "205.106.4.0"]
    #binary_list = to_binary_string(ip_addr)
    
    #print(get_class_stats(ip_addr))
    #print(get_subnet_stats(ip_addr, subnet_mask))
    #print(get_supernet_stats(ip_addresses))

    # Main Program which asks users for inputs

    program_chosen_by_user = input("Welcome to the IP Calculator! Would you like to determine:\n1. Class Stats.\n2. Subnet Stats\n3. Supernet Stats.\nPlease enter 1, 2 or 3.\n")
    while program_chosen_by_user not in "123":
        program_chosen_by_user = input("You didn't enter a valid number. Please try again.\n")

    if int(program_chosen_by_user) == 1:
        print()
        ip_addr = input("Please enter the IP address for which you'd like to find the class information.\n")
        print()
        print(get_class_stats(ip_addr))

    elif int(program_chosen_by_user) == 2:
        print()
        ip_addr = input("Please enter the IP address for the subnet stats about it.\n")
        print()
        subnet_mask = input("Please enter the subnet mask.\n")
        print()
        print(get_subnet_stats(ip_addr, subnet_mask))

    elif int(program_chosen_by_user) == 3:
        print()
        ip_addr = input("Please enter, seperated by a comma and a space, the list of IP addresses to be supernetted. Example: 205.106.2.0, 205.106.3.0, 205.106.4.0\n")
        print(get_supernet_stats(ip_addr.split(", ")))
    
    else:
        program_chosen_by_user = input("You did not enter a valid number. Please try again.\n")

if __name__ == "__main__":
    main()

