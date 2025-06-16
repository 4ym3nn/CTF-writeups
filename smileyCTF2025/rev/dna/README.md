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
!()[] image url
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

### starting with the challenge :
to decompile .pyc into python back i used https://pylingual.io/
