import unittest
import ip_calculator

#Testing the individual helper functions as oppose to testing the three main program functions. I'm doing this because the final strings are outputting a string containing all the values, 

# In many cases, it might seem irrelavent to check anything other then the assertEquals, but I think it's a good practice to get into to add at least a bit of variation.
class Test_ip_calculator(unittest.TestCase):

#----------------Testing-functions-for-determining-aspects-of-the-ip-address-----------------------#

    def test_determine_network_class(self):
        self.assertEqual(ip_calculator.determine_network_class("136.206.20.0"), "B")
        self.assertEqual(ip_calculator.determine_network_class("192.168.10.0"), "C")
        self.assertEqual(ip_calculator.determine_network_class("16.192.100.32"), "A")
        self.assertEqual(ip_calculator.determine_network_class("224.100.236.2"), "D")
        self.assertEqual(ip_calculator.determine_network_class("255.0.0.0"), "E")
        self.assertNotEqual(ip_calculator.determine_network_class("192.168.100.2"), "B")
        self.assertNotEqual(ip_calculator.determine_network_class("136.206.100.2"), "C")

    def test_determine_network(self):
        self.assertEqual(ip_calculator.determine_network("A"), 128)
        self.assertEqual(ip_calculator.determine_network("B"), 16384)
        self.assertEqual(ip_calculator.determine_network("C"), 65536)
        self.assertEqual(ip_calculator.determine_network("D"), "N/A")
        self.assertEqual(ip_calculator.determine_network("E"), "N/A")
        self.assertNotEqual(ip_calculator.determine_network("B"), 65536)
        self.assertNotEqual(ip_calculator.determine_network("C"), 16384)


    def test_determine_host(self):
        self.assertEqual(ip_calculator.determine_host("A"), 16777216)
        self.assertEqual(ip_calculator.determine_host("B"), 65536)
        self.assertEqual(ip_calculator.determine_host("C"), 256)
        self.assertEqual(ip_calculator.determine_host("D"), "N/A")
        self.assertEqual(ip_calculator.determine_host("E"), "N/A")
        self.assertNotEqual(ip_calculator.determine_host("B"), 256)
        self.assertNotEqual(ip_calculator.determine_host("C"), 65536)

    def test_determine_first_address(self):
        self.assertEqual(ip_calculator.determine_first_address("A"), "0.0.0.0")
        self.assertEqual(ip_calculator.determine_first_address("B"), "128.0.0.0")
        self.assertEqual(ip_calculator.determine_first_address("C"), "192.0.0.0")
        self.assertEqual(ip_calculator.determine_first_address("D"), "224.0.0.0")
        self.assertEqual(ip_calculator.determine_first_address("E"), "240.0.0.0")
        self.assertNotEqual(ip_calculator.determine_first_address("B"), "0.0.0.0")
        self.assertNotEqual(ip_calculator.determine_first_address("C"), "128.0.0.0")

    def test_determine_last_address(self):
        self.assertEqual(ip_calculator.determine_last_address("A"), "127.255.255.255")
        self.assertEqual(ip_calculator.determine_last_address("B"), "191.255.255.255")
        self.assertEqual(ip_calculator.determine_last_address("C"), "223.255.255.255")
        self.assertEqual(ip_calculator.determine_last_address("D"), "239.255.255.255")
        self.assertEqual(ip_calculator.determine_last_address("E"), "255.255.255.255")
    
