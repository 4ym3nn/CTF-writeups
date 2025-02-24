
a = 0xa1d41ebef9c575ac113fcfd5ac8dbda9
b = 0x8dcf3cf766e0b6c30e753416a70e2367
m = 0x100000000000000000000000000000000
texts=[
    {'init': False, 'cmd': 'ocXzAq8Q'},
    {'init': True, 'id': 'eba14c429a64b2251717da016e096091', 'cmd': 'kn4='},
    {'init': True, 'id': 'efbb599758d1743333e5b43ac3e4e2b2', 'cmd': '2ulbTirRTzn+EKa1bvu3'},
    {'init': True, 'id': '79f5d45d89a17c81d9137e0481d59465', 'cmd': 'B3ljT4UTIVliEXzIoq8='},
    {'init': True, 'id': '8829affbed23334d34016095627ba065', 'cmd': '4FfTtXHCD3LuRRJzLIzwyeylqqGwyTiugfjOo+MbNhyKv1ZDgSL33Lwaysu+dlONfwJ8jaqbuTVnVqwFloEI4wGdC9FFkmJgLpV9y3AZyjM0wsV+DRVR1cpOBvQqT4F46j2JiDxvABDqHRw5yrmv+uByJMyX/cZM2azJMonAVwV95ncUg0uWs3bmpturCW9sWiVaQ2pqjgAuUDs3Yab1/jJa4tthhkJrBJl6cyX88ijWqoMBKUkjsZ/sNa8uGLpC9gGpafUQwfyaPfImxIx8taB8bain59NlaI2RaL3YFfRrkxQAw8rUshLbxqI/AhpOH9LRQ09GeORcBnHPC0HaqMFDgp0euCJzrnVhdDmPrPPGhq/MsfISmr3R94HfOE4hs/h4ceMywp+qHOLZ/1RlvVoSBrK5w7o4G16PJLC9Xf8UzC6rQO5PQBiOcpNgCPg7NvToEickQd7CTBWQOEy+Rv0ar8gnTAooy2cjMe2iqeuEMTOd5Pz8QKS721vcxU4AU4cLDbwhr4tKteb3v3oGcAEiPF9sSoMbBlhoE0m7+f8wLPHvXrgfShSKBD0L9vccz42AMCUZGu+Ctw2QASe5apAnvWz0c+u3rD3aG8aXZo+hF3K4u7rjRkulqm2B+mD9aeJiVb2zlah74L6iRW0MUR7PvXkXSnnaX2sW8E9Y3obSBo2gEqcQAqhLAlsu7Y3y9Jyc87LJEMSf/tmq/BBEFIjcXXWBBO3ys1rK3vFdb5pfND6ApIO/AEhRoguD/SDGCpkOqkjXYk8cgSWaTE3aMULyhCZwFlHsyVMS9CodoFvAbInIEjE+L8ptHDff6IbbkENz/83i7SOGitFn3epsL0fyQjWlA5CSdceb/opVJVUeVwdYbVO4DC9XTRtDivq3VkbI0WL3cHUqmXcmAKzcGMSV/xkMB2Th6vAq+xcYhhm8EoFxqXC14e00/0XlvXm0pkZngfmo0Gd0qqJYofA34HS/Miuy6deJd5u3mnMeUGsv6O9mZ3VlpAUTQtEJXJvbzXbB7j+VPhb3J2JRRs+a9N2Is8jyyRO3tI7kmskDPRyMx1pg4jH138wWyqOvfWXVcTE+qNa+gh4VUZkDsaNE9H2+E/dyx2tKH78htEtT0zkU5tIOCzFl19odAJUdGapWjjqZmEBYKzGIdRF53KLK9qdmPczHycB8uYqRdNbLZixO2lIshAmGh1yx8ZKVGD1/RgFdPiE9k1YxHGQXd5Lmvg=='},
    {'init': True, 'id': '1680383308c87fc16900ba6808998e03', 'cmd': 'kg4kSA=='}
]

from pwn import *
from base64 import b64encode as be, b64decode as bd
import json
for i in texts:
    try:
        state=int(i['id'],16)
    except:
        state=0xeba14c429a64b2251717da016e096091
    states=[]
    text=i['cmd']
    msg=bd(text)
    count=0;
    for j in range(32):
        for i in range(len(msg)):
            for k in range(j+1):
                prev_state = ((state - b) * pow(a, -1, m)) % m ;
            
            states.append(prev_state)
            state = prev_state
        key = []  # Initialize an empty list to store the byte values
        states=states[::-1]
        for i in states:
        # Use & 0xff to extract the last 8 bits of each value
            key.append(i & 0xff)
        key=bytes(key) 


        res=xor(msg,key)
        try:
            decoded = res.decode() 
            print(decoded)
        except:
            # print("not found",res)
            continue;
