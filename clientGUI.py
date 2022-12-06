import customtkinter
from tabulate import tabulate

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    width = 1050
    height = 400

    def __init__(self):
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
        self.user_input = customtkinter.CTkEntry(master=layoutFrame, width=self.width - 200, placeholder_text="Enter Message")
        self.user_input.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        #Text Submit Button
        textSubmit = customtkinter.CTkButton(master=layoutFrame, width=50, command=self.button_send_message, text="Enter")
        textSubmit.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

    def button_send_message(self):
        self.textbox.configure(state="normal")
        self.textbox.insert("insert", self.user_input.get() + "\n")
        self.textbox.configure(state="disabled")
        self.user_input.delete(0, "end")
    
    def button_join(self):
        self.textbox.configure(state="normal")
        self.textbox.insert("insert", "Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.\n")
        self.textbox.configure(state="disabled")
        self.idAddress.delete(0, "end")
        self.port.delete(0, "end")

    def button_register(self):
        self.textbox.configure(state="normal")
        self.textbox.insert("insert", "Error: Registration failed. Handle or alias already exists.\n")
        self.textbox.configure(state="disabled")
        self.registerUser.delete(0, "end")

    def button_leave(self):
        self.textbox.configure(state="normal")
        self.textbox.insert("insert", "Error: Disconnection failed. Please connect to the server first.\n")
        self.textbox.configure(state="disabled")

    def button_help(self):
        commands = [
            ["/all <message>", "Send message to all"],
            ["/msg <handle> <message>", "Send direct message to a single handle"],
        ]
        header = ["Command", "Description"]
        print(tabulate(commands, headers=header))
        self.textbox.configure(state="normal")
        self.textbox.insert("insert", tabulate(commands, headers=header) + "\n")
        self.textbox.configure(state="disabled")
    
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
