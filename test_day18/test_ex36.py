from pathlib import Path


def solve_operation(operation: str) -> int:
    from_index = 0
    while (add_index := operation.find("+", from_index)) != -1:
        start = _find_start_close_position(
            operation, range(add_index - 1, -1, -1), ")", "("
        )
        end = _find_start_close_position(
            operation, range(add_index + 1, len(operation)), "(", ")"
        )
        from_index = add_index + 2
        operation = (
            f"{operation[0:start]}({operation[start : end + 1]}){operation[end + 1 :]}"
        )
    return eval(operation)


def _find_start_close_position(
    operation: str, direction: range, opening: str, closing: str
) -> int:
    num_parentheses = 0
    for i in direction:
        char = operation[i]
        if char == opening:
            num_parentheses += 1
        elif char == closing and num_parentheses > 1:
            num_parentheses -= 1
        elif char == closing or (char.isnumeric() and num_parentheses == 0):
            return i
    raise Exception("There is a bug in _find_start_close_position")


def test_solve_no_parentheses_operation() -> None:
    assert solve_operation("1 + 2 * 3 + 4 * 5 + 6") == 231


def test_solve_operation_with_parentheses() -> None:
    assert solve_operation("2 * 3 + (4 * 5)") == 46
    assert solve_operation("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert solve_operation("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert solve_operation("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert solve_operation("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]

    print(sum(solve_operation(line) for line in lines))
