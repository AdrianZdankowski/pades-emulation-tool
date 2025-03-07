import customtkinter as ctk
import psutil

ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")  

class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Key generation")
        self.geometry("400x300")

        vcmd = (self.register(self.validatePin),"%P")
        
        self.pendriveListLabel = ctk.CTkLabel(self, text="Available pendrives:")
        self.pendriveComboBox = ctk.CTkComboBox(self, values=[])
        self.detectButton = ctk.CTkButton(self, text="Detect", command=self.detectPendrive)
        self.inputLabel = ctk.CTkLabel(self, text="Input 8-digit PIN code for the encryption key")
        self.inputField = ctk.CTkEntry(self, show="*",validate="key" ,validatecommand=vcmd)
        self.submitButton = ctk.CTkButton(self, text="Generate", command=self.getPin)
        
        self.pendriveListLabel.pack(padx=20,pady=5)
        self.pendriveComboBox.pack(fill="x",padx=100,pady=5)
        self.detectButton.pack(padx=20,pady=5)
        self.inputLabel.pack(padx=20,pady=5)
        self.inputField.pack(padx=20,pady=5)
        self.submitButton.pack(padx=20,pady=20)

        self.pendriveComboBox.configure(state="readonly")

        self.pendrives = self.searchForPendrive()
        self.updateInputState()        

    def searchForPendrive(self):
        pendrives = []
        for partition in psutil.disk_partitions(all=False):
            if 'removable' in partition.opts.lower():
                pendrives.append(partition.device)
        return pendrives

    def getPin(self):
        pinCode = self.inputField.get()
        selected = self.pendriveComboBox.get()
        print(f"Entered pin: {pinCode}")
        print(f"Selected pendrive: {selected}")

    def detectPendrive(self):
        self.pendrives = self.searchForPendrive()
        self.updateInputState()

    def updateInputState(self):
        if self.pendrives:
            self.inputField.configure(state="normal")
            self.submitButton.configure(state="normal")
            self.pendriveComboBox.configure(values=self.pendrives)
            self.pendriveComboBox.set(self.pendrives[0])
        else:
            self.inputField.configure(state="disabled")
            self.submitButton.configure(state="disabled")
            self.pendriveComboBox.configure(values=["No pendrives detected!"])
            self.pendriveComboBox.set("No pendrives detected!")
        
    def validatePin(self, value):
        print("Wykonuje walidacje")
        if value.isdigit() and len(value) <= 8:
            if len(value) == 8:
                self.submitButton.configure(state="normal")
            else:
                self.submitButton.configure(state="disabled")
            return True
        else:
            self.submitButton.configure(state="disabled")
            return False
    



