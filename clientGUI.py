import socket
import json
from tabulate import tabulate
import threading
import ast
import customtkinter

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

class Client(customtkinter.CTk):
    width = 1050
    height = 400

    def __init__(self, bufferSize=1024):
        self.connected = False
        self.serverAddressPort = None
        self.bufferSize = bufferSize
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Calls for GUI
        super().__init__()
        self.geometry(f"{self.width}x{self.height}")
        self.title("CSNETWK-Message-Board-System")
        self.minsize(self.width, self.height)
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        #Top Frame
        topFrame = customtkinter.CTkFrame(master=self)
        topFrame.grid(row=0, column=0, padx=20, sticky="nsew")
        topFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        #Label
        label = customtkinter.CTkLabel(master=topFrame, text= "Message Board System", font=customtkinter.CTkFont(size=15, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        #Join
        self.idAddress = customtkinter.CTkEntry(master=topFrame, placeholder_text="Enter IP Address")
        self.idAddress.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        self.port = customtkinter.CTkEntry(master=topFrame, placeholder_text="Enter Port")
        self.port.grid(row=0, column=2, padx= (0,10), sticky="ew")
        joinButton = customtkinter.CTkButton(master=topFrame, width=50, command=self.button_join, text="Join")
        joinButton.grid(row=0, column=3, padx=(0, 20), sticky="ew")

        #Register
        self.registerUser = customtkinter.CTkEntry(master=topFrame, placeholder_text="Enter Username")
        self.registerUser.grid(row=0, column=4, padx=(0, 10), sticky="ew")
        registerButton = customtkinter.CTkButton(master=topFrame, width=75, command=self.button_register, text="Register")
        registerButton.grid(row=0, column=5, padx=(0,20), sticky="ew")

        #Leave
        leaveButton = customtkinter.CTkButton(master=topFrame, width=75, command=self.button_leave, text="Leave")
        leaveButton.grid(row=0, column=6, sticky="ew")

        #Help
        helpbutton = customtkinter.CTkButton(master=topFrame, width=25, command=self.button_help, text="Help")
        helpbutton.grid(row=0, column=7, padx=20, sticky="ew")

        #View Messages
        self.textbox = customtkinter.CTkTextbox(master=self, width=self.width-50)
        self.textbox.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")
        self.textbox.configure(state="disabled")

        #BottomFrame
        layoutFrame = customtkinter.CTkFrame(master=self)
        layoutFrame.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="nsew")
        layoutFrame.rowconfigure(0, weight=1)
        layoutFrame.columnconfigure((0, 1), weight=1)

        #Text Input
        self.user_input = customtkinter.CTkEntry(master=layoutFrame, width=self.width - 350, placeholder_text="Enter Message")
        self.user_input.grid(row=2, column=1, padx=5, pady=20, sticky="ew")
        
        # Msg to who Input
        self.destination = customtkinter.CTkEntry(master=layoutFrame, width=150, placeholder_text="Who to message?")
        self.destination.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        #Text Submit Button
        textSubmit = customtkinter.CTkButton(master=layoutFrame, width=100, command=self.button_send_message, text="Enter")
        textSubmit.grid(row=2, column=2, padx=20, pady=20, sticky="ew")

    def button_send_message(self):
        self.textbox.configure(state="normal")
        if self.destination.get() == all:
            self.msgAll(self.user_input.get())
        else:
            self.msgOne((self.destination.get(), self.user_input.get()))
        self.textbox.configure(state="disabled")
        self.user_input.delete(0, "end")
    
    def button_join(self):
        self.textbox.configure(state="normal")
        self.join((self.idAddress.get(), self.port.get()))
        self.textbox.configure(state="disabled")
        self.idAddress.delete(0, "end")
        self.port.delete(0, "end")

    def button_register(self):
        self.textbox.configure(state="normal")
        self.register(self.registerUser.get())
        self.textbox.configure(state="disabled")
        self.registerUser.delete(0, "end")

    def button_leave(self):
        self.textbox.configure(state="normal")
        self.leave()
        self.textbox.configure(state="disabled")

    def button_help(self):
        self.textbox.configure(state="normal")
        self.responses.append("insert", "Help: You must first join a server by inputting IP and port. Don't forget to register! If you want to message everyone then put the word 'all' in who to message box" + "\n")
        self.textbox.configure(state="disabled")
    
    ########################

    def join(self, s):
        if self.connected == False:
            self.serverAddressPort = (s[0], s[1])
            
            try:
                # Send to server using created UDP socket
                self.send({"command":"join"}, self.serverAddressPort)
                self.connected = True
                self.listener.start()
            except:
                self.connected = False
                self.responses.append("insert", "Join Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number." + "\n")
        else:
            self.responses.append("insert", "Currently Connected. Please do /leave first." + "\n")

    def leave(self):
        if self.connected:
            self.send({"command":"leave"}, self.serverAddressPort)
            self.connected = False
        else:
            self.responses.append("insert", "Error: Disconnection failed. Please connect to a server first." + "\n")

    def register(self, s):
        if self.connected:
            self.send({"command":"register", "handle":s}, self.serverAddressPort)
        else:
            self.responses.append("insert", "Error: Not Connected to a server!" + "\n")

    def msgAll(self, s):
        if self.connected:
            self.send({"command":"all", "message":s}, self.serverAddressPort)
        else:
            self.responses.append("insert", "Error: Not Connected to a server!" + "\n")

    def msgOne(self, s):
        if self.connected:
            handle = s[0]
            msg = s[1]

            self.send({"command":"msg", "handle": handle, "message":msg}, self.serverAddressPort)
        else:
            self.responses.append("insert", "Error: Not Connected to a server!" + "\n")

    def send(self, msg:str, address:tuple):
        bytesToSend = str.encode(json.dumps(str(msg)))
        self.UDPClientSocket.sendto(bytesToSend, (str(address[0]), int(address[1])))

##############################
def listen():
    while True:
        # Attempt to listen. Sometimes an error occurs even if already connected. 
        try:
            bytesAddressPair = recieve()
            # Convert recieved inputs
            byteMsg = bytesAddressPair[0]
            ServerMsgDict = ast.literal_eval(json.loads(byteMsg.decode()))
            
            client.textbox.insert("insert", ServerMsgDict["message"] + "\n") 
            
            if not client.connected:
                client.textbox.insert("insert", "[Client]: Disconnected from Server..." + "\n") 
                resetConnection()
        except:
            client.textbox.insert("insert", "Recieve Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number." + "\n") 
            resetConnection()

def recieve():
    return client.UDPClientSocket.recvfrom(client.bufferSize)

def resetConnection():
    client.serverAddressPort = None
    client.connected = False

#################

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
client = Client()
clientThread = threading.Thread(target=client.mainloop)
clientThread.start()

listen()

