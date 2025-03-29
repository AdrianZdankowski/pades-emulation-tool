import customtkinter as ctk, time
from utils.commonFunctions import searchForPendrive, searchAndReadPrivateKey
from main_application.signAndVerifyPDF import signPdfAndVerifyPin, verifyPdfFiles
from CTkMessagebox import CTkMessagebox

MENU_STATE_MAIN = 1
MENU_STATE_SIGNING = 2
MENU_STATE_VERIFYING = 3
PRIVATE_KEY_PATH = "Key/encrypted_PK.bin"

NO_SIGNATURE = 1
SIGNATURE_VERIFICATION_VALUE_ERROR = 2
UNKNOWN_ERROR = 3

INFO_ABOUT_SIGNING_DOCUMENT = 1
INFO_ABOUT_VERIFYING_DOCUMENT = 2

PDF_FILE = 1
PUBLIC_KEY_FILE = 2

ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")  

class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main application")
        self.geometry("600x600")

        self.vcmd = (self.register(self.validatePin),"%P")

        self.titleLabel = ctk.CTkLabel(self, text="Tool for Emulating\n the PAdES Qualified Electronic Signature", font=("Arial", 30))
        self.signFileMenuButton = ctk.CTkButton(self, width=280, height=70, text="Sign the PDF file", font=("Arial", 20), command=self.signFileMenu)
        self.verifyFileMenuButton = ctk.CTkButton(self, width=280, height=70, text="Verify the PDF file", font=("Arial", 20), command=self.verifyFileMenu)
        self.detectPendriveButton = ctk.CTkButton(self, width=280, height=70, text="Search pendrive again", font=("Arial", 20), command=self.checkIfPendriveSearched)
        self.infoAboutPendrive = ctk.CTkLabel(self, text="No pendrive detected\n or\n private key not found!\n\n Please try again!", font=("Arial", 30), text_color="red")

        self.inputLabel = ctk.CTkLabel(self, text="Input 8-digit PIN code", font=("Arial", 20))
        self.inputField = ctk.CTkEntry(self, show="*",validate="key" ,validatecommand=self.vcmd, width=280, height=30)
        self.inputFieldStatus = ctk.CTkLabel(self, text="")

        self.pdfFilePathButton = ctk.CTkButton(self, width=280, height=60, text="Select file path", font=("Arial", 20), command=lambda:self.selectFileLocation("Select the PDF file", [("PDF files", "*.pdf")], PDF_FILE))
        self.pdfFilePathInfo = ctk.CTkLabel(self, text="")

        self.publicKeyPathButton = ctk.CTkButton(self, width=280, height=60, text="Select public key path", font=("Arial", 20), command=lambda:self.selectFileLocation("Select the Public Key file", [("PEM files", "*.pem")], PUBLIC_KEY_FILE))
        self.publicKeyPathInfo = ctk.CTkLabel(self, text="")
        
        self.submitSignButton = ctk.CTkButton(self, width=280, height=60, text="Submit", font=("Arial", 20), command=self.signPdfFile)
        self.infoAboutSigningDocument = ctk.CTkLabel(self, text="", font=("Arial", 20))

        self.submitVerifyButton = ctk.CTkButton(self, width=280, height=60, text="Submit", font=("Arial", 20), command=self.verifyPdfFile)
        self.infoAboutVerifyingDocument = ctk.CTkLabel(self, text="", font=("Arial", 20))
        
        self.returnToMenuButton = ctk.CTkButton(self, width=180, height=40, text="Back", font=("Arial", 15), command=self.returnToMenu)

        self.pendrives = []
        self.privateKey = ""

        self.titleLabel.pack(pady=(40, 20))
        self.checkIfPendriveSearched()

        self.isPdfFileSelected = False
        self.isPublicKeySelected = False
        self.isValidPin = False
        self.menuState = MENU_STATE_MAIN

    def checkIfPendriveSearched(self):
        if self.detectPendriveAndReadPrivateKey():
            if self.infoAboutPendrive.winfo_ismapped():
                self.infoAboutPendrive.pack_forget()
            if self.detectPendriveButton.winfo_ismapped():
                self.detectPendriveButton.pack_forget()

            self.signFileMenuButton.pack(pady=(100,20))
            self.verifyFileMenuButton.pack(pady=(70.0))
        else:
            if self.signFileMenuButton.winfo_ismapped():
                self.signFileMenuButton.pack_forget()
            if self.verifyFileMenuButton.winfo_ismapped():
                self.verifyFileMenuButton.pack_forget()

            self.infoAboutPendrive.pack(pady=(80,20))
            self.detectPendriveButton.pack(pady=(50,0))
                        
    def detectPendriveAndReadPrivateKey(self):
        self.pendrives = searchForPendrive()
        if len(self.pendrives) == 0:
            return False
        self.privateKey = searchAndReadPrivateKey(self.pendrives, PRIVATE_KEY_PATH)
        if self.privateKey != "Not found":
            return True
        return False

    def resetMainMenu(self):
        if self.signFileMenuButton.winfo_ismapped():
            self.signFileMenuButton.pack_forget()
        if self.verifyFileMenuButton.winfo_ismapped():
            self.verifyFileMenuButton.pack_forget()

    def signFileMenu(self):
        self.menuState = MENU_STATE_SIGNING
        self.resetMainMenu()

        self.inputLabel.pack(pady=(15,0))
        self.inputField.pack(pady=(15,0))
        self.inputFieldStatus.pack(pady=(15,0))
        self.pdfFilePathButton.pack(pady=(15,0))
        self.pdfFilePathInfo.pack(pady=(15,0))
        self.submitSignButton.pack(pady=(15,0))
        self.infoAboutSigningDocument.pack(pady=(15,0))
        self.returnToMenuButton.pack(pady=(15,0))

        self.submitSignButton.configure(state="disabled")
        

    def verifyFileMenu(self):
        self.menuState = MENU_STATE_VERIFYING
        self.resetMainMenu()

        self.pdfFilePathButton.pack(pady=(15,0))
        self.pdfFilePathInfo.pack(pady=(15,0))
        self.publicKeyPathButton.pack(pady=(15,0))
        self.publicKeyPathInfo.pack(pady=(15,0))
        self.submitVerifyButton.pack(pady=(15,0))
        self.infoAboutVerifyingDocument.pack(pady=(15,0))
        self.returnToMenuButton.pack(pady=(25,0))

        self.submitVerifyButton.configure(state="disabled")

    def validatePin(self, value):
        if value.isdigit() and len(value) <= 8:
            if len(value) == 8:
                self.inputFieldStatus.configure(text="PIN is valid.", font=("Arial", 20), text_color="green")
                self.isValidPin = True
                self.updateMenuState()
            else:
                self.inputFieldStatus.configure(text="PIN is invalid!", font=("Arial", 20), text_color="red")
                self.isValidPin = False
                self.updateMenuState()
            return True
        else:
            self.inputFieldStatus.configure(text="PIN is invalid!", font=("Arial", 20), text_color="red")
            self.isValidPin = False
            self.updateMenuState()
            return False
        
    def selectFileLocation(self, title, filetypes, type):
        path = ctk.filedialog.askopenfilename(title=title, filetypes=filetypes)

        if path:
            if type == PDF_FILE:
                self.isPdfFileSelected = True
                self.pdfFilePathInfo.configure(text=f"Selected path:\n{path}", font=("Arial", 20))
            elif type == PUBLIC_KEY_FILE:
                self.isPublicKeySelected = True
                self.publicKeyPathInfo.configure(text=f"Selected path:\n{path}", font=("Arial", 20))
        else:
            if type == PDF_FILE:
                self.isPdfFileSelected = False
            elif type == PUBLIC_KEY_FILE:
                self.isPublicKeySelected = False

        self.updateMenuState()

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
        if self.isPdfFileSelected and self.isPublicKeySelected:
            self.submitVerifyButton.configure(state="normal")
        else:
            self.submitVerifyButton.configure(state="disabled")

    def resetSignPdfFileMenu(self):
        self.inputField.configure(validate="none")  
        self.inputField.delete(0, "end")
        self.inputField.configure(validate="key" ,validatecommand=self.vcmd)
        self.inputFieldStatus.configure(text="")
        self.infoAboutSigningDocument.configure(text="")
            
        self.inputLabel.pack_forget()
        self.inputField.pack_forget()
        self.inputFieldStatus.pack_forget()
        self.pdfFilePathButton.pack_forget()
        self.pdfFilePathInfo.pack_forget()
        self.submitSignButton.pack_forget()
        self.infoAboutSigningDocument.pack_forget()
        self.returnToMenuButton.pack_forget()

    def resetVerifyPdfFileMenu(self):
        self.publicKeyPathInfo.configure(text="")
        self.infoAboutVerifyingDocument.configure(text="")

        self.pdfFilePathButton.pack_forget()
        self.pdfFilePathInfo.pack_forget()
        self.publicKeyPathButton.pack_forget()
        self.publicKeyPathInfo.pack_forget()
        self.submitVerifyButton.pack_forget()
        self.infoAboutVerifyingDocument.pack_forget()
        self.returnToMenuButton.pack_forget()

    def returnToMenu(self):
        self.isValidPin = False
        self.isPdfFileSelected = False
        self.isPublicKeySelected = False
        self.pdfFilePathInfo.configure(text="")

        if self.menuState == MENU_STATE_SIGNING:
            self.resetSignPdfFileMenu()     
        elif self.menuState == MENU_STATE_VERIFYING:
            self.resetVerifyPdfFileMenu()
        
        self.menuState = MENU_STATE_MAIN
        self.signFileMenuButton.pack(pady=(100,20))
        self.verifyFileMenuButton.pack(pady=(70.0))
    
    def setLabelText(self, newText, labelType, color=None):
        if labelType == INFO_ABOUT_SIGNING_DOCUMENT:
            self.infoAboutSigningDocument.configure(text=newText)
            if color:
                self.infoAboutSigningDocument.configure(text_color=color)
        elif labelType == INFO_ABOUT_VERIFYING_DOCUMENT:
            self.infoAboutVerifyingDocument.configure(text=newText)
            if color:
                self.infoAboutVerifyingDocument.configure(text_color=color)
        if newText != "":
            time.sleep(1)

    def showMessageBox(self, title, message, option, icon):
        CTkMessagebox(
            title=title,
            message=message,
            option_1=option,
            icon=icon
        )

    def signPdfMessageBox(self, result):
        if result:
            self.showMessageBox("PDF Signing Completed Successfully", "The signed PDF file has been saved.", "OK", "check")
        else:
            self.showMessageBox("PDF Signing Failed", "An error occurred while signing the PDF file.", "Cancel", "cancel")

    def incorrectPinMessageBox(self):
        self.showMessageBox("Incorrect PIN Entered", "The PIN you entered is incorrect. Please try again.", "Cancel", "cancel")
    
    def verifyPdfSuccessfullyMessageBox(self):
        self.showMessageBox("PDF Signature Verification", "The PDF signature has been successfully verified.", "OK", "check")

    def verifyPdfErrorMessageBox(self, errorType):
        if errorType == NO_SIGNATURE:
            self.showMessageBox("PDF Signature Verification", "No signature found in the PDF document.", "Cancel", "cancel")
        elif errorType == SIGNATURE_VERIFICATION_VALUE_ERROR:
            self.showMessageBox("PDF Signature Verification", "The signature could not be verified due to an invalid value in the signature data.", "Cancel", "cancel")
        else:
            self.showMessageBox("PDF Signature Verification", "An unknown error occurred during PDF signature verification.", "Cancel", "cancel")

    def signPdfFile(self):
        signPdfAndVerifyPin(self, self.privateKey, self.inputField.get(), self.pdfFilePathInfo.cget("text").split("\n")[1])

    def verifyPdfFile(self):
        verifyPdfFiles(self, self.pdfFilePathInfo.cget("text").split("\n")[1], self.publicKeyPathInfo.cget("text").split("\n")[1])
