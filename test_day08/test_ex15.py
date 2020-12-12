from pathlib import Path
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    operation: str
    argument: int


class Program:
    def __init__(self, instructions: List[Instruction]) -> None:
        self._accumulator: int = 0
        self._instructions = instructions

    @property
    def accumulator(self) -> int:
        return self._accumulator

    def execute(self) -> None:
        index: int = 0
        visited_index: List[int] = []
        while index not in visited_index:
            visited_index.append(index)
            instruction = self._instructions[index]
            if instruction.operation == "acc":
                self._accumulator += instruction.argument
            index += instruction.argument if instruction.operation == "jmp" else 1


def line_to_instruction(line: str) -> Instruction:
    operation, raw_argument = line.split(" ")
    return Instruction(operation, int(raw_argument))


def test_get_instruction_from_line():
    assert line_to_instruction("nop +0") == Instruction("nop", 0)
    assert line_to_instruction("acc +3") == Instruction("acc", 3)
    assert line_to_instruction("jmp -2") == Instruction("jmp", -2)


def test_execute_program():
    program = Program(
        [
            Instruction("nop", 0),
            Instruction("acc", 1),
            Instruction("jmp", 4),
            Instruction("acc", 3),
            Instruction("jmp", -3),
            Instruction("acc", -99),
            Instruction("acc", 1),
            Instruction("jmp", -4),
            Instruction("acc", 6),
        ]
    )
    program.execute()
    assert program.accumulator == 5


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        instructions = [line_to_instruction(line.rstrip("\n")) for line in f]

    program = Program(instructions)
    program.execute()
    print(program.accumulator)
