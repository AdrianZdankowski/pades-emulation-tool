# Tool for Emulating the PAdES Qualified Electronic Signature

## 📖 Project overview

The main goal of the project is to realize a software tool for emulating the qualified electronic signature in accordance to the **PAdES (PDF Advanced Electronic Signature)** format. The primary task of the project is to design and develop an application that will allow to digitally sign PDF documents using RSA encryption. The private key is stored on a USB drive encrypted by the AES algorithm.

## 🛠️ Project features
- **Auxilliary application** for generating a **pair of RSA 4096-length keys**. Generated private key will be stored on the chosen **USB drive** and encrypted using **AES algorithm with SHA-256 key** that is the hash from 8 digit PIN provided by the user.
- **Main application** that allows the user to sign a PDF file in **PAdES** format with the encrypted private key stored on the USB drive that will be **automatically detected**. User has to input 8 digit PIN to decrypt the private key. The application also features **signature verification** by using the **public key**.
- Both applications feature an **user-friendly GUI** that displays application state (e.g. hardware detection, file paths, signing process status).
- Project is documented by **Doxygen** which provides full code documentation.

## 🧰 How to use the project

1. **Generate RSA key pair**:
    - Run the auxilliary application to generate a pair of RSA keys.
    - Input 8 digit PIN number that will be used to encrypt the private key.
    - Select an USB drive to store the private key and path to save the public key.
2. **Sign the PDF file**:
    - Insert the USB drive with the private key.
    - Run the main application and choose the PDF document you want to sign.
    - Input the 8 digit PIN number to decrypt the private key in order to begin the signig process.
3. **Verify the signature**:
    - Use the public key to verify the PDF document's signature. The application will check the integrity and authenticity of the document.

## 🚀 How to run the project

### 1. Install the [UV package and project manager](https://docs.astral.sh/uv/)
```bash
pip install uv
```

### 2. Install required dependencies and create the virtual environment

#### 🪟 On Windows:
```powershell
uv sync
venv\Scripts\activate
```
#### 🐧 On Linux:
```bash
uv sync
source venv/bin/activate
```

### 3. Run the auxiliary application
```bash
python -m auxiliary_application.main
```

### 4. Run the main application
```bash
python -m main_application.main
```


