from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from PyPDF2 import PdfReader, PdfWriter
import os, threading

NO_SIGNATURE = 1
SIGNATURE_VERIFICATION_VALUE_ERROR = 2
UNKNOWN_ERROR = 3
OK = 4

INFO_ABOUT_SIGNING_DOCUMENT = 1
INFO_ABOUT_VERIFYING_DOCUMENT = 2

def decryptPrivateKey(pin, privateKey):
    iv = privateKey[:16]
    cipherText = privateKey[16:]

    hashedPin = sha256(pin.encode()).digest()

    cipher = AES.new(hashedPin, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(cipherText), AES.block_size)

def verifyPin(pin, privateKey):
    try:
        decryptedPrivateKey = decryptPrivateKey(pin, privateKey)

        if decryptedPrivateKey:
           return True
        else:
            return False
    except Exception as e:
        return False

def createHash(pdfReader):
    hash = SHA256.new()
    for page in pdfReader.pages:
        hash.update(page.extract_text().encode())
    return hash

def signPDF(gui, privateKey, pin, pdfPath):
    try:
        base, ext = os.path.splitext(pdfPath)
        signedPdfPath = f"{base}-signed.pdf"
        decryptedPrivateKey = RSA.import_key(decryptPrivateKey(pin, privateKey))

        gui.setLabelText("Opening the PDF file ...", INFO_ABOUT_SIGNING_DOCUMENT, "white")
        with open(pdfPath, "rb") as f:
            pdfReader = PdfReader(f)
            pdfWriter = PdfWriter()

            gui.setLabelText("Generating hash of the PDF file ...", INFO_ABOUT_SIGNING_DOCUMENT)
            pdfHash = createHash(pdfReader)

            gui.setLabelText("Creating a digital signature ...", INFO_ABOUT_SIGNING_DOCUMENT)
            signature = pkcs1_15.new(decryptedPrivateKey).sign(pdfHash)

            gui.setLabelText("Adding a signature to the PDF file ...", INFO_ABOUT_SIGNING_DOCUMENT)
            for page in pdfReader.pages:
                pdfWriter.add_page(page)

            pdfWriter.add_metadata({
                "/Signature": signature
            })

            gui.setLabelText("Saving the signed PDF file ...", INFO_ABOUT_SIGNING_DOCUMENT)
            with open(signedPdfPath, "wb") as signedPDF:
                pdfWriter.write(signedPDF)

            return True
    except Exception as e:
        print(f"Error signing PDF: {e}")
        return False

def signPdfAndVerifyPin(gui, privateKey, pin, pdfPath):
    def signPdfThread():
        gui.setLabelText("Starting the PDF signing process ...", INFO_ABOUT_SIGNING_DOCUMENT)
        gui.setLabelText("Verifying PIN ...", INFO_ABOUT_SIGNING_DOCUMENT)
        
        if verifyPin(pin, privateKey):
            gui.setLabelText("PIN verified successfully", INFO_ABOUT_SIGNING_DOCUMENT, "green")
            if signPDF(gui, privateKey, pin, pdfPath):
                gui.setLabelText("", INFO_ABOUT_SIGNING_DOCUMENT)
                gui.signPdfMessageBox(True)
            else:
                gui.setLabelText("", INFO_ABOUT_SIGNING_DOCUMENT)
                gui.signPdfMessageBox(False)
        else:
            gui.setLabelText("", INFO_ABOUT_SIGNING_DOCUMENT)
            gui.incorrectPinMessageBox()

    threading.Thread(target=signPdfThread, daemon=True).start()

def verifyPdfSignatureFromMetadata(gui, pdfPath, publicKeyPath):
    try:
        gui.setLabelText("Reading the public key from file ...", INFO_ABOUT_VERIFYING_DOCUMENT)
        with open(publicKeyPath, "rb") as pub_file:
            public_key = RSA.import_key(pub_file.read())

        gui.setLabelText("Reading the PDF file ...", INFO_ABOUT_VERIFYING_DOCUMENT)
        with open(pdfPath, "rb") as f:
            pdfReader = PdfReader(f)
            metadata = pdfReader.metadata

            gui.setLabelText("Checking if signature exists in metadata ...", INFO_ABOUT_VERIFYING_DOCUMENT)
            if "/Signature" not in metadata:
                return NO_SIGNATURE

            signature = metadata["/Signature"]

            gui.setLabelText("Generating hash of the PDF file ...", INFO_ABOUT_VERIFYING_DOCUMENT)
            pdfHash = createHash(pdfReader)

            gui.setLabelText("Verifying the signature ...", INFO_ABOUT_VERIFYING_DOCUMENT)
            try:
                pkcs1_15.new(public_key).verify(pdfHash, signature)
                return OK
            except (ValueError, TypeError) as e:
                return SIGNATURE_VERIFICATION_VALUE_ERROR
    except Exception as e:
        print(f"Error verifying PDF signature: {e}")
        return UNKNOWN_ERROR
        
def verifyPdfFiles(gui, pdfPath, publicKeyPath):
    def verifyPdfThread():
        gui.setLabelText("Starting the PDF verification process ...", INFO_ABOUT_VERIFYING_DOCUMENT)

        result = verifyPdfSignatureFromMetadata(gui, pdfPath, publicKeyPath)
        gui.setLabelText("", INFO_ABOUT_VERIFYING_DOCUMENT)
        if result == OK:
            gui.verifyPdfSuccessfullyMessageBox()
        elif result == NO_SIGNATURE:
            gui.verifyPdfErrorMessageBox(NO_SIGNATURE)
        elif result == SIGNATURE_VERIFICATION_VALUE_ERROR:
            gui.verifyPdfErrorMessageBox(SIGNATURE_VERIFICATION_VALUE_ERROR)
        else:
            gui.verifyPdfErrorMessageBox(UNKNOWN_ERROR)

    threading.Thread(target=verifyPdfThread, daemon=True).start()

def checkPdfSignature(pdfPath):
    try:    
        with open(pdfPath, "rb") as f:
            pdfReader = PdfReader(f)
            metadata = pdfReader.metadata

            if metadata and "/Signature" in metadata:
                print("Signature found in the PDF metadata:", metadata["/Signature"])
            else:
                print("No signature found in the PDF metadata.")
    except Exception as e:
        print(f"Error reading the PDF file: {e}")

def modifyPdf(pdfPath):
    try:
        reader = PdfReader(pdfPath)
        writer = PdfWriter()

        signature = reader.metadata["/Signature"]

        for page in range(len(reader.pages)):
            writer.add_page(reader.pages[page])

        writer.add_page(reader.pages[0])

        writer.add_metadata({
            "/Signature": signature
        })

        with open(pdfPath, "wb") as f:
            writer.write(f)
    except Exception as e:
        print(f"Error modifying the PDF file: {e}")

#checkPdfSignature("")
#checkPdfSignature("")
#modifyPdf("")
