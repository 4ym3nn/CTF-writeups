---
layout: default
---
# smileyCTF2025 - rev Challenge: dna
## Flag : .;,;.{we_ought_to_start_storing_our_data_as_dna_instead}

# Description
deoxy ribo nucleic acid deoxy meaning without oxygen ribo meaning the 5-carbon sugar backbone nucleic meaning of the nucleus acid meaning proton donor

# Solution
## Initial Recon

We start by looking at the challenge directory:
```
➜  dna ls
main.cpython-310.pyc  vm.dna
➜  dna 
```
We can see that this is a virtual machine challenge, and the Python code has been compiled with Python 3.10 into a .pyc file ,Before diving into the challenge, let's take a moment to understand what a virtual machine (VM) is.

### What Is A VM?

VM is short form of Virtual Machine. A virtual machine is exactly what it’s name is, it’s virtual!.

An example of physical machine is your CPU. Your CPU is executing real instructions. When you do a mov instruction, your CPU will take minimum number of steps to complete that instruction. That instruction will have effect on real registers and memory.

When it comes to a virtual CPU (machine), it may or may not have a move instruction in the first place! Even if it has a mov instruction, it’ll be moving data to/from variables declared within the program. So the virtual cpu doesn’t directly use anything real (registers/memory) and all the resources that it’ll use will be stored in a variable that is already allocated on either the stack or the heap. All the (virtual) instructions that a virtual machine will run will ultimately be converted to machine code. Because of this conversion, a virtual CPU takes much more number of steps than a physical CPU to execute a single (virtual) instruction and because of this, virtual machines are slower too.

### How Do Virtual Machines Work?

Since a virtual machine is trying to emulate some new instruction set, it’ll need to have a CPU that will be able to decode those set of instructions and for that all virtual machines implement their own virtual CPU. How do we do that? Well, a CPU is just a bunch of registers and some helper units.
!(vm)[./abasiccomputer.gif] 
A virtual CPU is much similar to a physical CPU. It’ll have it’s own set of registers and cache and all. A simple implementation in code will look something like this
```python
class RegID(IntEnum):
    RAX = 0
    RBX = 1
    RCX = 2
    # Add other registers as needed


class CPU:
    def __init__(self, num_registers: int, code_size: int):
        self.registers: List[int] = [0] * num_registers  # X registers
        self.stack: List[int] = []

        self.pc: int = 0  # Program counter
        self.bytecode: List[int] = [0] * code_size
        self.code_sz: int = code_size
        # Additional VM components can go here
        # e.g., flags, memory, etc.
```
This makes up the structure of our CPU, but then how will it execute instructions? Normally, challenge developers write their program in a symbolic language and then convert it to the virtual CPUs assembly code. This assembled code is what we refer to as the bytecode. It’s just an array of numbers like the opcodes of your actual CPU.

This bytecode is then read and passed to a Fetch, Decode, Execute (FeDeX) loop. This loop does what it’s name is. It fetches the current instruction from bytecode, decodes what it means (useful part) and then executes it! This is very much similar to what an actual CPU does but this decoding part makes up the extra steps that our virtual CPU has to take.
### The FeDeX Loop

In normal CPU, there is a register called the program counter (instruction pointer in Intel CPUs). This register contains an absolute address or an offset from a base address that directly or indirectly points to the next instruction that needs to be executed. So, the fetch part just needs to keep track of this program counter. To fetch the next instruction, the program will do

```python
while pc < len(code):
    opcode, operand = map(trans, [code[pc:pc + 2], code[pc + 2:pc + 12]])
    # fetch current instruction 
    match opcode:
        # decode
        case 0:
            # execute
            s.append(operand)
            pc += 12
```
this is where the interesting part comes : In all normal, not crazy VMs you’ll find a FeDeX loop like this one. This function is what we need to find if it’s a VM challenge. Generally it’s easy to find because of the code structure here! When you’ll see this code in a graph like format, you’ll notice that almost all similar VMs (with a FeDeX loop) will have similar structure. Let’s try that in this crackme.

### Starting with the Challenge

