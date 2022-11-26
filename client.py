import socket
import json
from tabulate import tabulate

class Client:
    def __init__(self, serverAddress, serverPort, bufferSize=1024):
        self.serverAddressPort = (serverAddress, serverPort)
        self.bufferSize = bufferSize
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def join(self, serverAddress, serverPort):
        self.serverAddressPort = (serverAddress, serverPort)
        
        msgjson = 
        bytesToSend = str.encode(msgjson)
        try:
            # Send to server using created UDP socket
            self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
        except:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        
    def leave(self):
        # if not currently connected raise error
        if self.serverAddressPort == None:
            print("Error: Disconnection failed. Please connect to the server first.")
        else:
            self.serverAddressPort = None

    def register(self):
        status = 

    def msgAll(self, msg):
        pass

    def msgOne(self, msg, handle):
        # server only accepts json
        msgjson = 
        bytesToSend = str.encode(msgjson)
        # Send to server using created UDP socket
        self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
        
    def question(self):
        # Print all description of commands
        commands = [
            ["/join <server_ip_add> <port>", "Connect to the server application"]
            ["/leave", "Disconnect to the server application"]
            ["/register <handle>", "Register a unique handle or alias"]
            ["/all <message>", "Send message to all"]
            ["/msg <handle> <message>", "Send direct message to a single handle "]
            ["/?", "Request command help to output all Input Syntax commands for references"]
        ]
        header = ["Command", "Description"]
        print(tabulate(commands, headers=header))


client = Client()

def parseInput(input):
    s = input.split()
    
    if "/join" in input:
        if not len(s)==3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.join()
    elif "/leave" in input:
        if not len(s)==1:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.leave()
    elif "/register" in input:
        if not len(s)==2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.register()
    elif "/all" in input:
        if len(s)<2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgAll()
    elif "/msg" in input:
        if len(s)<3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgOne()
    elif "/question" in input:
        if not len(s)==1:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.question()
    else:
        print("Error: Command not found")

def main():
    # take input
    while True:
        parseInput(input())
        msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])
        print("Server IP:", msgFromServer[1])
        print(msg)