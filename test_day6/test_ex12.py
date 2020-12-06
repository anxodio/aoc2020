from pathlib import Path
from typing import List, Generator
from itertools import takewhile


def separate_group_lines(raw_lines: List[str]) -> Generator[List[str], None, None]:
    raw_lines_iterator = iter(raw_lines)
    while (lines := list(takewhile(lambda line: line != "", raw_lines_iterator))) :
        yield lines


def count_all_affirmative_answers_from_group(group_lines: List[str]) -> int:
    return len(set(group_lines[0]).intersection(*(set(group) for group in group_lines)))


def test_separate_group_lines():
    assert list(separate_group_lines(["abc", "", "a", "b", "c", "", "ab", "ac"])) == [
        ["abc"],
        ["a", "b", "c"],
        ["ab", "ac"],
    ]


def test_count_all_affirmative_answers_from_group():
    assert count_all_affirmative_answers_from_group(["abc"]) == 3
    assert count_all_affirmative_answers_from_group(["ab", "ac"]) == 1
    assert count_all_affirmative_answers_from_group(["a", "b", "c"]) == 0


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        raw_lines = [line.rstrip("\n") for line in f]

    print(
        sum(
            count_all_affirmative_answers_from_group(group_lines)
            for group_lines in separate_group_lines(raw_lines)
        )
    )
