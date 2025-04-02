from cryptography.fernet import Fernet
import base64
import os

def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    try:
        with open('secret.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        return generate_key()

def encrypt_password(website, password):
    key = load_key()
    f = Fernet(key)
    
    encrypted_password = f.encrypt(password.encode())
    
    with open('passwords.enc', 'ab') as file:
        file.write(f"{website}:".encode() + encrypted_password + b'\n')

def decrypt_passwords():
    key = load_key()
    f = Fernet(key)
    try:
        with open('passwords.enc', 'rb') as file:
            passwords = []
            for line in file:
                website, encrypted_password = line.strip().split(b':', 1)
                decrypted_password = f.decrypt(encrypted_password).decode()
                passwords.append((website.decode(), decrypted_password))
            return passwords
    except FileNotFoundError:
        return [] 