To decompile the .pyc file back into Python source code, I used pylingual.io.
and this was the result :
```python
# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: main.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 2025-06-06 03:24:45 UTC (1749180285)

import marshal
import sys
s = []
m = {}
nm = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
unlucky = [b'\x8coooooooooooonooolooo,ooo\x9cSooo\x06o\x12o\x1bo\x0bnvo\x13o\x0bmSo\x1bo\x0blvo\x13o\x0bnSo\x1bo\x0bkvo\x13o\x0blSo\x1bo\x0bmvo\x13o\x0bkSo\x13o\x0eo\x0bo<oFj!\xb5n;\xb5n.\xb5n(\xb5n,\xc6n\xb5m\x01\x02\xc6n\xb5l\x1b\x02\x1f\xc6o\x1deooo\x95fS\x1a\x01\x03\x1a\x0c\x04\x16Q\xb5h\x1a\x01\x03\x1a\x0c\x04\x16booo\x9ccoookmcncncncngn', b'\x96uuuuuuuuuuuuruuu}uuu6uuu\x86\x11uuu\x11t\x08u\x11w\x08t\x11v\x08w\x11q\x11p\xf1u\tu1u\xf6t\x08v\tu\tt\tw\x13v1u(n\x08q\x01u\x01t\x01w\xd5v\xd4u\xf6t\xf6t1u(e)w\x08p\x08s\tv\tspulu\x01w\tq\tpluluMuvuIu\x04i\x04g\tv\x14w\x11u&u\\s;\xafq426!\xafq!642\xafq6!24\x16tuuuuuuuuuuuwuuusuuu&uuu\x86ouuu\x1cu\tu(|\x08t\tt\x01u\x01t\xd5w\xd4u\xf6t\xe6w\x04w&u\\u\xdcv\xafv\x06\x00\x18\xafw\x1b\x18\xafs\x03\x14\x19\x00\x10\x06\xdcw\xafw[E\xaft\x16\xdcu\x07xuuu\x8f|I\x00\x1b\x19\x00\x16\x1e\x0cK\xafr\x00\x1b\x19\x00\x16\x1e\x0cnuuu\x86wuuuou\x8fh\x00\x1b\x19\x00\x16\x1e\x0c*G[I\x19\x1a\x16\x14\x19\x06K[I\x11\x1c\x16\x01\x16\x1a\x18\x05K\xdcq\xaf|\x10\x1b\x00\x18\x10\x07\x14\x01\x10\xafs\x06\x1a\x07\x01\x10\x11\x07}uuu\xafq\x1e\x10\x0c\x06\xdcr\xafw\x06D\xafw\x06G\xafw\x06F\xafv\x01\x18\x05\xaft\x06\xaft\x1c\x07yuuu\x07xuuu\x07xuuu\x07{uuu\x07zuuucuuu\x86guuuqwqtqt{t{tmtotw\x8a}w', b"\x8aiiiiiiiiiiiihiiiniiijiii\x9a/iii\x1di\rh\xeah\xe0i\xe1i\xc9h\x1di\rk\xeah\xc9k\rj\rm\xedi\x1dj\xc9m\xc8i\xc8k\xc8hhi.i\xeei\x0fh\rl\ro\xeda\ro\x1dl\xeaj\x14i\x15i\x1dj\xeah\x08j\ri:i@n'\xb3o\x1b\x08\x07\r\x06\x04\xb3`\x0f\x1c\x07\n\x1d\x06\x06\x05\x1a\nkiiiiiiiiiiikiiikiii:iii\x9aaiii\x15i\x15h(i:i@h'\xc0i\xc0k\xb3h\x11\xb3h\x10\x1bliii\x1bliii\x93`U\x1c\x07\x05\x1c\n\x02\x10W\xb3n\x1c\x07\x05\x1c\n\x02\x10Miii\x9akiiiai\x93r\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWGU\x05\x08\x04\x0b\r\x08W\niiiiiiiiiiiiiiiijiiiiiii\x9aCiii\x0ci3h\ri3k\xeei\xeeh\x0fk\rh\rk\xeda3j\xeei\x0fh\rj\rm\xeda3m\xeeimi3l:i@l\x93s\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10\nkiiiiiiiiiiimiiiliiiziii\x9a-iii\x1di\xeai\xc9h\x15h\xc8hhi\x1dk\rh\xeah\x14k\xe1h\xc9j\x15k\xc8hhi\x1dm\rk\xeah-i4e\x14j\x15h\x15k\x15jpipi\x15i\rh\x15jpiUi\x18z\ri:i@j'\xb3m(*.=\x80miii\xc0l\xb3l\x1a\x1c\x19\x0c\x1b\xb3a66\x00\x07\x00\x1d66\xb3m\x05\x00\x1a\x1d\xb3n\x1a\x01\x1c\x0f\x0f\x05\x0c\xb3l\x1b\x08\x07\x0e\x0c\xc0m\xb3m\x1a\x0c\x05\x0f\xb3n\x04\x08\x19\x19\x00\x07\x0e\xb3m\x02\x0c\x10\x1a\xb3h\x00\xc0k\xb3`66\n\x05\x08\x1a\x1a66\xb3h\x1b\x1bliii\x1b`iii\x1bciiiOiii\x9aeiiiehahcheh\x7fhm\x96\x93J\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10G66\x00\x07\x00\x1d66\nkiiiiiiiiiiiliiiliiiziii\x9a;iii\x1di\rh\xeah\x14k\x1di\rk\xeah\x14j`i\x15k\xc9h\rm\xc8h\x14m\x1dk\xeei\x0fh\rl\ro\xeda\x15j\xc9j\x15m\xc8h\xc9m\xc8i\ri\rn\xeckpi-i\xeah\xeah\x1bA\x1dl\xeai\xc9o\xe1i\xc8h:i\x18`@a'\x1bkiii\xb3n\x01\x08\x1a\x01\x05\x00\x0b=\x80Iiii\nhiiiiiiiiiiikiiimiiiZiii\x9auiii\xe8i\x15i4`\x14h\x15h\x1di\xe1i\xeah\x02k?ihi\x18k\ri:i@h'\xc0h\xb3j\x06\x1b\r\xc0k\xb3kGY\x1bniii\xc0h\xb3j\x02\x0c\x10\x1bliii\x1b`iii\x1bciii[iii\x9amiiik\xe9si\x93P\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10G66\x0e\x0c\x1d\x00\x1d\x0c\x0466GU\x05\x06\n\x08\x05\x1aWGU\x0e\x0c\x07\x0c\x11\x19\x1bW\x80hiii\xc0n\xb3c66\x00\x04\x19\x06\x1b\x1d66\xb3`\x1b\x08\x07\r\x0b\x10\x1d\x0c\x1a\xb3j\x08\x05\x05\xb3o\x1a\x01\x08[\\_\xb3o\r\x00\x0e\x0c\x1a\x1d\x1bziii\xb3b66\x0e\x0c\x1d\x00\x1d\x0c\x0466\xc0l\x1bpiii\x1bBiii\xb3m\x01\x05\x00\x0b\xb3m\x1b\x05\x00\x0b\xb3h\x0b\xc0h\x1bwiii\x1bCiii\x1b`iii\x1bciiiDiii\x9agiiiahahkhchAhehk\x94\x93O\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10G66\x0e\x0c\x1d\x00\x1d\x0c\x0466\xc0o\xb3a66\x07\x08\x04\x0c66\xb3c66\x04\x06\r\x1c\x05\x0c66\xb3e66\x18\x1c\x08\x05\x07\x08\x04\x0c66\x1b}iii\x1b\\iii\xb3d66\n\x05\x08\x1a\x1a\n\x0c\x05\x0566\x1bliii\xc0h\x1bviii\x1bSiii\x1b`iii\x1bciiiLiii\x9aoiiiaigh}n\x1bciii\xc0o\x1bYiii\xb3m\x1a\x0c\x0c\r\xb3o\x1b\x0c\r\x1c\n\x0c\xb3k\x07\x04\xb3o\x1f\x08\x05\x1c\x0c\x1a\xb3m\r\x00\n\x1d\xc0h\x1bciii\x1bliii\x1b+iii\x1b`iii\x1bciiiHiii\x9aaiiiakwh}hey", b'\x82aaaaaaaaaaaacaaagaaa"aaa\x92]aaa&a\x05`\x05c\xe5a\x05c\x15a\xe2b\x1ca&a\x05b\x05e\xe5a\x05e\x15`\x1da\x05d\xece\x1c`\x15c\x05g\x15`\x15b\xe2`\xfaa\x05f\xfcb\xe2``a\x05a2aHi/\x02aaaaaaaaaaaaaaaabaaaaaaa\x92Iaaa\x04a;`\x05a;c\xe6a\x07`\x05`\x05c\xe5i;b\xe6a\x07`\x05b\x05e\xe5i;e\xe6aea;d2aHd\x9bt\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,,\x02eaaaaaaaaaaaeaaagaaaraaa\x92saaa\x15a\xe2a\xc1`\x1da\x1d`\x1dc\x1db\xc0e2aH`/\xc8c\xbbd\x12\x14\x11\x04\x13\xbbf>>\x0f\x04\x16>>\xc8e\xbbb\x02\r\x12\xbbe\x0f\x00\x0c\x04\xbbd\x03\x00\x12\x04\x12\xbbb\x05\x02\x15\xc8`\xbbh>>\x02\r\x00\x12\x12>>\xc8a\x9bh]\x14\x0f\r\x14\x02\n\x18_\xbbf\x14\x0f\r\x14\x02\n\x18Zaaa\x92caaas`\x9b|\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,,O>>\x0f\x04\x16>>\x02`aaaaaaaaaaafaaadaaa~aaa\x92\x05aaa\x15a\xe2a\x0b`\x1d`\x08a\x1dc\xc5`\xef`\x1cb\x15c\x1db\xc1b\xc0a\xe2`\x1ce\x1de\x05a\x05a\x05`\xe4bxa\x1de\x05c\x05a\x05`\xe4bxava\x1ce\x15e\x15d\x1db\xc1g\xc0a\xe2`\xe2`%a<k=c\x1cd\x1cg\x1de\x1ddxa\x1db\x1dg]a\x10D\x1db2aHb/\x88caaa\x88`aaa\xc8f\x13gaaa\xbbi>>\x02\x00\r\r>>\xbbe\r\x08\x12\x15\xbbg\x17\x00\r\x14\x04\x12\xbbh\x04\x0f\x14\x0c\x04\x13\x00\x15\x04\xbbg\x12\x0e\x13\x15\x04\x05\xbbe\n\x04\x18\x12\xc8f\x13haaa\xbbe\x00\x13\x06\x12\xbbg\n\x16\x00\x13\x06\x12\xbbi\x08\x0f\x12\x15\x00\x0f\x02\x04\xbbe\x17\x00\r\x12\xbb`\x08\xbb`\n\x13laaa\x13naaa\x13qaaa\x13paaa_aaa\x92maaas`m`}`y`o`e`\x9b\x7f\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,,O>>\x02\x00\r\r>>\xc8g\xbbi>>\x0f\x00\x0c\x04>>\xbbk>>\x0c\x0e\x05\x14\r\x04>>\xbbm>>\x10\x14\x00\r\x0f\x00\x0c\x04>>\x13faaa\x13yaaa\xbbl>>\x02\r\x00\x12\x12\x02\x04\r\r>>\x13naaa\x13naaa\x13laaa\x13qaaa\x13paaa[aaa\x92gaaaiam`ub\xbbc,,\x02aaaaaaaaaaaaaaaa`aaa!aaa\x92maaa\x04a;`\x05a;c\x05`2aHc\x9bt\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,%/\xc8b\x13Iaaa\x13Haaa\x13Kaaa\x13naaa\x13naaa\x13naaa\x13qaaa\x13paaa\'aaa\x92eaaaiae`\xbbc,%\xc8`\xbbh\x0c\x04\x15\x00\x02\r\x00\x12\x12\x9b@\x06\r\x0e\x03\x00\r\x12IH:F\x0f\x14\x02\r\x04\x0e\x15\x08\x05\x04>\x0c\x00\x11F<A\\A,%I\x9b`H\xc8e\xbbe\x15\x18\x11\x04\xbbe\x05\x08\x02\x15\xbbe\x04\x19\x04\x02\xbbc\x0f\x0c\xc8c\x13Laaa\x13Saaa\x13naaa\x13naaa\x13qaaa\x13paaaVaaa\x92gaaaqbumyb']
trans = lambda s: sum((nm[c] << 2 * i for i, c in enumerate(s)))
if len(sys.argv)!= 2:
    print(f'Usage: {sys.argv[0]} <dna_file>')
    sys.exit(1)
