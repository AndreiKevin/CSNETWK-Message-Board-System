import socket
import json
from tabulate import tabulate

class Client:
    def __init__(self, address=socket.gethostbyname(socket.gethostname()), port=20001, bufferSize=1024):
        self.serverAddressPort = (address, port)
        self.bufferSize = bufferSize
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.bind((socket.gethostbyname(socket.gethostname()), 20002))
        

    def join(self, s):
        self.serverAddressPort = (s[1], s[2])
        
        try:
            # Send to server using created UDP socket
            self.send('{"command":"join"}', self.serverAddressPort)
        except:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        
    def leave(self):
        # if not currently connected print error
        try:
            self.send('{"command":"leave"}', self.serverAddressPort)
            self.serverAddressPort = None
        except:
            print("Error: Disconnection failed. Please connect to the server first.")

    def register(self, s):
        s[0][0] = ''
        command = s[0]
        handle = s[1]

        self.send('{"command":command, "handle":handle}', self.serverAddressPort)

    def msgAll(self, s):
        s[0][0] = ''
        command = s[0]
        message = ' '.join(word for word in s[1::])

        self.send('{"command":command, "message":message}', self.serverAddressPort)

    def msgOne(self, s):
        s[0][0] = ''
        command = s[0]
        handle = s[1]
        message = ' '.join(word for word in s[2::])

        self.send('{"command":command, "handle": handle, "message":message}', self.serverAddressPort)
        
    def question(self):
        # Print all description of commands
        commands = [
            ["/join <server_ip_add> <port>", "Connect to the server application"],
            ["/leave", "Disconnect to the server application"],
            ["/register <handle>", "Register a unique handle or alias"],
            ["/all <message>", "Send message to all"],
            ["/msg <handle> <message>", "Send direct message to a single handle"],
            ["/?", "Request command help to output all Input Syntax commands for references"]
        ]
        header = ["Command", "Description"]
        print(tabulate(commands, headers=header))

    def send(self, msg:str, address:tuple):
        bytesToSend = str.encode(json.dumps(msg))
        self.UDPClientSocket.sendto(bytesToSend, address)

    def recieve(self):
        return self.UDPClientSocket.recvfrom(self.bufferSize)

#####################

client = Client()

def parseInput(input):
    s = input.split()
    
    if "/join" in input:
        if not len(s)==3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.join(s)
    elif "/leave" in input:
        if not len(s)==1:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.leave()
    elif "/register" in input:
        if not len(s)==2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.register(s)
    elif "/all" in input:
        if len(s)<2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgAll(s)
    elif "/msg" in input:
        if len(s)<3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgOne(s)
    elif "/?" in input:
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

        bytesAddressPair = client.recieve()
        # Convert recieved inputs
        byteMsg = bytesAddressPair[0]
        byteAddress = bytesAddressPair[1]
        ServerMsgStr = str.decode(json.loads(byteMsg))

        print(ServerMsgStr['message'])


main()