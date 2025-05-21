from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.config['Upload_Folder'] = 'uploads'
app.config['Encrypted_Folder'] = 'encrypted'

os.makedirs(app.config['Upload_Folder'], exist_ok=True)
os.makedirs(app.config['Encrypted_Folder'], exist_ok=True)

@app.route('/', methods=['GET','POST'])

def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        password = request.form['password']

        if uploaded_file and password:
            file_path = os.path.join(app.config['Upload_Folder'], uploaded_file.filename)
            uploaded_file.save(file_path)

            with open(file_path, 'rb') as f:
                data = f.read()

            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)

            encrypted_path = os.path.join(app.config['Encrypted_Folder'], uploaded_file.filename + '.enc')
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data) 

            key_filename = uploaded_file.filename + '_key.txt'
            key_path = os.path.join(app.config['Encrypted_Folder'], key_filename)
            
            with open(key_path, 'wb') as key_file:
                key_file.write(key)

            return send_file(key_path, as_attachment=True)
    return render_template('index.html')

@app.route('/decrypt', methods=['GET','POST'])
def decrypt():
    if request.method == 'POST':
        enc_file = request.files['enc_file']
        key_file = request.files['key_file']

        if enc_file and key_file:
            encrypted_path = os.path.join(app.config['Encrypted_Folder'], enc_file.filename)
            enc_file.save(encrypted_path)

            key = key_file.read()
            fernet = Fernet(key)

            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()

            try:
                decrypted_data = fernet.decrypt(encrypted_data)
            except Exception:
                return render_template('decrypt.html',error="Invalid key or corrupted file!")

            original_filename = enc_file.filename.replace('.enc', '')
            decrypted_path = os.path.join(app.config['Upload_Folder'], 'decrypted_' + original_filename)

            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_data)

            return send_file(decrypted_path, as_attachment=True)

    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(debug=True)