code = open(sys.argv[1]).read()
flag = input('> ').encode()
if len(flag)!= 56:
    exit('WRONG!')
if flag[:6]!= b'.;,;.{':
    exit('WRONG!')
if flag[(-1)]!= 125:
    exit('WRONG!')
flag = flag[6:(-1)]
for i in range(len(flag)):
    m[640 + i] = flag[i]
pc = 0

while pc < len(code):
    opcode, operand = map(trans, [code[pc:pc + 2], code[pc + 2:pc + 12]])
    match opcode:
        case 0: 
            s.append(operand)
            pc += 12
        case 1:
            if not s:
                raise Exception('Stack underflow')
            s.pop()
            pc += 2
        case 2:
        
            if operand not in m:
                raise Exception(f'Uninitialized memory access at {operand}')
            s.append(m[operand])
            pc += 12
        case 3: 
            if not s:
                raise Exception('Stack underflow')
            m[operand] = s.pop()
            pc += 12
        case 4: 
            if len(s) < 2:
                raise Exception('Stack underflow')
            a, b = (s.pop(), s.pop())
            s.append(a + b)
            pc += 2
        case 5:
            if len(s) < 2:
                raise Exception('Stack underflow')
            a, b = (s.pop(), s.pop())
            s.append(b - a)
            pc += 2
        case 6:
            if len(s) < 2:
                raise Exception('Stack underflow')
            a, b = (s.pop(), s.pop())
            s.append(a * b)
            pc += 2
        case 7:
            if len(s) < 2:
                raise Exception('Stack underflow')
            a, b = (s.pop(), s.pop())
            if a == 0:
                raise Exception('Division by zero')
            s.append(b % a)
            pc += 2
        case 8:
            if len(s) < 2:
                raise Exception('Stack underflow')
            a, b = (s.pop(), s.pop())
            print(a);print(b)
            s.append(1 if a == b else 0)
            pc += 2
        case 9:
            pc = operand
        case 10:
            if not s:
                raise Exception('Stack underflow')
            if s.pop() == 1:
                pc = operand
            else:  
                pc += 12
        case 11:
            if not s:
                raise Exception('Stack underflow')
            if s.pop()!= 1:
                pc = operand
            else:  # inserted
                pc += 12
        case 12:
            if not s:
                raise Exception('Stack underflow')
            opcodent(chr(s.pop()), end='')
            pc += 2
        case 13:
            if not s:
                raise Exception('Stack underflow')
            key = s.pop()
            print(m[666])
            print(f'Key: {key}')
            def f():
                return
            f.__code__ = marshal.loads(bytes([b ^ key for b in unlucky.pop(0)]))
            f()
            pc += 2
        case 14:
            if len(s) < 2:
                raise Exception('Stack underflow')
            a, b = (s.pop(), s.pop())
            if a not in nm or b not in nm:
                raise Exception('Invalid')
            nm[a], nm[b] = (nm[b], nm[a])
            pc += 2
        case 15:
            break
