import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from auxilliary_application.key_gen_app.keygen import GenerateAndSaveKeys
from utils.commonFunctions import searchForPendrive


ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")  

class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Key generation")
        self.geometry("400x400")

        vcmd = (self.register(self.validatePin),"%P")
        
        self.publicKeyPath = None
        self.DELAY_IN_MS = 1000

        self.pendriveListLabel = ctk.CTkLabel(self, text="Available pendrives:")
        self.pendriveComboBox = ctk.CTkComboBox(self, values=[])
        self.detectButton = ctk.CTkButton(self, text="Detect", command=self.detectPendrive)
        self.inputLabel = ctk.CTkLabel(self, text="Input 8-digit PIN code for the encryption key")
        self.inputField = ctk.CTkEntry(self, show="*",validate="key" ,validatecommand=vcmd)
        self.inputFieldStatus = ctk.CTkLabel(self, text="")
        self.publicKeyPathLabel = ctk.CTkLabel(self, text="Select where you want to save the private key:")
        self.publicKeyPathButton = ctk.CTkButton(self, text="Select file path", command=self.selectFileLocation)
        self.publicKeyPathInfo = ctk.CTkLabel(self, text="")
        self.submitButton = ctk.CTkButton(self, text="Generate", command=self.getPin)
        self.generationStatusLabel = ctk.CTkLabel(self, text="")
        
        self.pendriveListLabel.pack(padx=20,pady=5)
        self.pendriveComboBox.pack(fill="x",padx=100,pady=5)
        self.detectButton.pack(padx=20,pady=5)
        self.inputLabel.pack(padx=20,pady=5)
        self.inputField.pack(padx=20,pady=5)
        self.inputFieldStatus.pack(padx=20,pady=0)
        self.publicKeyPathLabel.pack(padx=20,pady=5)
        self.publicKeyPathButton.pack(padx=20,pady=5)
        self.publicKeyPathInfo.pack(padx=20,pady=0)
        self.submitButton.pack(padx=20,pady=10)
        self.generationStatusLabel.pack(padx=20,pady=0)

        self.pendriveComboBox.configure(state="readonly")

        self.pendrives = searchForPendrive()
        self.updateInputState()        

    def getPin(self):
        pinCode = self.inputField.get()
        selectedPendrive = self.pendriveComboBox.get()

        def generateInThread():
            result = GenerateAndSaveKeys(self, pinCode, selectedPendrive, self.publicKeyPath, self.DELAY_IN_MS)
            self.after(self.DELAY_IN_MS*6, showMessageBox, result)

        def showMessageBox(result):
            if result == True:
                CTkMessagebox(
                    title="Key generation successful",
                    message="Private and public keys have been generated and saved! You can close the application now.",
                    option_1="OK",
                    icon="check"
                    )
            else:
                CTkMessagebox(
                    title="Key generation failed",
                    message="There was an error in saving the keys.",
                    option_1="Cancel",
                    icon="cancel"
                    )
                
        thread = threading.Thread(target=generateInThread)
        thread.start()

    def detectPendrive(self):
        self.pendrives = searchForPendrive()
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

        if not self.publicKeyPath:
            self.submitButton.configure(state="disabled")

        
    def validatePin(self, value):
        print("Wykonuje walidacje")
        if value.isdigit() and len(value) <= 8:
            if len(value) == 8:
                self.submitButton.configure(state="normal")
                self.inputFieldStatus.configure(text="PIN is valid.", text_color="green")
            else:
                self.submitButton.configure(state="disabled")
                self.inputFieldStatus.configure(text="PIN is invalid!", text_color="red")
            return True
        else:
            self.submitButton.configure(state="disabled")
            self.inputFieldStatus.configure(text="PIN is invalid!", text_color="red")
            return False
    
    def selectFileLocation(self):
        path = ctk.filedialog.askdirectory(title="Select public key save location")

        if path:
            self.publicKeyPath = path
            self.publicKeyPathInfo.configure(text=f"Selected path:\n{path}")

    def setGenerationStatusLabelText(self, state):
        self.generationStatusLabel.configure(text=state)



