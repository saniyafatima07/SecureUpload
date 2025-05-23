# SecureUpload

This Flask web application allows users to securely encrypt and decrypt files using a passphrase. 
The encryption key is derived from the user-provided passphrase using PBKDF2 with a random salt, ensuring stronger security.

Users can:

- Upload a file and provide a passphrase to receive an encrypted version of the file.
- Decrypt an encrypted file by providing the same passphrase.

## Features

- Passphrase-based encryption key derivation using PBKDF2 with SHA-256.
- Random salt generation stored alongside the encrypted data.
- Fully secure as the original files and passphrase is not stored anywhere else.
- Encryption and decryption with Fernet symmetric encryption.
- File upload and download handled securely via Flask's cryptographic library.

## Disclaimer

Please remember your passphrase, as it is required to decrypt your file.
