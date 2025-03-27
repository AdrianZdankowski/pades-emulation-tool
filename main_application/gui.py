import customtkinter as ctk
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
        self.geometry("600x600")

        self.vcmd = (self.register(self.validatePin),"%P")

        self.titleLabel = ctk.CTkLabel(self, text="Tool for Emulating\n the PAdES Qualified Electronic Signature", font=("Arial", 30))
        self.signFileMenuButton = ctk.CTkButton(self, width=280, height=70, text="Sign the PDF file", font=("Arial", 20), command=self.signFileMenu)
        self.verifyFileMenuButton = ctk.CTkButton(self, width=280, height=70, text="Verify the PDF file", font=("Arial", 20), command=self.verifyFileMenu)
        self.detectPendriveButton = ctk.CTkButton(self, width=280, height=70, text="Search pendrive again", font=("Arial", 20), command=self.checkIfPendriveSearched)
        self.infoAboutPendrive = ctk.CTkLabel(self, text="No pendrive detected! Please try again!", font=("Arial", 30), text_color="red")

        self.inputLabel = ctk.CTkLabel(self, text="Input 8-digit PIN code", font=("Arial", 20))
        self.inputField = ctk.CTkEntry(self, show="*",validate="key" ,validatecommand=self.vcmd, width=280, height=30)
        self.inputFieldStatus = ctk.CTkLabel(self, text="")

        self.pdfFilePathButton = ctk.CTkButton(self, width=280, height=60, text="Select file path", font=("Arial", 20), command=self.selectFileLocation)
        self.pdfFilePathInfo = ctk.CTkLabel(self, text="")
        
        self.submitSignButton = ctk.CTkButton(self, width=280, height=60, text="Submit", font=("Arial", 20), command=self.signPdfFile)
        self.infoAboutSigningDocument = ctk.CTkLabel(self, text="The entered PIN is associated with your private key!", font=("Arial", 20), text_color="green")

        self.submitVerifyButton = ctk.CTkButton(self, width=280, height=60, text="Submit", font=("Arial", 20), command=self.verifyPdfFile)
        self.infoAboutVerifyingDocument = ctk.CTkLabel(self, text="The PDF file is identical to the originally signed document!", font=("Arial", 20), text_color="green")
        
        self.returnToMenuButton = ctk.CTkButton(self, width=280, height=60, text="Back", font=("Arial", 20), command=self.returnToMenu)

        self.pendrives = []

        self.titleLabel.pack(pady=(40, 20))
        self.checkIfPendriveSearched()

        self.isPdfFileSelected = False
        self.isValidPin = False
        self.menuState = MENU_STATE_MAIN


    def checkIfPendriveSearched(self):
        if self.detectPendrive():
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


    def detectPendrive(self):
        self.pendrives = searchForPendrive()
        if len(self.pendrives) == 0:
            return False
        return True

    def resetMainMenu(self):
        if self.infoAboutPendrive.winfo_ismapped():
            self.infoAboutPendrive.pack_forget()
        if self.detectPendriveButton.winfo_ismapped():
            self.detectPendriveButton.pack_forget()
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

        self.pdfFilePathButton.pack(pady=(60,0))
        self.pdfFilePathInfo.pack(pady=(30,0))
        self.submitVerifyButton.pack(pady=(30,0))
        self.infoAboutVerifyingDocument.pack(pady=(30,0))
        self.returnToMenuButton.pack(pady=(45,0))

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
        
    def selectFileLocation(self):
        path = ctk.filedialog.askopenfilename(title="Select the PDF file", filetypes=[("PDF files", "*.pdf")])

        if path:
            self.isPdfFileSelected = True
            self.pdfFilePathInfo.configure(text=f"Selected path:\n{path}", font=("Arial", 20))
        else:
            self.isPdfFileSelected = False
        
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
            
        self.checkIfPendriveSearched()

    def signPdfFile(self):
        pass

    def verifyPdfFile(self):
        pass
