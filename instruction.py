from enum import *
from typing import *

class OpCode(Enum):
    CLS = "CLS"
    RET = "RET"
    JP = "JP"
    JPI = "JPI"
    JPO = "JPO"
    CALL = "CALL"
    SE = "SE"
    SEI = "SEI"
    SNE = "SNE"
    SNEI = "SNEI"
    STI = "STI"
    LD = "LD"
    LDI = "LDI"
    ADD = "ADDI"
    ADDI = "ADDI"
    OR = "OR"
    AND = "AND"
    XOR = "XOR"
    SUB = "SUB"
    SHR = "SHR"
    SUBN = "SUBN"
    SHL = "SHL"
    RND = "RND"
    DRW = "DRW"
    SKP = "SKP"
    SKNP = "SKNP"





class Instruction:
    def __init__(self, instruction: OpCode, vx=None, vy=None, data=None):
        self.op_code = instruction
        self.vx = vx
        self.vy = vy
        self.data = data
        if data and not isinstance(data, int):
            raise RuntimeError(f"Incorrect data type: {type(data)}")

    def jump_address(self) -> Optional[int]:
        if self.op_code in (OpCode.CALL, OpCode.JPI):
            return self.data

    def __str__(self):
        instruction_string = ""
        if self.op_code:
            instruction_string += f'{self.op_code.value} '
        if self.vx is not None:
            instruction_string += f'V{self.vx} '
        if self.vy is not None:
            instruction_string += f'V{self.vy} '
        if self.data:
            instruction_string += hex(self.data)
        return instruction_string