pwd="avengedsevenfold"
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import string


# Encode the password to bytes
pwd = pwd.encode()

# Ensure that the key length is valid (16, 24, or 32 bytes)
if len(pwd) not in [16, 24, 32]:
    raise ValueError("Invalid AES key length. Key must be 16, 24, or 32 bytes long.")

# Read the encrypted ciphertext from the file
with open('encrypted_message.aes', 'rb') as encrypted_file:
    ciphertext = encrypted_file.read()

# Initialize the cipher for decryption using the same key and ECB mode
cipher = AES.new(pwd, AES.MODE_ECB)

# Decrypt the ciphertext
decrypted_padded = cipher.decrypt(ciphertext)

# Remove padding (the same block size used during encryption)
decrypted_message = unpad(decrypted_padded, AES.block_size)

# Decode the decrypted message (from bytes back to string)
decrypted_message_str = decrypted_message.decode()
decrypted_message_str=decrypted_message_str.replace(" ", "")
# Print the decrypted message
print("Decrypted Message:", decrypted_message_str)
