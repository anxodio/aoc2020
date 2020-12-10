from pathlib import Path
from typing import List
from collections import defaultdict


# I had to search how to do it without brute force, but at least I understand it 🤷‍♂
# It is solved in O(n), just sorting and iterating the list.
# It calculates all possible paths to every point, adding the possible paths of the
# previois points.
def count_all_possible_paths(numbers: List[int]) -> int:
    paths = defaultdict(int)
    paths[0] = 1  # charging outlet
    for number in sorted(numbers):
        if number - 1 in paths:
            paths[number] += paths[number - 1]
        if number - 2 in paths:
            paths[number] += paths[number - 2]
        if number - 3 in paths:
            paths[number] += paths[number - 3]
    return paths[max(numbers)]


def test_count_all_possible_paths():
    assert count_all_possible_paths([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]) == 8


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        numbers = [int(line.rstrip("\n")) for line in f]

    print(count_all_possible_paths(numbers))
