from pathlib import Path
from typing import List, Iterable, Generator
from itertools import takewhile


def separate_group_lines(raw_lines: List[str]) -> Generator[List[str], None, None]:
    raw_lines_iterator = iter(raw_lines)
    while (lines := list(takewhile(lambda line: line != "", raw_lines_iterator))) :
        yield lines


def count_affimative_answers_from_lines(lines: Iterable[str]) -> int:
    return len(set("".join(lines)))


def test_separate_group_lines():
    assert list(separate_group_lines(["abc", "", "a", "b", "c", "", "ab", "ac"])) == [
        ["abc"],
        ["a", "b", "c"],
        ["ab", "ac"],
    ]


def test_count_affimative_answers_from_lines():
    assert count_affimative_answers_from_lines(["ab", "ac"]) == 3


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        raw_lines = [line.rstrip("\n") for line in f]

    print(
        sum(
            count_affimative_answers_from_lines(lines)
            for lines in separate_group_lines(raw_lines)
        )
    )
