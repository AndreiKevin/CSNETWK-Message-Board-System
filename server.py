import socket
import json
import ast

class Server:
    def __init__(self, address=socket.gethostbyname(socket.gethostname()), port=20001, bufferSize=1024):
        # self.clients is of type dict{string(handle) : tuple(address, port)}
        self.clients = {}
        self.bufferSize = bufferSize
        self.address = address
        self.port = port
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Set up address and ip for UDP server. It is automatic for client.
        self.UDPServerSocket.bind((self.address, self.port))

    def bind(self, address, port):
        self.address = address
        self.port = port
        self.UDPServerSocket.bind((self.address, self.port))

    # Given handle, returns address
    def findAddress(self, handle):
        if handle in self.clients:
            return self.clients[handle]
        else:
            return False

    # Given an address, returns handle
    def findHandle(self, address):
        for key, value in self.clients.items():
            if address == value:
                return key

        # If handle is not found, use address
        self.send({"command":"msg", "handle":"Server", "message":"[Server]: Message sent but register to also recieve messages."}, address)
        return address[0] + ' ' + str(address[1])

    def join(self, clientAddress):
        self.send({"command":"msg", "handle":"Server", "message":"[Server]: Connection to the Message Board Server is successful!"}, clientAddress)

    def leave(self, clientAddress):
        self.send({"command":"msg", "handle":"Server", "message":"[Server]: Connection closed. Thank you!"}, clientAddress)

    def register(self, name, clientAddress):
        if name in self.clients:
            self.send({"command":"error", "message":"[Server]: Error: Registration failed. Handle or alias already exists."}, clientAddress)
        else:
            self.clients[name] = clientAddress
            self.send({"command":"msg", "handle":"Server", "message":"[Server]: Welcome "+name+"!"}, clientAddress)
        
        print("Current Clients:", self.clients)

    def msgAll(self, msg, clientAddress):
        senderHandle = self.findHandle(clientAddress)

        msg["message"] = senderHandle + ': ' + msg["message"]
        for address in self.clients.values():
            self.send(msg, address)

    def msgOne(self, msg:dict, clientAddress:tuple):
        # find address of handler in dictionary
        address = self.findAddress(msg["handle"])
        serverResponse = {"command":"msg", "handle":"Server", "message":"[To " + msg["handle"] + "]: " + msg["message"]}
        senderHandle = self.findHandle(clientAddress)
        
        msg["message"] = '[From ' + senderHandle + ']: ' + msg["message"]
        if address:
            self.send(serverResponse, clientAddress)
            self.send(msg, address)
        else:
            self.send({"command":"error", "message":"[Server]: Error: Handle or alias not found."}, clientAddress)

    def send(self, msg:dict, address:tuple):
        bytesToSend = str.encode(json.dumps(str(msg)))
        self.UDPServerSocket.sendto(bytesToSend, address)

    def recieve(self):
        return self.UDPServerSocket.recvfrom(self.bufferSize)
        
######################

def main():
    server = Server()

    print(f'Server IP: {server.address}\nServer Port: {server.port}')
    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = server.recieve()
        byteMsg = bytesAddressPair[0]
        clientAddress = bytesAddressPair[1]

        # decode and turn to json
        clientMsgDict = ast.literal_eval(json.loads(byteMsg.decode()))
        print("Server Recieved: ", clientMsgDict)

        # Respond
        match clientMsgDict["command"]:
            case "join":
                server.join(clientAddress)
            case "leave":
                server.leave(clientAddress)
            case "register":
                server.register(clientMsgDict["handle"], clientAddress)
            case "all":
                server.msgAll(clientMsgDict, clientAddress)
            case "msg":
                server.msgOne(clientMsgDict, clientAddress)
            case _:
                # Return error message
                server.send(str({"command":"error", "message":"[Server]: Error: Command parameters do not match or is not allowed."}), clientAddress)


main()