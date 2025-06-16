#!/usr/bin/env python3
"""
Dynamic DNA Virtual Machine Disassembler

This disassembler converts DNA-based bytecode into readable assembly instructions
while tracking dynamic nucleotide mapping changes that occur after CALL operations.
"""

import sys
from typing import List, Tuple, Dict

class DynamicDNADisassembler:
    def __init__(self):
        # Initial nucleotide mapping
        self.initial_nm = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
        
        # Instruction set mapping
        self.instructions = {
            0: "PUSH",      # Push operand to stack
            1: "POP",       # Pop from stack
            2: "LOAD",      # Load from memory[operand] to stack
            3: "STORE",     # Store stack top to memory[operand]
            4: "ADD",       # Pop two values, push sum
            5: "SUB",       # Pop two values, push difference (b-a)
            6: "MUL",       # Pop two values, push product
            7: "MOD",       # Pop two values, push modulo (b%a)
            8: "EQ",        # Pop two values, push 1 if equal, 0 otherwise
            9: "JMP",       # Jump to operand address
            10: "JEQ",      # Jump if stack top == 1
            11: "JNE",      # Jump if stack top != 1
            12: "PRINT",    # Print stack top as character
            13: "CALL",     # Call snippet with stack top as key
            14: "SWAP",     # Swap nucleotide mappings
            15: "HALT"      # Halt execution
        }
        
        # Dynamic mapping transformations based on your analysis
        self.mapping_transforms = {
            # fun1 (key 111): A->T->G->C->A rotation
            111: {'A': 1, 'T': 2, 'G': 3, 'C': 0},
            # fun2 (key 117): Complex transform
            117: {'A': 3, 'G': 2, 'C': 1, 'T': 0},
            # fun3 (key 105): Another transform
            105: {'A': 2, 'G': 1, 'C': 3, 'T': 0}
        }
        
        # Predefined memory values
        self.predefined_values = {22: 105, 26: 111, 27: 117}
    
    def trans(self, dna_sequence: str, nm: Dict[str, int]) -> int:
        """Convert DNA sequence to integer using current nucleotide mapping"""
        return sum((nm[c] << 2 * i for i, c in enumerate(dna_sequence)))
    
    def reverse_trans(self, value: int, length: int) -> str:
        """Convert integer back to DNA sequence"""
        nucleotides = ['A', 'T', 'G', 'C']
        result = []
        for i in range(length):
            result.append(nucleotides[(value >> (2 * i)) & 3])
        return ''.join(result)
    
    def predict_call_key(self, instructions_so_far: List, current_stack: List[int]) -> int:
        """
        Predict the key that will be used for CALL instruction
        Based on stack operations and memory loads
        """
        # Look for recent LOAD operations from predefined memory locations
        for addr, instr, operand_dna, operand in reversed(instructions_so_far[-10:]):
            if instr == "LOAD" and operand in self.predefined_values:
                return self.predefined_values[operand]
        
        # If we can't predict, return None
        return None
    
    def disassemble_dynamic(self, code: str) -> List[Tuple[int, str, str, int, Dict[str, int]]]:
        """
        Disassemble DNA bytecode with dynamic nucleotide mapping tracking
        Returns list of tuples: (address, instruction, operand_dna, operand_value, current_nm)
        """
        instructions = []
        pc = 0
        current_nm = self.initial_nm.copy()
        call_count = 0
        
        while pc < len(code):
            # Extract opcode (2 nucleotides) and operand (10 nucleotides)
            if pc + 2 > len(code):
                break
                
            opcode_dna = code[pc:pc + 2]
            opcode = self.trans(opcode_dna, current_nm)
            
            # Determine instruction length based on opcode
            if opcode in [1, 4, 5, 6, 7, 8, 12, 13, 14, 15]:
                # Instructions without operand (2 nucleotides)
                operand_dna = ""
                operand = 0
                instruction_length = 2
            else:
                # Instructions with operand (12 nucleotides total)
                if pc + 12 > len(code):
                    break
                operand_dna = code[pc + 2:pc + 12]
                operand = self.trans(operand_dna, current_nm)
                instruction_length = 12
            
            # Get instruction name
            instr_name = self.instructions.get(opcode, f"UNKNOWN_{opcode}")
            
            # Store instruction with current mapping
            instructions.append((pc, instr_name, operand_dna, operand, current_nm.copy()))
            
            # Handle dynamic mapping changes after CALL instructions
            if instr_name == "CALL":
                call_count += 1
                # Predict the key based on pattern analysis
                predicted_key = None
                
                # Based on your sequence: fun1(111), fun2(117), fun3(105), fun4(105)
                if call_count == 1:
                    predicted_key = 111
                elif call_count == 2:
                    predicted_key = 117
                elif call_count >= 3:
                    predicted_key = 105
                
                if predicted_key and predicted_key in self.mapping_transforms:
                    current_nm = self.mapping_transforms[predicted_key].copy()
                    print(f"DEBUG: After CALL #{call_count}, nm updated to: {current_nm}")
            
            pc += instruction_length
        
        return instructions
    
    def format_instruction_dynamic(self, addr: int, instr: str, operand_dna: str, 
                                 operand: int, nm: Dict[str, int], call_count: int = 0) -> str:
        """Format a single instruction for display with mapping info"""
        addr_str = f"{addr:04d}"
        
        # Show current nucleotide mapping state
        nm_str = f"[nm: A={nm['A']},T={nm['T']},G={nm['G']},C={nm['C']}]"
        
        if operand_dna:
            base_str = f"{addr_str}: {instr:<8} {operand_dna} ({operand})"
            # Add special annotations
            if instr in ["LOAD", "STORE"]:
                if operand == 666:
                    base_str += " ; debug marker"
                elif operand >= 640 and operand < 696:
                    base_str += f" ; flag[{operand-640}]"
                elif operand in [22, 26, 27]:
                    value = self.predefined_values.get(operand, "unknown")
                    base_str += f" ; predefined value={value}"
            return f"{base_str} {nm_str}"
        else:
            # Add special annotations for CALL instructions
            if instr == "CALL":
                return f"{addr_str}: {instr:<8} ; will change nucleotide mapping {nm_str}"
            return f"{addr_str}: {instr} {nm_str}"
    
    def disassemble_file_dynamic(self, filename: str) -> str:
        """Disassemble a DNA bytecode file with dynamic mapping tracking"""
        try:
            with open(filename, 'r') as f:
                code = f.read().strip()
        except FileNotFoundError:
            return f"Error: File '{filename}' not found"
        except Exception as e:
            return f"Error reading file: {e}"
        
        instructions = self.disassemble_dynamic(code)
        
        if not instructions:
            return "No valid instructions found"
        
        # Format output
        output_lines = []
        output_lines.append("Dynamic DNA Virtual Machine Disassembly")
        output_lines.append("=" * 50)
        output_lines.append("Nucleotide mappings change after each CALL instruction")
        output_lines.append("")
        
        call_count = 0
        for addr, instr, operand_dna, operand, nm in instructions:
            if instr == "CALL":
                call_count += 1
            output_lines.append(self.format_instruction_dynamic(addr, instr, operand_dna, operand, nm, call_count))
        
        output_lines.append("")
        output_lines.append(f"Total instructions: {len(instructions)}")
        output_lines.append(f"CALL operations: {call_count}")
        
        return "\n".join(output_lines)
    
    def analyze_mapping_evolution(self, code: str) -> Dict:
        """Analyze how nucleotide mappings evolve throughout execution"""
        instructions = self.disassemble_dynamic(code)
        
        mapping_states = []
        call_positions = []
        
        for addr, instr, operand_dna, operand, nm in instructions:
            if instr == "CALL":
                call_positions.append(addr)
            mapping_states.append((addr, nm.copy()))
        
        return {
            'mapping_evolution': mapping_states,
            'call_positions': call_positions,
            'total_calls': len(call_positions)
        }
    
    def compare_static_vs_dynamic(self, code: str) -> str:
        """Compare static vs dynamic disassembly to show the differences"""
        # Static disassembly (original method)
        static_instructions = []
        pc = 0
        static_nm = self.initial_nm
        
        while pc < len(code):
            if pc + 2 > len(code):
                break
                
            opcode_dna = code[pc:pc + 2]
            opcode = self.trans(opcode_dna, static_nm)
            
            if opcode in [1, 4, 5, 6, 7, 8, 12, 13, 14, 15]:
                operand_dna = ""
                operand = 0
                instruction_length = 2
            else:
                if pc + 12 > len(code):
                    break
                operand_dna = code[pc + 2:pc + 12]
                operand = self.trans(operand_dna, static_nm)
                instruction_length = 12
            
            instr_name = self.instructions.get(opcode, f"UNKNOWN_{opcode}")
            static_instructions.append((pc, instr_name, operand_dna, operand))
            pc += instruction_length
        
        # Dynamic disassembly
        dynamic_instructions = self.disassemble_dynamic(code)
        
        # Compare and show differences
        output_lines = []
        output_lines.append("Static vs Dynamic Disassembly Comparison")
        output_lines.append("=" * 50)
        output_lines.append("")
        
        for i, ((s_addr, s_instr, s_op_dna, s_op), (d_addr, d_instr, d_op_dna, d_op, d_nm)) in enumerate(zip(static_instructions, dynamic_instructions)):
            if s_instr != d_instr or s_op != d_op:
                output_lines.append(f"DIFFERENCE at position {i}:")
                output_lines.append(f"  Static:  {s_addr:04d}: {s_instr:<8} {s_op_dna} ({s_op})")
                output_lines.append(f"  Dynamic: {d_addr:04d}: {d_instr:<8} {d_op_dna} ({d_op}) [nm: A={d_nm['A']},T={d_nm['T']},G={d_nm['G']},C={d_nm['C']}]")
                output_lines.append("")
        
        return "\n".join(output_lines)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <dna_bytecode_file>")
        sys.exit(1)
    
    disassembler = DynamicDNADisassembler()
    
    print("=== DYNAMIC DISASSEMBLY ===")
    result = disassembler.disassemble_file_dynamic(sys.argv[1])
    print(result)
    
    # print("\n=== MAPPING EVOLUTION ANALYSIS ===")
    # try:
    #     with open(sys.argv[1], 'r') as f:
    #         code = f.read().strip()
        
    #     evolution = disassembler.analyze_mapping_evolution(code)
        
    #     print(f"Total CALL operations found: {evolution['total_calls']}")
    #     print("CALL positions:", evolution['call_positions'])
        
    #     print("\nMapping state changes:")
    #     prev_nm = None
    #     for addr, nm in evolution['mapping_evolution']:
    #         if prev_nm is None or nm != prev_nm:
    #             print(f"  Address {addr}: A={nm['A']}, T={nm['T']}, G={nm['G']}, C={nm['C']}")
    #             prev_nm = nm
        
    #     print("\n=== STATIC vs DYNAMIC COMPARISON ===")
    #     comparison = disassembler.compare_static_vs_dynamic(code)
        
    # except Exception as e:
    #     print(f"Analysis error: {e}")

if __name__ == "__main__":
    main()