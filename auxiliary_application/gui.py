##
#@file gui.py
#@brief GUI handling for the auxiliary application.
#
#This module defines the graphical user interface components for the key generation application.
#It allows the user to input a PIN code, select a pendrive for saving the keys, and handle key generation
#using a graphical interface. The GUI is built using the `customtkinter` library.
#
#Classes:
#    - Gui: The main GUI class that handles the user interface for key generation, pendrive detection,
#           and managing the state of the input fields.
#
#Functions:
#    - getPin: Handles the logic for key generation in a separate thread, after validating the PIN and
#              selecting a pendrive.
#    - detectPendrive: Detects available pendrives and updates the GUI with the list.
#    - updateInputState: Updates the state of the input fields based on available pendrives and public key
#                        file selection.
#    - validatePin: Validates the entered PIN code (ensures it is a valid 8-digit number).
#    - selectFileLocation: Opens a dialog to select the location to save the public key.
#    - setGenerationStatusLabelText: Sets the status label text for key generation status.
#
import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from .keygen import GenerateAndSaveKeys
from utils.commonFunctions import searchForPendrive


ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")  
##
#@class Gui
#@brief The main GUI class that handles the user interface for key generation, pendrive detection,
#and managing the state of the input fields.
#
#This class defines the GUI elements such as buttons, labels, input fields, and combo boxes.
#It also handels validation of the entered PIN code.
#
class Gui(ctk.CTk):
    ##
    #@brief The constructor of the class. Initializes the GUI components and sets up the layout.
    #
    #@details It creates all the GUI elements (buttons, labels, combo boxes) and arranges them in a window using the
    #pack geometry manager. Additionally, it initializes the pendrive list and updates the state of the input fields.
    #
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
        self.publicKeyPathLabel = ctk.CTkLabel(self, text="Select where you want to save the public key:")
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

    ##
    #@brief Handles the key generation process after validating the PIN code and selecting a pendrive.
    #
    #    This method runs the key generation logic in a separate thread to avoid blocking the main UI thread.
    #    It uses the `GenerateAndSaveKeys` function to generate and save the keys.
    #
    #    After completion, a message box is displayed to inform the user of the success or failure of the process.
    #
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

    ##
    #@brief Detects available pendrives and updates the pendrive combo box in the GUI.
    #
    #This method is called when the user clicks the "Detect" button. It updates the list of available pendrives
    #and the input state accordingly.
    #
    def detectPendrive(self):
        self.pendrives = searchForPendrive()
        self.updateInputState()

    ##
    #@brief Updates the state of the input fields based on the available pendrives and selected save location.
    #
    #If pendrives are detected, the input field and submit button are enabled. If no pendrives are detected,
    #the input field and submit button are disabled.
    #If no public key path is selected, the submit button is also disabled.
    #
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

    ##
    # @brief Validates the entered PIN code.
    #
    #    @param value The entered PIN code.
    #    @return True if the PIN is valid, False otherwise.
    #
    #    The PIN must be a numeric string and should have a maximum length of 8 digits. The validation is used
    #    to enable or disable the submit button and provide feedback to the user regarding the validity of the PIN.
    #  
    def validatePin(self, value):
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
    

    ##
    # @brief Opens a dialog to select the location for saving the public key.
    # After selecting a location, the path is displayed in the GUI.
    #   
    def selectFileLocation(self):
        path = ctk.filedialog.askdirectory(title="Select public key save location")

        if path:
            self.publicKeyPath = path
            self.publicKeyPathInfo.configure(text=f"Selected path:\n{path}")

    ##
    # @brief Sets the status label text for key generation process.
    # @param state The status text to display.
    #
    def setGenerationStatusLabelText(self, state):
        self.generationStatusLabel.configure(text=state)



