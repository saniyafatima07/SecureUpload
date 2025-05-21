from flask import Flask, render_template, request, send_file
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os
import io

app = Flask(__name__)

def derive_key(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

@app.route('/', methods=['GET','POST'])

def index():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        passphrase = request.form.get('password')

        if uploaded_file and passphrase:
            salt = os.urandom(16)
            key = derive_key(passphrase, salt)
            fernet = Fernet(key)

            data = uploaded_file.read()
            encrypted_data = fernet.encrypt(data)

            final_data = salt + encrypted_data

            encrypted_output = io.BytesIO(final_data)
            encrypted_output.seek(0)

            filename = uploaded_file.filename + '.enc'
            return send_file(encrypted_output, as_attachment=True, download_name = filename)

    return render_template('index.html')

@app.route('/decrypt', methods=['GET','POST'])
def decrypt():
    if request.method == 'POST':
        enc_file = request.files.get('enc_file')
        passphrase = request.form.get('password')

        if enc_file and passphrase:
            encrypted_content = enc_file.read()
            salt = encrypted_content[:16]
            encrypted_data = encrypted_content[16:]

            key = derive_key(passphrase, salt)
            fernet = Fernet(key)

            try:
                decrypted_data = fernet.decrypt(encrypted_data)
            except Exception:
                return render_template('decrypt.html', error="Invalid passphrase or corrupted file! ")

            output = io.BytesIO(decrypted_data)
            output.seek(0)

            original_filename = enc_file.filename.replace('.enc','')
            return send_file(output, as_attachment=True, download_name='decrypted_' + original_filename)

    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(debug=True)