```

### Virtual Machine Overview

The code defines two key data structures:

    s: An array used internally by the VM (we’ll understand its purpose later).

    m: A dictionary that serves as memory for the virtual machine.

DNA Code Representation

The virtual machine reads a DNA-like string from a file, which consists only of the characters {A, T, G, C}. Here's an example:

```GAAAAGGAAAAAAAGGGTAAAAAAGTGATAAGGAAAAAAACGTAAAAAAAGTGAGAAGGAAAAAAAACAGAAAAAAGTGACAAGGAAAAAAAGGAGAAAAAAGTGAATAGGAAAAAAAACGTAAAAAA...```

To decode these characters into numbers, a simple base-4 mapping is used:
```python
nm = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
```
This mapping turns each DNA character into a digit between 0 and 3.
DNA to Integer Conversion

The VM uses the following trans lambda function to convert short DNA strings into integers:
```python
trans = lambda s: sum((nm[c] << 2 * i for i, c in enumerate(s)))
```
This treats the DNA string as a little-endian base-4 number.

Example:
```python

trans('AT') = (0 << 0) + (1 << 2) = 0 + 4 = 4
```
The unlucky List

The code defines an unlucky list of four byte strings. These likely contain encrypted or obfuscated data used later in the VM's logic.
```python

unlucky = [
    b'...',  # Placeholder for large byte strings
    b'...',
    b'...',
    b'...'
]
```
Input Validation and Setup

The program expects a DNA code file as an argument. It reads the file and prompts the user for a flag.
```python

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <dna_file>')
    sys.exit(1)

