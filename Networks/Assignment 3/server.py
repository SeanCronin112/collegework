import threading
import socket
import argparse
import os
import errno

#Creating the Server class, as a thread.
class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.connections = []
        self.connected_clients = {}
        self.chatroom_dictionary = {}


# The Run Function sets up the socket, and runs as a thread to listen to connections coming in from other sockets. 
# The line (sock.setsockopt(sock.SOL_SOCKET, socket.SO_REUSEADDR, 1) sets the option to reuse address for the sockets to on.)
# Everytime a new socket connects to the server socket, the while loop runs.
    def run(self):
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        main_socket.bind((self.host, self.port))
        main_socket.listen(1)
        print("Listening for connections at {}:{}".format(self.host, self.port))

        while True:
            sock, sockname = main_socket.accept()
            print('{} connected, on port {}'.format(sock.getpeername(), sock.getsockname()))

            server_socket = ServerSocket(sock, sockname, self)
            server_socket.start()

            self.connections.append(server_socket)

            print("Ready to recieve messages from", sock.getpeername())

    #The Broadcast function checks to see if a client is in the right chatroom before sending the message.]
    # The connected_clients dictionary pairs socket host/port tuple to a username.
    # The chatroom_dictionary pairs usernames to their respective chatrooms.

    def broadcast(self, message, source, chatroom):
        for connection in self.connected_clients.keys():
            if connection.sockname != source.sockname:    
                username = server.connected_clients[connection]
                if chatroom == server.chatroom_dictionary[username]:
                    connection.send(message)
    
    def remove_connection(self, connection):
        if connection in self.connected_clients:
            del self.connected_clients[connection]


    def help(self):
        print("exit: Exits the server.")
        print("connections: lists connected clients by username")
        print("chatrooms: Shows what chatroom everybody is in")

    #A function called in the server_commands thread to close the server down.
    def exit_server(self):
        print("Closing all connections.")
        for connection in self.connected_clients.keys():
            connection.sock.close()
        print("Shutting down the server.")
        os._exit(0)

    # A function called by the server commands thread which lists all the current connected users.
    def list_connections(self):
        print("Connections: ")
        if server.connected_clients:
            for client_name in server.connected_clients.values():
                print("    " + client_name)
        else:    
            print("No connections.")

    # A Function called by the server commands thread, to list what chatrooms each user is in.
    def list_chatrooms(self):
        for username in self.chatroom_dictionary:
            print("{} is on chatroom {}".format(username, self.chatroom_dictionary[username]))

class ServerSocket(threading.Thread):

    def __init__(self, sock, sockname, server):
        super().__init__()
        self.sock = sock
        self.sockname = sockname
        self.server = server

    def run(self):
        try:
            while True:
                #Receiving initial message from the socket, and splitting it to determine both user and chatroom.
                message = self.sock.recv(1024).decode('utf-8')
                message_split = message.split()
                client_username = message_split[0]

                #Adding the user to the chatroom dictionary if not already in it. The chatroom variable is in this if statement because 
                #Otherwise, it would have the chatroom_choice as the last word of each message, making loads of chatrooms.
                if client_username not in server.chatroom_dictionary:
                    chatroom_choice = message_split[-1][0]
                    server.chatroom_dictionary[client_username] = chatroom_choice

                #If the users chatroom is already in the dictionary, the chatroom_choice variable is set to be its appropriate value.
                else:
                    chatroom_choice = server.chatroom_dictionary[client_username]

                #If the user is not in the connected_clients dictionary, it adds the user in.
                if self not in server.connected_clients:
                    server.connected_clients[self] = message_split[0]
                
                #Prints the message server side, prefixing .
                print('{}'.format(message))
                self.server.broadcast(message, self, chatroom_choice)
        
        #Handles any OS Errors.
        except OSError:
            print('{} has closed the connection'.format(self.sockname))
            self.sock.close()
            server.remove_connection(self)

    #Sends the encoded message.
    def send(self, message):
        self.sock.sendall(message.encode('utf-8'))


#The extra that I added. It allows you to exit the server, view connections and view respective chatrooms.
def server_commands(server):
    while True:
        server_input = input("Server: ")
        if server_input == "exit":
            server.exit_server()
        elif server_input == "connections":
            server.list_connections()
        elif server_input == "chatrooms":
            server.list_chatrooms()
        elif server_input == "help":
            server.help()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', type=str, default="0.0.0.0", help='Interface the server listens at')
    parser.add_argument('port', type=int, default=8080, help='TCP port (default 8080)')
    args = parser.parse_args()

    #Creates a thread of the server.
    server = Server(args.host, args.port)
    server.start()

    #Creates and starts a thread of the server commands.
    server_commands = threading.Thread(target = server_commands, args = (server,))
    server_commands.start()