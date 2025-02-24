from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib

# Define guessed plaintext words
plaintext_words = ["The", "a", "flag"]

# Function to read passwords from a file and ignore comments
def read_passwords(file_path):
    passwords = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            # Ignore lines that start with '#' (comments)
            line = line.strip()
            if line and not line.startswith('#'):
                passwords.append(line)
    return passwords

# AES block size (16 bytes)
BLOCK_SIZE = 16

# Function to pad plaintext
def pad_plaintext(plaintext):
    padder = padding.PKCS7(BLOCK_SIZE * 8).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    return padded_data

# Function to generate a key from a password
def generate_key(password):
    # Use SHA-256 to derive a 16-byte key (AES-128)
    return (password.encode())

# Encrypt plaintext with a given key in ECB mode
def encrypt_with_ecb(padded_plaintext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ciphertext

# Output file for ciphertexts
output_file = "encrypted_texts_ecb.txt"

# Path to your passwords file (e.g., 'rockyou.txt')
passwords_file = "./filtered_passwords.txt"

# Read passwords from the file
passwords = read_passwords(passwords_file)

# Open file to save results
with open(output_file, "w") as outfile:
    for plaintext in plaintext_words:
        padded_plaintext = pad_plaintext(plaintext)
        for password in passwords:
            key = generate_key(password)
            ciphertext = encrypt_with_ecb(padded_plaintext, key)
            # Write results to the file
            
            outfile.write(f"Plaintext: {plaintext}, Password: {password}, Ciphertext: {ciphertext.hex()}\n")

print(f"Encrypted results (ECB mode) written to {output_file}.")
