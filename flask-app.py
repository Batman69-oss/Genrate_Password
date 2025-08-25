import os
import subprocess
import secrets
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ask-her', methods=['GET', 'POST'])
def ask_her():
    if request.method == 'GET':
        question = request.args.get('question', 'What do you want to ask her?')
        return jsonify({'response': f'She heard your GET and replies: "{question}"'})
    else:
        data = request.get_json()
        question = data.get('question', 'No question provided')
        return jsonify({'response': f'She received your POST and replies: "{question}"'})

@app.route('/generate-password', methods=['GET'])
def generate_password():
    length = int(request.args.get('length', 16))
    password = secrets.token_urlsafe(length)
    return jsonify({'password': password})

@app.route('/create-cert', methods=['POST'])
def create_cert():
    data = request.get_json()
    cert_name = data.get('name', 'mycert')
    
    # Filenames
    key_file = f"{cert_name}.key"
    cert_file = f"{cert_name}.crt"
    p12_file = f"{cert_name}.p12"

    # Generate private key and certificate
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-keyout', key_file,
                    '-out', cert_file, '-days', '365', '-nodes',
                    '-subj', '/CN=localhost'])

    # Convert to .p12 format
    subprocess.run(['openssl', 'pkcs12', '-export', '-out', p12_file,
                    '-inkey', key_file, '-in', cert_file,
                    '-password', 'pass:password123'])

    return jsonify({'status': 'Certificate created', 'files': [key_file, cert_file, p12_file]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
