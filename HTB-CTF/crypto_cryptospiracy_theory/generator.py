from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii, string


with open('password.txt') as pwd_file:
    pwd = pwd_file.read().strip()

# check printability
assert all(k in string.ascii_letters + string.digits for k in pwd)

pwd = pwd.encode()

if len(pwd) not in [16, 24, 32]:
    raise ValueError("Invalid AES key length. Key must be 16, 24, or 32 bytes long.")

with open('message.txt', 'r') as message_file:
    message = message_file.read().strip()  

words = message.split()

ciphertext = b""
cipher = AES.new(pwd, AES.MODE_ECB)

for word in words:
    word_padded = pad(word.encode(), AES.block_size)
    encrypted_word = cipher.encrypt(word_padded)
    ciphertext += encrypted_word


with open('encrypted_message.aes', 'wb') as file:
    file.write(ciphertext)

print("Encryption complete. Ciphertext saved to 'encrypted_message.aes'.")