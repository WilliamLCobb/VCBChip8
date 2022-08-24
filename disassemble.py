import os.path
import sys
from enum import Enum
from typing import *
from instruction import *


class Nibbles16Bit:
    def __init__(self, number: int):
        self._number = number

    def __getitem__(self, key: int) -> int:
        return (self._number >> (4 * (3 - key))) & 0xF


def convert_address_to_label(address):
    return f'@addr_{str(hex(address))[2:]}'


def parse_machine_instruction(instruction: int) -> Instruction:
    if instruction == 0x00E0:
        return Instruction(OpCode.CLS)
    elif instruction == 0x00EE:
        return Instruction(OpCode.RET)

    nibbles = Nibbles16Bit(instruction)
    left = nibbles[0]

    if left == 1:
        address = instruction & 0xFFF
        return Instruction(OpCode.JPI, data=address)
    elif left == 2:
        address = instruction & 0xFFF
        return Instruction(OpCode.CALL, data=address)
    elif left == 3:
        return Instruction(OpCode.SEI,
                           vx=nibbles[1],
                           data=instruction & 0xFF)
    elif left == 4:
        return Instruction(OpCode.SNEI,
                           vx=nibbles[1],
                           data=instruction & 0xFF)
    elif left == 5:
        return Instruction(OpCode.SE,
                           vx=nibbles[1],
                           vy=nibbles[2])
    elif left == 6:
        return Instruction(OpCode.LDI,
                           vx=nibbles[1],
                           data=instruction & 0xFF)
    elif left == 7:
        return Instruction(OpCode.ADD,
                           vx=nibbles[1],
                           data=instruction & 0xFF)
    elif left == 8:
        right = nibbles[3]
        if right == 0:
            return Instruction(OpCode.LD,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 1:
            return Instruction(OpCode.OR,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 2:
            return Instruction(OpCode.AND,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 3:
            return Instruction(OpCode.XOR,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 4:
            return Instruction(OpCode.ADD,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 5:
            return Instruction(OpCode.SUB,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 6:
            return Instruction(OpCode.SHR,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 7:
            return Instruction(OpCode.SUBN,
                               vx=nibbles[1],
                               vy=nibbles[2])
        elif right == 15:
            return Instruction(OpCode.SHL,
                               vx=nibbles[1],
                               vy=nibbles[2])
    elif left == 9:
        return Instruction(OpCode.SNE,
                           vx=nibbles[1],
                           vy=nibbles[2])
    elif left == 10:
        return Instruction(OpCode.STI,
                           data=instruction & 0xFFF)
    elif left == 11:
        return Instruction(OpCode.JPO,
                           data=instruction & 0xFFF)
    elif left == 12:
        return Instruction(OpCode.RND,
                           vx=nibbles[1],
                           data=instruction & 0xFF)
    elif left == 13:
        return Instruction(OpCode.DRW,
                           vx=nibbles[1],
                           vy=nibbles[2],
                           data=instruction & 0xF)
    elif left == 14:
        right_two = instruction & 0xFF
        if right_two == 0x9E:
            return Instruction(OpCode.SKP,
                               vx=nibbles[1])
        elif right_two == 0xA1:
            return Instruction(OpCode.SKNP,
                               vx=nibbles[1])
    elif left == 15:
        right_two = instruction & 0xFF
        if right_two == 0x07:
            return Instruction(f'LD V{nibbles[1]}, DT')
        elif right_two == 0x0A:
            return Instruction(f'LD V{nibbles[1]}, K')
        elif right_two == 0x15:
            return Instruction(f'LD DT, V{nibbles[1]}')
        elif right_two == 0x18:
            return Instruction(f'LD ST, V{nibbles[1]}')
        elif right_two == 0x1E:
            return Instruction(f'ADD I, V{nibbles[1]}')
        elif right_two == 0x29:
            return Instruction(f'LD F, V{nibbles[1]}')
        elif right_two == 0x33:
            return Instruction(f'LD B, V{nibbles[1]}')
        elif right_two == 0x55:
            return Instruction(f'LD [I], V{nibbles[1]}')
        elif right_two == 0x65:
            return Instruction(f'LD V{nibbles[1]}, [I]')
    return Instruction(None, data=instruction)


def disassemble_file(filepath: str):
    output = ""
    instructions = []
    raw_opcodes = []

    for i in range(511):
        output += "0x00\n"

    with open(filepath, 'rb') as f:
        chunk = f.read(2)
        while chunk:
            raw_opcodes.append(int.from_bytes(chunk, "big"))
            instructions.append(
                parse_machine_instruction(int.from_bytes(chunk, "big")))
            chunk = f.read(2)

    for instruction, raw in zip(instructions, raw_opcodes):
        nibbles = Nibbles16Bit(raw)
        left = "{0:#0{1}x}".format((nibbles[0] << 4) + nibbles[1], 4)
        right = "{0:#0{1}x}".format((nibbles[2] << 4) + nibbles[3], 4)
        if instruction.op_code:
            output += left + "  # " + str(instruction) + "\n"
        else:
            output += left + "\n"
        output += right + "\n"
    return output


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 main.py <ROM File>')
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f'{filepath} does not exist!')
        sys.exit(1)

    print(disassemble_file(filepath))