#-------------Testing-functions-for-determining-Subnet-Stats-------------------------------------------------#

    def test_determine_subnet_index(self):
        self.assertEqual(ip_calculator.determine_subnet_index("255.255.255.192"), 3)
        self.assertEqual(ip_calculator.determine_subnet_index("255.255.192.0"), 2)
        self.assertNotEqual(ip_calculator.determine_subnet_index("255.255.255.192"), 2)
        self.assertNotEqual(ip_calculator.determine_subnet_index("255.255.192.0"), 3)

    def test_determine_cidr(self):
        self.assertEqual(ip_calculator.determine_cidr("255.255.255.192"), 26)
        self.assertEqual(ip_calculator.determine_cidr("255.255.192.0"), 18)
        self.assertEqual(ip_calculator.determine_cidr("255.255.255.192"), 26)
        self.assertNotEqual(ip_calculator.determine_cidr("255.255.255.192"), 18)
        self.assertNotEqual(ip_calculator.determine_cidr("255.255.192.0"), 26)

    def test_determine_subnets(self):
        self.assertEqual(ip_calculator.determine_subnets("255.255.255.192", 3), 4)
        self.assertEqual(ip_calculator.determine_subnets("255.255.192.0", 2), 4) 
        self.assertNotEqual(ip_calculator.determine_subnets("255.255.255.192", 3), 2)
        self.assertNotEqual(ip_calculator.determine_subnets("255.255.192.0", 2), 2)

    def test_determine_valid_subnets(self):
        self.assertEqual(ip_calculator.determine_valid_subnets("192.168.10.0", 64, 3), ["192.168.10.0", "192.168.10.64", "192.168.10.128", "192.168.10.192"])
        self.assertEqual(ip_calculator.determine_valid_subnets("172.16.0.0", 64, 2), ["172.16.0.0", "172.16.64.0", "172.16.128.0", "172.16.192.0"])
        self.assertNotEqual(ip_calculator.determine_valid_subnets("192.168.10.0", 64, 2), ["192.168.10.0", "192.168.10.64", "192.168.10.128", "192.168.10.192"])
        self.assertNotEqual(ip_calculator.determine_valid_subnets("172.16.0.0", 64, 3), ["172.16.0.0", "172.16.64.0", "172.16.128.0", "172.16.192.0"])

    def test_determine_broadcast_addresses(self):
        self.assertEqual(ip_calculator.determine_broadcast_addresses(["192.168.10.0", "192.168.10.64", "192.168.10.128", "192.168.10.192"], 64, 3), ["192.168.10.63", "192.168.10.127", "192.168.10.191", "192.168.10.255"])
        self.assertEqual(ip_calculator.determine_broadcast_addresses(["172.16.0.0", "172.16.64.0", "172.16.128.0", "172.16.192.0"], 64, 2), ["172.16.63.255", "172.16.127.255", "172.16.191.255", "172.16.255.255"])
        self.assertNotEqual(ip_calculator.determine_broadcast_addresses(["192.168.10.0", "192.168.10.64", "192.168.10.128", "192.168.10.192"], 64, 3), ["192.168.63.0", "192.168.127.0", "192.168.191.0", "192.168.255.0"])
        self.assertNotEqual(ip_calculator.determine_broadcast_addresses(["172.16.0.0", "172.16.64.0", "172.16.128.0", "172.168.0.0"], 64, 2), ["172.16.0.255", "172.16.64.255", "172.16.128.255", "172.16.192.255"])

    
    def test_determine_first_subnet_addresses(self):
        self.assertEqual(ip_calculator.determine_first_subnet_addresses(["192.168.10.0", "192.168.10.64", "192.168.10.128", "192.168.10.192"]), ["192.168.10.1","192.168.10.65","192.168.10.129","192.168.10.193"])
        self.assertEqual(ip_calculator.determine_first_subnet_addresses(["172.16.0.0", "172.16.64.0", "172.16.128.0", "172.16.192.0"]),  ["172.16.0.1","172.16.64.1","172.16.128.1","172.16.192.1"])
        self.assertNotEqual(ip_calculator.determine_first_subnet_addresses(["192.168.10.0", "192.168.10.64", "192.168.10.128", "192.168.10.192"]), ["192.168.10.1", "192.168.10.2""192.168.10.65","192.168.10.129","192.168.10.193"])
        self.assertNotEqual(ip_calculator.determine_first_subnet_addresses(["172.16.0.0", "172.16.64.0", "172.16.128.0", "172.16.192.0"]),  ["172.16.0.1", "172.16.0.2""172.16.64.1","172.16.128.1","172.16.192.1"])

    def test_determine_last_subnet_addresses(self):
        self.assertEqual(ip_calculator.determine_last_subnet_addresses(["192.168.10.63","192.168.10.127","192.168.10.191","192.168.10.255"]), ["192.168.10.62","192.168.10.126","192.168.10.190","192.168.10.254"])
        self.assertEqual(ip_calculator.determine_last_subnet_addresses(["172.16.63.255","172.16.127.255","172.16.191.255","172.16.255.255"]), ["172.16.63.254","172.16.127.254","172.16.191.254","172.16.255.254"])
        self.assertNotEqual(ip_calculator.determine_last_subnet_addresses(["192.168.10.62","192.168.10.127","192.168.10.191","192.168.10.255"]), ["192.168.10.62","192.168.10.126","192.168.10.190","192.168.10.254"])
        self.assertNotEqual(ip_calculator.determine_last_subnet_addresses(["172.16.63.254","172.16.127.255","172.16.191.255","172.16.255.255"]), ["172.16.63.254","172.16.127.254","172.16.191.254","172.16.255.254"])

#---------------------Testing-The-SuperNetting-Functions--------------------------------------------------#

    def test_determine_supernet_cidr(self):
        self.assertEqual(ip_calculator.determine_supernet_cidr(["205.100.0.0", "205.100.1.0", "205.100.2.0", "205.100.3.0"]), 22)
        self.assertEqual(ip_calculator.determine_supernet_cidr(["205.106.2.0", "205.106.3.0", "205.106.4.0"]), 21)
        self.assertNotEqual(ip_calculator.determine_supernet_cidr(["205.100.0.0", "205.100.1.0", "205.100.2.0", "205.100.3.0"]), 21)
        self.assertNotEqual(ip_calculator.determine_supernet_cidr(["205.106.2.0", "205.106.3.0", "205.106.4.0"]), 22)

    def test_determine_supernet_mask(self):
        self.assertEqual(ip_calculator.determine_supernet_network_mask(22), "255.255.252.0")
        self.assertEqual(ip_calculator.determine_supernet_network_mask(21), "255.255.248.0")
        self.assertNotEqual(ip_calculator.determine_supernet_network_mask(22), "255.255.248.0")
        self.assertNotEqual(ip_calculator.determine_supernet_network_mask(21), "255.255.252.0")

if __name__ == "__main__":
    unittest.main()