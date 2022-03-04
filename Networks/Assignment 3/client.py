import threading
import socket
import argparse
import os
import sys
import errno
import tkinter as tk

class Send(threading.Thread):
    def __init__(self, client_socket, username):
        super().__init__()
        self.socket = client_socket
        self.name = username

    #This function is constantly running when the user sets up the server to allow the user to enter input at any time, 
    #Without interfering with recieving messages, as they are being taken in on another thread.

    def run(self):
        while True:

            message = "{} : {}".format(self.name, input())

            if message == "{} : !!".format(self.name):
                self.socket.sendall("{} has left the chat. Goodbye!".format(self.name).encode('utf-8'))
                break
        
            else:
                self.socket.sendall('{}'.format(message).encode('utf-8'))

        #Once the loop breaks (when !! is inputted), the loop breaks and the whole program is shut down.

        print("Leaving the Server!")
        self.socket.close()
        os._exit()

class Recieve(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    #This will run as long as the connection is active, allowing the client to recieve messages.
    def run(self):
        while True:
            message = self.sock.recv(1024).decode("utf-8")

            if message:
                if self.messages:
                    self.messages.insert(tk.END, message)
                    print("{}".format(message))

            else:
                print("You have lost connection from the server. Run the program again to retry.")
                self.sock.close()
                os._exit(0)

class Client:
    def __init__(self, host, port, name, chatroom):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.name = name
        self.chatroom = chatroom
        

    #Starts by connecting to the serversocke
    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            print("You have successfully joined the server.")
        except:
            print("You were unable to connect to the server. Please try again.")
        
        #Starting the Send and Recieve Threads.
        send = Send(self.socket, self.name)
        recieve = Recieve(self.socket, self.name)

        send.start()
        recieve.start()


        #Broadcasts to everyone that the user has entered the chatroom.
        self.socket.sendall("{} has joined the chat on chatroom {}".format(self.name, self.chatroom).encode('utf-8'))

        return recieve


    #Sends out the messages, taken from the tkinter window. Quits the program if !! is entered.
    def send(self, text_input):
        message = '{} : {}'.format(self.name, text_input.get())
        text_input.delete(0, tk.END)
        self.messages.insert(tk.END, "{} : {}".format(self.name, message).encode('utf-8'))

        if message == "!!".format(self.name):
            self.socket.sendall("Server: {} has left the chat.".format(self.name).encode('utf-8'))
            self.socket.close()
            os._exit(0)
        
        else:
            self.socket.sendall('{}'.format(message).encode('utf-8'))

def main(host, port, name, chatroom):
    """
    Initializes and runs the GUI application.
    Args:
        host (str): The IP address of the server's listening socket.
        port (int): The port number of the server's listening socket.
    """
    client = Client(host, port, name, chatroom)
    receive = client.start()

    
    window = tk.Tk()
    window.title('Chatroom: {}'.format(chatroom))

    frm_messages = tk.Frame(master=window)
    scrollbar = tk.Scrollbar(master=frm_messages)
    messages = tk.Listbox(
        master=frm_messages, 
        yscrollcommand=scrollbar.set
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    client.messages = messages
    receive.messages = messages

    frm_messages.grid(row=0, column=0, columnspan=2, sticky="nsew")

    frm_entry = tk.Frame(master=window)
    text_input = tk.Entry(master=frm_entry)
    text_input.pack(fill=tk.BOTH, expand=True)
    text_input.bind("<Return>", lambda x: client.send(text_input))
    text_input.insert(0, "Enter Message: ")

    btn_send = tk.Button(
        master=window,
        text='Send',
        command=lambda: client.send(text_input)
    )

    frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.mainloop()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('name', metavar = 'NAME', type=str, help='Enter your name' )
    parser.add_argument('host', metavar = 'HOST', default = "127.0.0.1", help='Interface the server listens at')
    parser.add_argument('port', metavar='PORT', type=int, default=8080, help='TCP port (default 1060)')
    parser.add_argument('chatroom', metavar = 'CHATROOM', default = 1, help = "Enter the chatroom you would like to join.")
    
    args = parser.parse_args()

    main(args.host, args.port, args.name, args.chatroom)