code = open(sys.argv[1]).read()
flag = input('> ').encode()
```
Flag Validation

The flag must meet strict format requirements:
```python

if len(flag) != 56:
    exit('WRONG!')

if flag[:6] != b'.;,;.{':
    exit('WRONG!')

if flag[-1] != 125:  # ASCII code for '}'
    exit('WRONG!')
```
After validation, the wrapper format is stripped, leaving 49 bytes of core flag data:
```python

flag = flag[6:-1]
```
Storing the Flag in VM Memory

Each byte of the flag is stored in the virtual memory dictionary m, starting at address 640:
```python

for i in range(len(flag)):
    m[640 + i] = flag[i]
```

#### Beginning Execution

The virtual machine sets the program counter (pc) to 0 and begins a decode-execute loop:
```python
pc = 0

while pc < len(code):
    # Each instruction is 12 DNA characters:
    #   - First 2 characters: opcode
    #   - Next 10 characters: operand
    opcode, operand = map(trans, [code[pc:pc + 2], code[pc + 2:pc + 12]])
    ...
```
####  Opcode Interpretation

##### PUSH — Opcode 0
```python

case 0:  # PUSH
    # Push operand onto the stack
    s.append(operand)
    pc += 12
```
##### POP — Opcode 1
```python

case 1:  # POP
    # Remove the top element from the stack
    if not s:
        raise Exception('Stack underflow')
    s.pop()
    pc += 2
```
##### LOAD — Opcode 2
```python

case 2:  # LOAD from memory
    # Push value at memory[operand] onto the stack
    if operand not in m:
        raise Exception(f'Uninitialized memory access at {operand}')
    s.append(m[operand])
    pc += 12
```
##### STORE — Opcode 3
```python

case 3:  # STORE to memory
    # Pop top of stack and store at memory[operand]
    if not s:
        raise Exception('Stack underflow')
    m[operand] = s.pop()
    pc += 12
```
##### ADD — Opcode 4
```python

case 4:  # ADD
    # Pop two values, push their sum
    if len(s) < 2:
        raise Exception('Stack underflow')
    a, b = s.pop(), s.pop()
    s.append(a + b)
    pc += 2
```
##### SUB — Opcode 5
```python

case 5:  # SUB
    # Pop two values, push b - a
    if len(s) < 2:
        raise Exception('Stack underflow')
    a, b = s.pop(), s.pop()
    s.append(b - a)
    pc += 2
```
##### MUL — Opcode 6
```python

case 6:  # MUL
    # Pop two values, push their product
    if len(s) < 2:
        raise Exception('Stack underflow')
    a, b = s.pop(), s.pop()
    s.append(a * b)
    pc += 2
```
##### MOD — Opcode 7
```python
case 7:  # MOD
    # Pop two values, push b % a (a must not be 0)
    if len(s) < 2:
        raise Exception('Stack underflow')
    a, b = s.pop(), s.pop()
    if a == 0:
        raise Exception('Division by zero')
    s.append(b % a)
    pc += 2
```
##### EQUAL — Opcode 8
```python
case 8:  # EQUAL
    # Push 1 if a == b else 0
    if len(s) < 2:
        raise Exception('Stack underflow')
    a, b = s.pop(), s.pop()
    print(a)
    print(b)
    s.append(1 if a == b else 0)
    pc += 2
```
##### JMP — Opcode 9
```python

