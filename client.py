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
        self.output = []
        self.event = threading.Event()

    def listen(self):
        while True:
            # Attempt to listen. Sometimes an error occurs even if already connected. 
            try:
                bytesAddressPair = self.recieve()
                # Convert recieved inputs
                byteMsg = bytesAddressPair[0]
                ServerMsgDict = ast.literal_eval(json.loads(byteMsg.decode()))

                self.output.append(ServerMsgDict["message"])
                print(ServerMsgDict["message"])
                self.event.set()
                
                if not self.connected:
                    self.output.append("[Client]: Disconnected from Server...")
                    self.event.set()
                    break
            except:
                self.output.append("Recieve Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                self.event.set()
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
                self.output.append("Join Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                self.event.set()
        else:
            self.output.append("Currently Connected. Please do /leave first.")
            self.event.set()

    def resetConnection(self):
        # A thread can only be run once so assign a new one
        self.listener = BaseThread(target=self.listen, callback=self.resetConnection)
        self.serverAddressPort = None
        self.connected = False

    def leave(self):
        # if not currently connected self.output.append error
        if self.connected:
            self.send({"command":"leave"}, self.serverAddressPort)
            self.connected = False
        else:
            self.output.append("Error: Disconnection failed. Please connect to a server first.")
            self.event.set()

    def register(self, s):
        if self.connected:
            s[0] = s[0].replace('/', '')
            command = s[0]
            handle = s[1]

            self.send({"command":command, "handle":handle}, self.serverAddressPort)
        else:
            self.output.append("Error: Not Connected to a server!")
            self.event.set()

    def msgAll(self, s):
        if self.connected:
            s[0] = s[0].replace('/', '')
            command = s[0]
            message = ' '.join(word for word in s[1::])
            self.send({"command":command, "message":message}, self.serverAddressPort)
        else:
            self.output.append("Error: Not Connected to a server!")
            self.event.set()

    def msgOne(self, s):
        if self.connected:
            s[0] = s[0].replace('/', '')
            command = s[0]
            handle = s[1]
            message = ' '.join(word for word in s[2::])

            self.send({"command":command, "handle": handle, "message":message}, self.serverAddressPort)
        else:
            self.output.append("Error: Not Connected to a server!")
            self.event.set()

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

    def parseInput(self, input):
        s = input.split()
        
        if "/join" in s[0]:
            if not len(s)==3:
                self.output.append("Error: Command parameters do not match or is not allowed.")
                self.event.set()
            else:
                self.join(s)
        elif "/leave" in s[0]:
            if not len(s)==1:
                self.output.append("Error: Command parameters do not match or is not allowed.")
                self.event.set()
            else:
                self.leave()
        elif "/register" in s[0]:
            if not len(s)==2:
                self.output.append("Error: Command parameters do not match or is not allowed.")
                self.event.set()
            else:
                self.register(s)
        elif "/all" in s[0]:
            if len(s)<2:
                self.output.append("Error: Command parameters do not match or is not allowed.")
                self.event.set()
            else:
                self.msgAll(s)
        elif "/msg" in s[0]:
            if len(s)<3:
                self.output.append("Error: Command parameters do not match or is not allowed.")
                self.event.set()
            else:
                self.msgOne(s)
        elif "/?" in s[0]:
            if not len(s)==1:
                self.output.append("Error: Command parameters do not match or is not allowed.")
                self.event.set()
            else:
                self.question()
        else:
            self.output.append("Error: Command not found")
            self.event.set()
#####################

def clientProgram():
    client = Client()
    while True:
        client.parseInput(input())

def start():
    print("Client Started...")
    program = threading.Thread(target=clientProgram)

    program.start()

