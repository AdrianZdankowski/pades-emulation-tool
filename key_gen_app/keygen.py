from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from hashlib import sha256
import os


def GenerateAndSaveKeys(pin, pendrive):
    pseudoRandomGenerator = get_random_bytes
    hashedPin = sha256(pin.encode()).digest()
    key = RSA.generate(4096, randfunc=pseudoRandomGenerator)
    privateKey = key.export_key()
    publicKey = key.public_key().export_key()

    cipher = AES.new(hashedPin, AES.MODE_CBC)
    iv = cipher.iv
    encryptedPrivateKey = iv + cipher.encrypt(pad(privateKey, AES.block_size))

    keyFolder = os.path.join(pendrive,"Key")
    os.makedirs(keyFolder,exist_ok=True)

    privateKeyPath = os.path.join(keyFolder, "encrypted_PK.bin")
    
    with open(privateKeyPath, "wb") as f:
        f.write(encryptedPrivateKey)

   


        
        
        