case 9:  # JMP
    # Unconditional jump to address `operand`
    pc = operand
```
##### JMP_IF_EQ_1 — Opcode 10
```python

case 10:  # JMP_IF_EQ_1
    # Conditional jump if top of stack == 1
    if not s:
        raise Exception('Stack underflow')
    if s.pop() == 1:
        pc = operand
    else:
        pc += 12
```
##### JMP_IF_NEQ_1 — Opcode 11
```python

case 11:  # JMP_IF_NEQ_1
    # Conditional jump if top of stack != 1
    if not s:
        raise Exception('Stack underflow')
    if s.pop() != 1:
        pc = operand
    else:
        pc += 12
```
##### PRINT — Opcode 12
```python

case 12:  # PRINT
    # Print character from top of stack
    if not s:
        raise Exception('Stack underflow')
    print(chr(s.pop()), end='')
    pc += 2
```
##### CALL_SNIPPET — Opcode 13
```python

case 13:  # CALL_SNIPPET
    # Decrypt and execute marshaled code from 'unlucky' list
    if not s:
        raise Exception('Stack underflow')
    key = s.pop()
    def f(): return
    f.__code__ = marshal.loads(bytes([b ^ key for b in unlucky.pop(0)]))
    f()
    pc += 2
```
##### SWAP — Opcode 14
```python

case 14:  # SWAP
    # Swap values in the nm (DNA map)
    if len(s) < 2:
        raise Exception('Stack underflow')
    a, b = s.pop(), s.pop()
    if a not in nm or b not in nm:
        raise Exception('Invalid swap keys')
    nm[a], nm[b] = nm[b], nm[a]
    pc += 2
```
##### HALT — Opcode 15
```python
case 15:  # HALT
    # Stop execution
    break
```
For a while, I thought the main challenge was to reverse-engineer the virtual machine (VM) itself. So I ran the VM (v1.py) using Python 3.10 and provided a flag input of length 56, as required.

###  Error Trace

```shell
(venv) ➔  dna python3 v1.py vm.dna
> .;.,;{the_secret_dna_koy_is_hiooon_horo_1234567890123aa}
Traceback (most recent call last):
  File "/mnt/default-linux/CTFS/smiley/chall1/dna/v1.py", line 116, in <module>
    f.__code__ = marshal.loads(bytes([b ^ key for b in unlucky.pop(0)]))
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: bad marshal data (unknown type code)
(venv) ➔  dna
```

---

###  Key Extraction

I printed the XOR key using:

```python
key = s.pop()
print(f'Key: {key}')
def f():
    return
f.__code__ = marshal.loads(bytes([b ^ key for b in unlucky.pop(0)]))
f()
pc += 2
```

**Result:**

```
Key: 101
```
which is
```" .;.,;{the_secret_dna_key_is_hidden_here_1234567890123aa}"[26+6]===chr(101)=="o"```
--- 

### Analysis

* `s.pop()` equals `101` (which comes from `m[666]`)
* In assembler version 0, the first call where the error happens is:

```
015202: LOAD_MEM        Operand=666
015214: CALL_SNIPPET
```

* `LOAD_MEM` performs: `s.append(m[666])`
* Then `CALL_SNIPPET` does: `key = s.pop()` → which equals `m[666]` (our input `flag[26]`)

---

### Brute Force Approach

Since the key XORs `flag[26]` with `unlucky[0]` byte-by-byte, and the key range is 0–255 (`2^8`), we can brute-force the correct key:

```python
for key in range(256):
    decrypted = bytes([b ^ key for b in blob])
    try:
        obj = marshal.loads(decrypted)
    except Exception:
        continue
    print(f"Key {key}: loaded type {type(obj)}; value/obj: {obj!r}")
    if isinstance(obj, types.CodeType):
        dis.dis(obj)
```
and the correct key was  111 which is "o" for unluck[0] i updated flag[26] to "o" and got the same error here i understand that i should do that with all unluck list starting from the begining with order because it pops the first element always after bruteforcing the keys i found this python machine code 

### Decompiled Python Code from `unlucky` Bytecode

#### unlucky[0]
**Python Bytecode:**
```python
    15           0 BUILD_MAP                0
                             2 STORE_FAST               0 (tmp)

    16           4 LOAD_GLOBAL              0 (nm)
                             6 LOAD_CONST               1 ('T')
                             8 BINARY_SUBSCR
                            10 LOAD_FAST                0 (tmp)
                            12 LOAD_CONST               2 ('A')
                            14 STORE_SUBSCR

    17          16 LOAD_GLOBAL              0 (nm)
                            18 LOAD_CONST               3 ('G')
                            20 BINARY_SUBSCR
                            22 LOAD_FAST                0 (tmp)
                            24 LOAD_CONST               1 ('T')
                            26 STORE_SUBSCR

    18          28 LOAD_GLOBAL              0 (nm)
                            30 LOAD_CONST               4 ('C')
                            32 BINARY_SUBSCR
                            34 LOAD_FAST                0 (tmp)
                            36 LOAD_CONST               3 ('G')
                            38 STORE_SUBSCR

    19          40 LOAD_GLOBAL              0 (nm)
                            42 LOAD_CONST               2 ('A')
                            44 BINARY_SUBSCR
                            46 LOAD_FAST                0 (tmp)
                            48 LOAD_CONST               4 ('C')
                            50 STORE_SUBSCR

    20          52 LOAD_FAST                0 (tmp)
                            54 STORE_GLOBAL             0 (nm)
                            56 LOAD_CONST               0 (None)
                            58 RETURN_VALUE
