import socket
import json

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

    # This function finds the address based on the handle/alias name
    def findHandle(self, handle):
        if handle in self.clients:
            return self.clients[handle]
        else:
            return False

    def join(self, clientAddress):
        self.send(str({"command":"msg", "handle":"Server", "message":"Connection to the Message Board Server is successful!"}), clientAddress)

    def leave(self, clientAddress):
        self.send(str({"command":"msg", "handle":"Server", "message":"Connection closed. Thank you!"}), clientAddress)

    def register(self, name, clientAddress):
        if name in self.clients:
            self.send(str({"command":"error", "message":"Error: Registration failed. Handle or alias already exists."}))
        else:
            self.clients['name'] = clientAddress
            self.send(str({"command":"msg", "handle":"Server", "message":"Welcome!"}), clientAddress)

    def msgAll(self, msg):
        for address in self.clients.values():
            self.send(msg, address)

    def msgOne(self, msg:str, clientAddress:tuple):
        # find address of handler in dictionary
        address = self.findHandle(msg["handle"])
        
        if address:
            self.send(msg, address)
        else:
            self.send(str({"command":"error", "message":"Error: Handle or alias not found."}), clientAddress)

    def send(self, msg:str, address:tuple):
        bytesToSend = str.encode(json.dumps(msg))
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
        clientMsgStr = json.loads(byteMsg.decode())
        print("Server Recieved: ",clientMsgStr)

        # Respond
        match clientMsgStr[0]:
            case "join":
                server.join(clientAddress)
            case "leave":
                server.leave(clientAddress)
            case "register":
                server.register(clientAddress)
            case "all":
                server.msgAll(clientMsgStr)
            case "msg":
                server.msgOne(clientMsgStr, clientAddress)
            case _:
                # Return error message
                server.send(str({"command":"error", "message":"Error: Command parameters do not match or is not allowed."}), clientAddress)


main()