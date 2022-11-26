import socket

class Server:
    def __init__(self, address=socket.gethostbyname(socket.gethostname()), port=20001, bufferSize=1024):
        self.bufferSize = bufferSize
        self.address = address
        self.port = port
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        self.UDPServerSocket.bind((self.address, self.port))

    def bind(self, address, port):
        self.address = address
        self.port = port
        self.UDPServerSocket.bind((self.address, self.port))

    def recieve(self):
        return self.UDPServerSocket.recvfrom(self.bufferSize)

    def join(self, address):
        self.msgOne("pong", address)

    def leave(self):
        pass

    def register(self):
        pass

    def msgAll(self):
        pass

    def msgOne(self, msg:str, address):
        # make json
        msgjson = 
        bytesToSend = str.encode(msgjson.)
        self.UDPServerSocket.sendto(bytesToSend, address)

def main():
    server = Server()

    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = server.recieve()
        byteMsg = bytesAddressPair[0]
        byteAddress = bytesAddressPair[1]

        # decode
        clientMsg = str.decode(byteMsg)
        clientAddress = str.decode(byteAddress)

        # Respond
        match clientMsg["command"]:
            case "join":
                server.join(clientAddress)
            case "leave":
                pass
            case "register":
                pass
            case "all":
                pass
            case "msg":
                pass
            case _:
                # Return error message
                server.msgOne("Error: Command parameters do not match or is not allowed.", clientAddress)


main()