```

**Decompiled Python Code:**
```python
def unlucky0(nm_in):
        tmp = {}
        tmp['A'] = nm_in['T']
        tmp['T'] = nm_in['G']
        tmp['G'] = nm_in['C']
        tmp['C'] = nm_in['A']
        return tmp
```

---

#### unlucky[1]
**Python Bytecode:**
```python
    24           0 LOAD_CONST               1 ('AGCT')
                             2 STORE_FAST               0 (s1)

    25           4 LOAD_CONST               2 ('TCAG')
                             6 STORE_FAST               1 (s2)

    26           8 LOAD_CONST               3 ('CTGA')
                            10 STORE_FAST               2 (s3)

    27          12 LOAD_CONST               4 (<code object unlucky at 0x...>)
                            14 LOAD_CONST               5 ('unlucky_2.<locals>.<dictcomp>')
                            16 MAKE_FUNCTION            0
                            18 LOAD_FAST                0 (s1)
                            20 GET_ITER
                            22 CALL_FUNCTION            1
                            24 STORE_FAST               3 (tmp)

    28          26 LOAD_FAST                0 (s1)
                            28 LOAD_FAST                1 (s2)
                            30 LOAD_FAST                2 (s3)
                            32 BUILD_TUPLE              3
                            34 GET_ITER
                 >>   36 FOR_ITER                27 (to 92)
                            38 STORE_FAST               4 (s)

    29          40 LOAD_GLOBAL              0 (enumerate)
                            42 LOAD_GLOBAL              1 (sorted)
                            44 LOAD_GLOBAL              2 (nm)
                            46 LOAD_METHOD              3 (keys)
                            48 CALL_METHOD              0
                            50 CALL_FUNCTION            1
                            52 CALL_FUNCTION            1
                            54 GET_ITER
                 >>   56 FOR_ITER                16 (to 90)
                            58 UNPACK_SEQUENCE          2
                            60 STORE_FAST               5 (i)
                            62 STORE_FAST               6 (c)

    30          64 LOAD_FAST                3 (tmp)
                            66 LOAD_FAST                6 (c)
                            68 DUP_TOP_TWO
                            70 BINARY_SUBSCR
                            72 LOAD_GLOBAL              2 (nm)
                            74 LOAD_FAST                4 (s)
                            76 LOAD_FAST                5 (i)
                            78 BINARY_SUBSCR
                            80 BINARY_SUBSCR
                            82 INPLACE_SUBTRACT
                            84 ROT_THREE
                            86 STORE_SUBSCR
                            88 JUMP_ABSOLUTE           28 (to 56)

    29     >>   90 JUMP_ABSOLUTE           18 (to 36)

    31     >>   92 LOAD_FAST                3 (tmp)
                            94 STORE_GLOBAL             2 (nm)
                            96 LOAD_CONST               0 (None)
                            98 RETURN_VALUE
```

**Decompiled Python Code:**
```python
def unlucky1(nm_in):
        s1 = "AGCT"
        s2 = "TCAG"
        s3 = "CTGA"
        total = sum(nm_in.values())
        tmp = {c: total for c in s1}
        for s in (s1, s2, s3):
                for i, c in enumerate(sorted(nm_in.keys())):
                        tmp[c] -= nm_in[s[i]]
        return tmp
```

---

#### unlucky[2]
**Python Bytecode:**
```python
    35           0 LOAD_GLOBAL              0 (__import__)
                             2 LOAD_CONST               1 ('random')
                             4 CALL_FUNCTION            1
                             6 STORE_DEREF              0 (r)

    36           8 LOAD_DEREF               0 (r)
                            10 LOAD_METHOD              1 (seed)
                            12 LOAD_GLOBAL              0 (__import__)
                            14 LOAD_CONST               2 ('functools')
                            16 CALL_FUNCTION            1
                            18 LOAD_METHOD              2 (reduce)
                            20 LOAD_CONST               3 (<code object unlucky at 0x...>)
                            22 LOAD_CONST               4 ('unlucky_3.<locals>.<lambda>')
                            24 MAKE_FUNCTION            0
                            26 LOAD_GLOBAL              3 (nm)
                            28 LOAD_METHOD              4 (values)
                            30 CALL_METHOD              0
                            32 CALL_METHOD              2
                            34 CALL_METHOD              1
                            36 POP_TOP

    37          38 LOAD_BUILD_CLASS
                            40 LOAD_CLOSURE             0 (r)
                            42 BUILD_TUPLE              1
                            44 LOAD_CONST               5 (<code object unlucky at 0x...>)
                            46 LOAD_CONST               6 ('unlucky')
                            48 MAKE_FUNCTION            8 (closure)
                            50 LOAD_CONST               6 ('unlucky')
                            52 LOAD_GLOBAL              5 (dict)
                            54 CALL_FUNCTION            3
                            56 STORE_FAST               0 (unlucky)

    53          58 LOAD_FAST                0 (unlucky)
                            60 LOAD_GLOBAL              3 (nm)
                            62 CALL_FUNCTION            1
                            64 STORE_GLOBAL             3 (nm)
                            66 LOAD_CONST               0 (None)
                            68 RETURN_VALUE
