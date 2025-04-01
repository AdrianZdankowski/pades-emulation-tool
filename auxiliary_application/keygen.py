##
#@file keygen.py
#@brief RSA key generation and encryption module.
#
#This module provides functions to generate RSA key pairs, encrypt private key, 
#and store them securely.
#
#Functions:
#    - GenerateAndSaveKeys: generates a pair of RSA keys, encrypts the private key and saves them in user's chosen locations.
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from hashlib import sha256
import os

##
#@brief Generates a private and public RSA key pair, encrypts the private key using a PIN, 
#           and saves both keys in specified locations.
#
#    @param gui GUI object used to update the generation status in the user interface.
#    @param pin PIN used to encrypt the private key.
#    @param pendrive Path to the pendrive where the encrypted private key will be saved.
#    @param publicKeyPath Path to the directory where the public key will be stored.
#    @param DELAY_IN_MS Delay in milliseconds used for updating the user interface status.
#
#    @return True if the key pair generation and saving operation is successful, False in case of an error.
#
def GenerateAndSaveKeys(gui, pin, pendrive, publicKeyPath, DELAY_IN_MS):
    try:
        gui.after(0, gui.setGenerationStatusLabelText, "Generating PIN hash...")
        pseudoRandomGenerator = get_random_bytes
        hashedPin = sha256(pin.encode()).digest()

        gui.after(DELAY_IN_MS, gui.setGenerationStatusLabelText, "Generating private and public key...")
        key = RSA.generate(4096, randfunc=pseudoRandomGenerator)
        privateKey = key.export_key()
        publicKey = key.public_key().export_key()

        gui.after(DELAY_IN_MS*2, gui.setGenerationStatusLabelText, "Encrypting private key...")
        cipher = AES.new(hashedPin, AES.MODE_CBC)
        iv = cipher.iv
        encryptedPrivateKey = iv + cipher.encrypt(pad(privateKey, AES.block_size))

        keyFolder = os.path.join(pendrive,"Key")
        os.makedirs(keyFolder,exist_ok=True)

        privateKeyPath = os.path.join(keyFolder, "encrypted_PK.bin")
        publicKeyPath = os.path.join(publicKeyPath, "public_key.pem")
        
        gui.after(DELAY_IN_MS*3, gui.setGenerationStatusLabelText, "Saving private key...")
        with open(privateKeyPath, "wb") as f:
            f.write(encryptedPrivateKey)

        gui.after(DELAY_IN_MS*4, gui.setGenerationStatusLabelText, "Saving public key...")
        with open(publicKeyPath, "wb") as f:
            f.write(publicKey)

        gui.after(DELAY_IN_MS*5, gui.setGenerationStatusLabelText, "Generation and saving succeeded!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
   


        
        
        




