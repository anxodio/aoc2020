from pathlib import Path
from typing import List, Set, Generator
from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class Instruction:
    operation: str
    argument: int


class InfiniteLoopError(Exception):
    pass


class Program:
    def __init__(self, instructions: List[Instruction]) -> None:
        self._reset()
        self._instructions = instructions

    def _reset(self) -> None:
        self._index: int = 0
        self._accumulator: int = 0
        self._visited_index: Set[int] = set()

    @property
    def accumulator(self) -> int:
        return self._accumulator

    def execute(self) -> None:
        self._reset()
        while self._index < len(self._instructions):
            self._check_visited_index(self._index)
            instruction = self._instructions[self._index]
            if instruction.operation == "acc":
                self._accumulator += instruction.argument
            self._index += instruction.argument if instruction.operation == "jmp" else 1

    def _check_visited_index(self, index: int) -> None:
        if index in self._visited_index:
            raise InfiniteLoopError(f"Index {index} visited twice.")
        self._visited_index.add(index)


def line_to_instruction(line: str) -> Instruction:
    operation, raw_argument = line.split(" ")
    return Instruction(operation, int(raw_argument))


def sanitize_instructions(instructions: List[Instruction]) -> List[Instruction]:
    for alternative_instructions in _generate_alternative_instructions(instructions):
        program = Program(alternative_instructions)
        try:
            program.execute()
            return alternative_instructions
        except InfiniteLoopError:
            continue
    raise Exception("Not found D:")


def _generate_alternative_instructions(
    instructions: List[Instruction],
) -> Generator[List[Instruction], None, None]:
    alternative_instructions = instructions.copy()
    for i, instruction in enumerate(instructions):
        if instruction.operation in ["jmp", "nop"]:
            alternative_instructions[i] = _swap_nop_jmp_instruction(instruction)
            yield alternative_instructions
            alternative_instructions[i] = instruction


def _swap_nop_jmp_instruction(instruction: Instruction) -> Instruction:
    if instruction.operation == "jmp":
        return Instruction("nop", instruction.argument)
    return Instruction("jmp", instruction.argument)


def test_get_instruction_from_line():
    assert line_to_instruction("nop +0") == Instruction("nop", 0)
    assert line_to_instruction("acc +3") == Instruction("acc", 3)
    assert line_to_instruction("jmp -2") == Instruction("jmp", -2)


test_instructions = [
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


def test_execute_program():
    program = Program(test_instructions)
    with pytest.raises(InfiniteLoopError):
        program.execute()
    assert program.accumulator == 5


def test_execute_healthy_program():
    program = Program(
        [Instruction("nop", 0), Instruction("acc", 42), Instruction("nop", 0)]
    )
    program.execute()
    assert program.accumulator == 42


def test_sanitize_instructions():
    healthy_instructions = sanitize_instructions(test_instructions)
    program = Program(healthy_instructions)
    program.execute()
    assert program.accumulator == 8


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        instructions = [line_to_instruction(line.rstrip("\n")) for line in f]

    healthy_instructions = sanitize_instructions(instructions)
    program = Program(healthy_instructions)
    program.execute()
    print(program.accumulator)
