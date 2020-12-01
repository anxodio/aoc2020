from pathlib import Path
from typing import List


def expense_report(expenses: List[int]):
    return 514579


def test_expense_report():
    assert (
        expense_report(
            [
                1721,
                979,
                366,
                299,
                675,
                1456,
            ]
        )
        == 514579
    )


if __name__ == "__main__":
    with open((Path(__file__).parent / "input1.txt")) as f:
        expenses = [int(line) for line in f.readlines()]
    print(expense_report(expenses))
