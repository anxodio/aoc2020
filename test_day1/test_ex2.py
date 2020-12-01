from pathlib import Path
from typing import List
import itertools


def expense_report_v2(expenses: List[int]) -> int:
    TARGET_SUM = 2020
    for exp1, exp2, exp3 in itertools.combinations(expenses, 3):
        if sum((exp1, exp2, exp3)) == TARGET_SUM:
            return exp1 * exp2 * exp3
    raise Exception("Not found D:")


def test_expense_report_v2():
    assert (
        expense_report_v2(
            [
                1721,
                979,
                366,
                299,
                675,
                1456,
            ]
        )
        == 241861950
    )


if __name__ == "__main__":
    with open((Path(__file__).parent / "input1.txt")) as f:
        expenses = [int(line) for line in f.readlines()]
    print(expense_report_v2(expenses))
