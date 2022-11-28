import socket
import json
from tabulate import tabulate
import threading
import ast

class BaseThread(threading.Thread):
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

    def target_with_callback(self):
        self.method()
        if self.callback is not None:
            if self.callback_args is not None:
                self.callback(*self.callback_args)
            else:
                self.callback()

class Client:
    def __init__(self, bufferSize=1024):
        self.connected = False
        self.listener = BaseThread(target=self.listen, callback=self.resetConnection)
        self.serverAddressPort = None
        self.bufferSize = bufferSize
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def listen(self):
        while True:
            # Attempt to listen. Sometimes an error occurs even if already connected. 
            try:
                bytesAddressPair = client.recieve()
                # Convert recieved inputs
                byteMsg = bytesAddressPair[0]
                ServerMsgDict = ast.literal_eval(json.loads(byteMsg.decode()))

                print(ServerMsgDict["message"])
                
                if not self.connected:
                    print("[Client]: Disconnected from Server...")
                    break
            except:
                print("Recieve Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                break

    def join(self, s):
        if self.connected == False:
            self.serverAddressPort = (s[1], s[2])
            
            try:
                # Send to server using created UDP socket
                self.send({"command":"join"}, self.serverAddressPort)
                self.connected = True
                self.listener.start()
            except:
                self.connected = False
                print("Join Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        else:
            print("Currently Connected. Please do /leave first.")

    def resetConnection(self):
        self.serverAddressPort = None
        self.connected = False
        # A thread can only be run once so assign a new one
        self.listener = BaseThread(target=self.listen, callback=self.resetConnection)

    def leave(self):
        # if not currently connected print error
        if self.connected:
            self.send({"command":"leave"}, self.serverAddressPort)
            self.connected = False
        else:
            print("Error: Disconnection failed. Please connect to a server first.")

    def register(self, s):
        if self.connected:
            s[0] = s[0].replace('/', '')
            command = s[0]
            handle = s[1]

            self.send({"command":command, "handle":handle}, self.serverAddressPort)
        else:
            print("Error: Not Connected to a server!")

    def msgAll(self, s):
        if self.connected:
            s[0] = s[0].replace('/', '')
            command = s[0]
            message = ' '.join(word for word in s[1::])
            self.send({"command":command, "message":message}, self.serverAddressPort)
        else:
            print("Error: Not Connected to a server!")

    def msgOne(self, s):
        if self.connected:
            s[0] = s[0].replace('/', '')
            command = s[0]
            handle = s[1]
            message = ' '.join(word for word in s[2::])

            self.send({"command":command, "handle": handle, "message":message}, self.serverAddressPort)
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
        bytesToSend = str.encode(json.dumps(str(msg)))
        self.UDPClientSocket.sendto(bytesToSend, (str(address[0]), int(address[1])))

    def recieve(self):
        return self.UDPClientSocket.recvfrom(self.bufferSize)

#####################

client = Client()

def parseInput(input):
    s = input.split()
    
    if "/join" in s[0]:
        if not len(s)==3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.join(s)
    elif "/leave" in s[0]:
        if not len(s)==1:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.leave()
    elif "/register" in s[0]:
        if not len(s)==2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.register(s)
    elif "/all" in s[0]:
        if len(s)<2:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgAll(s)
    elif "/msg" in s[0]:
        if len(s)<3:
            print("Error: Command parameters do not match or is not allowed.")
        else:
            client.msgOne(s)
    elif "/?" in s[0]:
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