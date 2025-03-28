from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

def verifyPin(pin, privateKey):
    try:
        iv = privateKey[:16] 
        cipherText = privateKey[16:]

        hashedPin = sha256(pin.encode()).digest()

        cipher = AES.new(hashedPin, AES.MODE_CBC, iv)
        
        decryptedPrivateKey = unpad(cipher.decrypt(cipherText), AES.block_size)

        if decryptedPrivateKey:
           return True
        else:
            return False
    except Exception as e:
        return False

