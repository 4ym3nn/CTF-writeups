from math import gcd
import random

def encrypt(a, b):
    ct = []
    for ch in msg:
        if ch.isalpha():
            encrypted_char = chr(((a * (ord(ch) - 65 - b)) % 26) + 65)
            ct.append(encrypted_char)
        else :
            ct.append(ch)
    return ''.join(ct)


msg = open('secret_message.txt').read()

while True:
    a = random.randint(1, 26)
    b = random.randint(1, 26)
    if gcd(a, 26) == 1:
        break

with open('encrypted.txt', 'w') as f:
    f.write(encrypt(a,b))

print("Encrypted message saved to encrypted.txt")