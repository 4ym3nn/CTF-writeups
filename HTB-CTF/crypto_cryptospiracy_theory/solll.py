from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import hashlib

# Function to pad plaintext to AES block size (16 bytes)
def pad_plaintext(plaintext):
    padder = padding.PKCS7(128).padder()  # 128 bits = 16 bytes
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    return padded_data

# Function to generate the AES key from a password
def generate_key(password):
    # SHA-256 is used here, and we take the first 16 bytes for AES-128
    key = password.encode()
    return key

# Function to encrypt plaintext with AES in ECB mode
def encrypt_with_aes_ecb(plaintext, key):
    padded_plaintext = pad_plaintext(plaintext)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ciphertext

# Given values
plaintext = "The"
password = "avengedsevenfold"
expected_ciphertext_hex = "fa7c7b06acf010ed961d2f1ef6caa73a"

# Generate key from password
key = generate_key(password)

# Encrypt plaintext with the generated key
ciphertext = encrypt_with_aes_ecb(plaintext, key)

# Check if the computed ciphertext matches the expected ciphertext
if ciphertext.hex() == expected_ciphertext_hex:
    print(f"Key derived from password '{password}' successfully matches the given ciphertext.")
else:
    print("Ciphertext does not match. There might be an issue.")