```

**Decompiled Python Code:**
```python
def unlucky2(nm_in):
        seed = 0
        for v in nm_in.values():
                seed ^= v
        random.seed(seed)
        class Unlucky(dict):
                def __init__(self, mapping):
                        super().__init__(mapping)
                        keys = list("ACGT")
                        random.shuffle(keys)
                        for i in range(4):
                                self["ACGT"[i]] = mapping[keys[i]]
        new_nm = Unlucky(nm_in)
        return new_nm
```

---

#### unlucky[3]
**Python Bytecode:**
```python
    58           0 LOAD_BUILD_CLASS
                             2 LOAD_CONST               1 (<code object unlucky at 0x...>)
                             4 LOAD_CONST               2 ('MM')
                             6 MAKE_FUNCTION            0
                             8 LOAD_CONST               2 ('MM')
                            10 LOAD_GLOBAL              0 (type)
                            12 CALL_FUNCTION            3
                            14 STORE_FAST               0 (MM)

    70          16 LOAD_BUILD_CLASS
                            18 LOAD_CONST               3 (<code object unlucky at 0x...>)
                            20 LOAD_CONST               4 ('MD')
                            22 MAKE_FUNCTION            0
                            24 LOAD_CONST               4 ('MD')
                            26 LOAD_GLOBAL              1 (dict)
                            28 LOAD_FAST                0 (MM)
                            30 LOAD_CONST               5 (('metaclass',))
                            32 CALL_FUNCTION_KW         4
                            34 STORE_FAST               1 (MD)

    73          36 LOAD_GLOBAL              2 (exec)
                            38 LOAD_CONST               6 ("globals()['nucleotide_map'] = MD(")
                            40 LOAD_GLOBAL              1 (dict)
                            42 LOAD_GLOBAL              3 (nm)
                            44 CALL_FUNCTION            1
                            46 FORMAT_VALUE             0
                            48 LOAD_CONST               7 (')')
                            50 BUILD_STRING             3
                            52 CALL_FUNCTION            1
                            54 POP_TOP
                            56 LOAD_CONST               0 (None)
                            58 RETURN_VALUE
```

**Decompiled Python Code:**
```python
def unlucky3(nm_in):
        class MM(type):
                def __new__(cls, name, bases, dct):
                        return super().__new__(cls, name, bases, dct)
                def __call__(cls, *args, **kwargs):
                        instance = super().__call__(*args, **kwargs)
                        vals = list(instance.values())
                        vals = vals[::2] + vals[1::2]
                        for i, k in enumerate(sorted(instance.keys())):
                                instance[k] = vals[i]
                        return instance

        class MD(dict, metaclass=MM):
                pass

        new_nm = MD(dict(nm_in))
        return new_nm
```
```markdown
# Run and print after each step

```python
print("Initial nm:", nm)
nm = unlucky0(nm)
print("After unlucky0, nm =", nm)
nm = unlucky1(nm)
print("After unlucky1, nm =", nm)
nm = unlucky2(nm)
print("After unlucky2, nm =", nm)
nm = unlucky3(nm)
print("After unlucky3, nm =", nm)
```

## Output

```plaintext
Initial nm: {'A': 0, 'T': 1, 'G': 2, 'C': 3}
After unlucky0, nm = {'A': 1, 'T': 2, 'G': 3, 'C': 0}
After unlucky1, nm = {'A': 3, 'G': 2, 'C': 1, 'T': 0}
After unlucky2, nm = {'A': 2, 'G': 1, 'C': 3, 'T': 0}
After unlucky3, nm = {'A': 2, 'G': 1, 'C': 3, 'T': 0}
```

## Explanation

- **Initial nm**: The starting nucleotide map is `{'A': 0, 'T': 1, 'G': 2, 'C': 3}`.
- **After unlucky0**: The nucleotide map is updated based on the first transformation function.
- **After unlucky1**: The nucleotide map is further transformed using the second function.
- **After unlucky2**: The third transformation function applies additional changes.
- **After unlucky3**: The final transformation function is applied, resulting in the final nucleotide map.

Each function (`unlucky0`, `unlucky1`, `unlucky2`, `unlucky3`) modifies the global `nm` variable, and the changes are printed after each step.
```
