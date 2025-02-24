from pwn import *
from params import *
from secret import SEED
from base64 import b64encode as be, b64decode as bd
import json

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


# context.log_level = 'debug'

l = listen(1337)
l.wait_for_connection()

lcg = LCG()
init = False

while True:
    cmd = input('/home/v1ctim/Desktop> ').encode()
    enc_cmd = lcg.encrypt(cmd)
    
    if init:
        uuid = lcg.generate_packet_uuid()
        l.sendline(json.dumps({'init': init, 'id': uuid[2:], 'cmd': be(enc_cmd).decode()}).encode())
    else:
        l.sendline(json.dumps({'init': init, 'cmd': be(enc_cmd).decode()}).encode())
        init = True

    if cmd == b'exit':
        l.close()
        break

    enc_out = bd(l.recvline())
    data = lcg.decrypt(enc_out)
    print(data)
    l.clean()