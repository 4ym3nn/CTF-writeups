from math import gcd

# Function to find modular inverse of a under modulo m
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None  # If no inverse exists

# Decrypt the message using the decryption formula
def decrypt(a, b, ct):
    msg = []
    a_inv = mod_inverse(a, 26)  # Find modular inverse of 'a' under mod 26
    
    if a_inv is None:
        return None  # If no modular inverse, skip this pair
    
    for ch in ct:
        if ch.isalpha():
            decrypted_char = chr(((a_inv * (ord(ch) - 65 - b)) % 26) + 65)
            msg.append(decrypted_char)
        else:
            msg.append(ch)
    
    return ''.join(msg)

# Brute-force all values of a and b
def brute_force_decrypt(ct):
    valid_a_values = [a for a in range(1, 26) if gcd(a, 26) == 1]
    valid_b_values = range(1, 26)
    
    for a in valid_a_values:
        for b in valid_b_values:
            decrypted_message = decrypt(a, b, ct)
            if decrypted_message :
                print(f"Found potential match with a={a}, b={b}:")
                print(decrypted_message)
                print("\n---\n")

# Example usage:
with open('encrypted.txt', 'r') as f:
    encrypted_message = f.read()

# Brute-force all (a, b) combinations and print possible decrypted messages containing 'HTB{'
brute_force_decrypt(encrypted_message)
