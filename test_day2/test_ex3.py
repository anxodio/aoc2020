from pathlib import Path
from typing import List
from dataclasses import dataclass
from collections import Counter


# Ultra coupled :D
@dataclass
class PasswordPolicy:
    letter: str
    minimum: int
    maximum: int
    password: str

    def is_valid(self) -> bool:
        return self.minimum <= Counter(self.password)[self.letter] <= self.maximum

    @staticmethod
    def from_text_line(line: str) -> "PasswordPolicy":
        minmax, dirtyletter, password = line.split(" ")
        letter = dirtyletter[0]
        minimum, maximum = map(int, minmax.split("-"))
        return PasswordPolicy(
            letter=letter, minimum=minimum, maximum=maximum, password=password
        )


def valid_password_counter(passwords: List[PasswordPolicy]) -> int:
    return sum(1 for password in passwords if password.is_valid())


def test_valid_password():
    assert (
        PasswordPolicy(letter="a", minimum=1, maximum=3, password="abcde").is_valid()
        is True
    )


def test_invalid_password():
    assert (
        PasswordPolicy(letter="b", minimum=1, maximum=3, password="cdefg").is_valid()
        is False
    )


def test_transform_from_text_line():
    assert PasswordPolicy.from_text_line("1-3 a: abcde") == PasswordPolicy(
        letter="a", minimum=1, maximum=3, password="abcde"
    )


def test_valid_password_counter():
    passwords = [
        PasswordPolicy(letter="a", minimum=1, maximum=3, password="abcde"),
        PasswordPolicy(letter="b", minimum=1, maximum=3, password="cdefg"),
    ]
    assert valid_password_counter(passwords) == 1


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        passwords = [PasswordPolicy.from_text_line(line) for line in f.readlines()]
    print(valid_password_counter(passwords))
