# SecureUpload

This Flask web application allows users to securely encrypt and decrypt files using a passphrase. 
The encryption key is derived from the user-provided passphrase using PBKDF2 with a random salt, ensuring stronger security.

Users can:

- Upload a file and provide a passphrase to receive an encrypted version of the file.
- Decrypt an encrypted file by providing the same passphrase.

## Getting Started 

### Prerequisites
- Python 3.8+
- pip

### SetUp 

**1. Clone the Repository:**
```bash
git clone https://github.com/saniyafatima07/SecureUpload.git
```

**2. Direct to the repository:**
```bash
cd SecureUpload
```

**3. Create virtual environment:**
```bash
python3 -m venv venv
```

**3. Activate virtual environment:**

Linux/macOS:
```bash
source venv/bin/activate
```
Windows:
```bash
.\venv\Scripts\Activate
```
**4. Install dependencies:**
```bash
pip install -r requirements.txt
```

**5. Run the application**
```bash
python app.py
```
Once the application is running, open your browser and navigate to: http://127.0.0.1:5000/



## Features

- Passphrase-based encryption key derivation using PBKDF2 with SHA-256.
- Random salt generation stored alongside the encrypted data.
- Fully secure as the original files and passphrase is not stored anywhere else.
- Encryption and decryption with Fernet symmetric encryption.
- File upload and download handled securely via Flask's cryptographic library.

## Disclaimer

Please remember your passphrase, as it is required to decrypt your file.

