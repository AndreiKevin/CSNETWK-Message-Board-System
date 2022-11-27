import socket
import json
from tabulate import tabulate
import threading

class Client:
    def __init__(self, bufferSize=1024):
        self.connected = False
        self.listener = threading.Thread(target=self.listen)
        self.serverAddressPort = None
        self.bufferSize = bufferSize
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def listen(self):
        while True:
            bytesAddressPair = client.recieve()
            # Convert recieved inputs
            byteMsg = bytesAddressPair[0]
            ServerMsgStr = json.loads(byteMsg.decode())

            print("From Server:", ServerMsgStr['message'])
            
            if not self.connected:
                break

    def join(self, s):
        if self.connected == False:
            self.serverAddressPort = (s[1], s[2])

            self.send(str({"command":"join"}), self.serverAddressPort)
            self.connected = True
            self.listener.start()

            try:
                # Send to server using created UDP socket
                print()    
            except:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        else:
            print("Currently Connected. Please do /leave first.")

    def leave(self):
        # if not currently connected print error
        try:
            self.send(str({"command":"leave"}), self.serverAddressPort)
            self.serverAddressPort = None
            self.connected = False
            self.listener.join()
            print("Disconnected from Server...")

        except:
            print("Error: Disconnection failed. Please connect to the server first.")

    def register(self, s):
        if self.connected:
            s[0][0] = ''
            command = s[0]
            handle = s[1]

            self.send(str({"command":command, "handle":handle}), self.serverAddressPort)
        else:
            print("Error: Not Connected to a server!")

    def msgAll(self, s):
        if self.connected:
            s[0][0] = ''
            command = s[0]
            message = ' '.join(word for word in s[1::])
            self.send(str({"command":command, "message":message}), self.serverAddressPort)
        else:
            print("Error: Not Connected to a server!")


    def msgOne(self, s):
        if self.connected:
            s[0][0] = ''
            command = s[0]
            handle = s[1]
            message = ' '.join(word for word in s[2::])

            self.send(str({"command":command, "handle": handle, "message":message}), self.serverAddressPort)
        else:
            print("Error: Not Connected to a server!")

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
        print(bytesToSend, address)
        self.UDPClientSocket.sendto(bytesToSend, (str(address[0]), int(address[1])))

    def recieve(self):
        return self.UDPClientSocket.recvfrom(self.bufferSize)

#####################

client = Client()

def parseInput(input):
    s = input.split()
    
    if "/join" in s:
        if not len(s)==3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.join(s)
    elif "/leave" in s:
        if not len(s)==1:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.leave()
    elif "/register" in s:
        if not len(s)==2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.register(s)
    elif "/all" in s:
        if len(s)<2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgAll(s)
    elif "/msg" in s:
        if len(s)<3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgOne(s)
    elif "/?" in s:
        if not len(s)==1:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.question()
    else:
        print("Error: Command not found")

def clientProgram():
    while True:
        parseInput(input())

def main():
    print("Client Started...")
    program = threading.Thread(target=clientProgram)

    program.start()


main()