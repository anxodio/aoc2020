from pathlib import Path
from typing import Tuple
import operator


def solve_operation(operation: str) -> int:
    while (indexes := _find_suboperation_indexes(operation)) != (-1, -1):
        start, end = indexes
        subresult = solve_operation(operation[start + 1 : end])
        operation = operation[0:start] + str(subresult) + operation[end + 1 :]

    value = 0
    last_operation = operator.add
    for i, char in enumerate(operation.split(" ")):
        if char.isnumeric():
            value = last_operation(value, int(char))
        else:
            last_operation = operator.add if char == "+" else operator.mul
    return value


def _find_suboperation_indexes(operation: str) -> Tuple[int, int]:
    if (starting_index := operation.find("(")) != -1:
        extra_parentheses = 0
        for i, char in enumerate(operation[starting_index + 1 :]):
            if char == "(":
                extra_parentheses += 1
            elif char == ")" and extra_parentheses > 0:
                extra_parentheses -= 1
            elif char == ")":
                return starting_index, starting_index + 1 + i
    return (-1, -1)


def test_solve_no_parentheses_operation() -> None:
    assert solve_operation("1 + 2 * 3 + 4 * 5 + 6") == 71


def test_solve_operation_with_parentheses() -> None:
    assert solve_operation("2 * 3 + (4 * 5)") == 26
    assert solve_operation("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert solve_operation("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    assert solve_operation("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert solve_operation("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]

    print(sum(solve_operation(line) for line in lines))
