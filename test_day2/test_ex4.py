from pathlib import Path
from typing import List
from dataclasses import dataclass
from collections import Counter


# Ultra coupled :D
@dataclass
class PasswordPolicy:
    letter: str
    first_index: int
    second_index: int
    password: str

    def is_valid(self) -> bool:
        return (self.password[self.first_index] == self.letter) ^ (
            self.password[self.second_index] == self.letter
        )

    @staticmethod
    def from_text_line(line: str) -> "PasswordPolicy":
        indexes, dirtyletter, password = line.split(" ")
        letter = dirtyletter[0]
        first_index, second_index = map(lambda s: int(s) - 1, indexes.split("-"))
        return PasswordPolicy(
            letter=letter,
            first_index=first_index,
            second_index=second_index,
            password=password,
        )


def valid_password_counter(passwords: List[PasswordPolicy]) -> int:
    return sum(1 for password in passwords if password.is_valid())


def test_valid_password():
    assert (
        PasswordPolicy(
            letter="a", first_index=0, second_index=2, password="abcde"
        ).is_valid()
        is True
    )


def test_no_letter_invalid_password():
    assert (
        PasswordPolicy(
            letter="b", first_index=0, second_index=2, password="cdefg"
        ).is_valid()
        is False
    )


def test_more_than_one_letter_invalid_password():
    assert (
        PasswordPolicy(
            letter="c", first_index=1, second_index=8, password="ccccccccc"
        ).is_valid()
        is False
    )


def test_transform_from_text_line():
    assert PasswordPolicy.from_text_line("1-3 a: abcde") == PasswordPolicy(
        letter="a", first_index=0, second_index=2, password="abcde"
    )


def test_valid_password_counter():
    passwords = [
        PasswordPolicy(letter="a", first_index=0, second_index=2, password="abcde"),
        PasswordPolicy(letter="b", first_index=0, second_index=2, password="cdefg"),
    ]
    assert valid_password_counter(passwords) == 1


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        passwords = [PasswordPolicy.from_text_line(line) for line in f.readlines()]
    print(valid_password_counter(passwords))
