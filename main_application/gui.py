import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from auxilliary_application.keygen import GenerateAndSaveKeys
from utils.commonFunctions import searchForPendrive

MENU_STATE_MAIN = 1
MENU_STATE_SIGNING = 2
MENU_STATE_VERIFYING = 3

ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")  

class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main application")
        self.geometry("400x400")

        self.vcmd = (self.register(self.validatePin),"%P")

        self.titleLabel = ctk.CTkLabel(self, text="PAdES Signer Application", font=("Arial", 30))
        self.signFileButton = ctk.CTkButton(self, width=180, height=50, text="Sign the PDF file", font=("Arial", 15), command=self.signFileMenu)
        self.verifyFileButton = ctk.CTkButton(self, width=180, height=50, text="Verify the PDF file", font=("Arial", 15), command=self.verifyFileMenu)
        
        self.inputLabel = ctk.CTkLabel(self, text="Input 8-digit PIN code")
        self.inputField = ctk.CTkEntry(self, show="*",validate="key" ,validatecommand=self.vcmd)
        self.inputFieldStatus = ctk.CTkLabel(self, text="")

        self.pdfFilePathButton = ctk.CTkButton(self, text="Select file path", command=self.selectFileLocation)
        self.pdfFilePathInfo = ctk.CTkLabel(self, text="")
        
        self.submitSignButton = ctk.CTkButton(self, text="Submit", command=self.signPdfFile)
        self.infoAboutSigningDocument = ctk.CTkLabel(self, text="The entered PIN is associated with your private key!", text_color="green")

        self.submitVerifyButton = ctk.CTkButton(self, text="Submit", command=self.verifyPdfFile)
        self.infoAboutVerifyingDocument = ctk.CTkLabel(self, text="The PDF file is identical to the originally signed document!", text_color="green")
        
        self.returnToMenuButton = ctk.CTkButton(self, text="Back", command=self.returnToMenu)

        self.titleLabel.pack(pady=(40, 0))
        self.signFileButton.pack(pady=(60,20))
        self.verifyFileButton.pack(pady=(30.0))

        self.isPdfFileSelected = False
        self.isValidPin = False
        self.menuState = MENU_STATE_MAIN

    def signFileMenu(self):
        self.menuState = MENU_STATE_SIGNING
        self.signFileButton.pack_forget()
        self.verifyFileButton.pack_forget()

        self.inputLabel.pack(pady=(20,0))
        self.inputField.pack(pady=(10,0))
        self.inputFieldStatus.pack(pady=(10,0))
        self.pdfFilePathButton.pack(pady=(10,0))
        self.pdfFilePathInfo.pack(pady=(10,0))
        self.submitSignButton.pack(pady=(10,0))
        self.infoAboutSigningDocument.pack(pady=(10,0))
        self.returnToMenuButton.pack(pady=(10,0))

        self.submitSignButton.configure(state="disabled")
        

    def verifyFileMenu(self):
        self.menuState = MENU_STATE_VERIFYING
        self.signFileButton.pack_forget()
        self.verifyFileButton.pack_forget()

        self.pdfFilePathButton.pack(pady=(60,0))
        self.pdfFilePathInfo.pack(pady=(10,0))
        self.submitVerifyButton.pack(pady=(10,0))
        self.infoAboutVerifyingDocument.pack(pady=(10,0))
        self.returnToMenuButton.pack(pady=(10,0))

        self.submitVerifyButton.configure(state="disabled")

    def validatePin(self, value):
        if value.isdigit() and len(value) <= 8:
            if len(value) == 8:
                self.inputFieldStatus.configure(text="PIN is valid.", text_color="green")
                self.isValidPin = True
                self.updateMenuState()
            else:
                self.inputFieldStatus.configure(text="PIN is invalid!", text_color="red")
                self.isValidPin = False
                self.updateMenuState()
            return True
        else:
            self.inputFieldStatus.configure(text="PIN is invalid!", text_color="red")
            self.isValidPin = False
            self.updateMenuState()
            return False
        
    def selectFileLocation(self):
        path = ctk.filedialog.askopenfilename(title="Select the PDF file", filetypes=[("PDF files", "*.pdf")])

        if path:
            self.isPdfFileSelected = True
            self.pdfFilePathInfo.configure(text=f"Selected path:\n{path}")
        else:
            self.isPdfFileSelected = False
        
        self.updateMenuState()

    def signPdfFile(self):
        pass

    def verifyPdfFile(self):
        pass

    def updateMenuState(self):
        if self.menuState == MENU_STATE_SIGNING:
            self.updateSignPdfFileMenuState()
        elif self.menuState == MENU_STATE_VERIFYING:
            self.updateVerifyPdfFileMenuState()

    def updateSignPdfFileMenuState(self):
        if self.isValidPin and self.isPdfFileSelected:
            self.submitSignButton.configure(state="normal")
        else:
            self.submitSignButton.configure(state="disabled")

    def updateVerifyPdfFileMenuState(self):
        if self.isPdfFileSelected:
            self.submitVerifyButton.configure(state="normal")
        else:
            self.submitVerifyButton.configure(state="disabled")

    def resetSignPdfFileMenu(self):
        self.inputField.configure(validate="none")  
        self.inputField.delete(0, "end")
        self.inputField.configure(validate="key" ,validatecommand=self.vcmd)
        self.inputFieldStatus.configure(text="")
            
        self.inputLabel.pack_forget()
        self.inputField.pack_forget()
        self.inputFieldStatus.pack_forget()
        self.pdfFilePathButton.pack_forget()
        self.pdfFilePathInfo.pack_forget()
        self.submitSignButton.pack_forget()
        self.infoAboutSigningDocument.pack_forget()
        self.returnToMenuButton.pack_forget()

    def resetVerifyPdfFileMenu(self):
        self.pdfFilePathButton.pack_forget()
        self.pdfFilePathInfo.pack_forget()
        self.submitVerifyButton.pack_forget()
        self.infoAboutVerifyingDocument.pack_forget()
        self.returnToMenuButton.pack_forget()

    def returnToMenu(self):
        self.isValidPin = False
        self.isPdfFileSelected = False
        self.pdfFilePathInfo.configure(text="")

        if self.menuState == MENU_STATE_SIGNING:
            self.menuState = MENU_STATE_MAIN
            self.resetSignPdfFileMenu()
            
        elif self.menuState == MENU_STATE_VERIFYING:
            self.menuState = MENU_STATE_MAIN
            self.resetVerifyPdfFileMenu()
            
        self.titleLabel.pack(pady=(40, 0))
        self.signFileButton.pack(pady=(60,20))
        self.verifyFileButton.pack(pady=(30.0))
