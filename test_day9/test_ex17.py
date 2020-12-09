from pathlib import Path
from typing import List
from itertools import dropwhile, combinations


def find_invalid_number(numbers: List[int], preamble: int = 25) -> int:
    for i, number in dropwhile(lambda x: x[0] < preamble, enumerate(numbers)):
        is_valid = any(
            n1 + n2 == number for n1, n2 in combinations(numbers[i - preamble : i], 2)
        )
        if not is_valid:
            return number
    raise Exception("Not found D:")


def test_find_invalid_number():
    assert (
        find_invalid_number(
            [
                35,
                20,
                15,
                25,
                47,
                40,
                62,
                55,
                65,
                95,
                102,
                117,
                150,
                182,
                127,
                219,
                299,
                277,
                309,
                576,
            ],
            5,
        )
        == 127
    )


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        numbers = [int(line.rstrip("\n")) for line in f]

    print(find_invalid_number(numbers))
