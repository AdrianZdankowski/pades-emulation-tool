import customtkinter as ctk
import psutil

ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")  

class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Key generation")
        self.geometry("400x300")
        
        
        self.alertLabel = ctk.CTkLabel(self, text="Lorem ipsum")
        self.inputLabel = ctk.CTkLabel(self, text="Input 8-digit PIN code for a encryption key")
        self.inputField = ctk.CTkEntry(self, show="*")
        self.submitButton = ctk.CTkButton(self, text="Generate", command=self.getPin)
        
        self.alertLabel.pack(padx=20,pady=20)
        self.inputLabel.pack(padx=20,pady=5)
        self.inputField.pack(padx=20,pady=5)
        self.submitButton.pack(padx=20,pady=20)

        self.pendrives = self.searchForPendrive()
        self.showPendrives(self.pendrives)

        if not self.pendrives:
            self.inputField.configure(state="disabled")

    def searchForPendrive(self):
        pendrives = []
        for partition in psutil.disk_partitions(all=False):
            if 'removable' in partition.opts.lower():
                pendrives.append(partition.device)
        return pendrives

    def getPin(self):
        pinCode = self.inputField.get()
        print(f"Entered pin: {pinCode}")

    def showPendrives(self,pendrives):
        if pendrives:
            self.alertLabel.configure(text=f"Connected pendrives: {', '.join(pendrives)}")
        else:
            self.alertLabel.configure(text="No connected pendrive detected!")

    



