from pathlib import Path
from typing import List, Iterable, Any
from itertools import tee


def find_jolt_differences_calculation(numbers: List[int]) -> int:
    diff_1 = 0
    diff_3 = 1  # last one
    sorted_numbers_from_0 = sorted([0] + numbers)
    for n1, n2 in pairwise(sorted_numbers_from_0):
        if n2 - n1 == 1:
            diff_1 += 1
        else:
            diff_3 += 1

    return diff_1 * diff_3


# Recipe from https://docs.python.org/3/library/itertools.html
def pairwise(iterable: Iterable[Any]):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def test_find_jolt_differences_calculation():
    assert (
        find_jolt_differences_calculation([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]) == 35
    )


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        numbers = [int(line.rstrip("\n")) for line in f]

    print(find_jolt_differences_calculation(numbers))
