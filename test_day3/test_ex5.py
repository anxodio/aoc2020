from pathlib import Path
from typing import List
from collections import UserList


class TreeRow(UserList):
    def __getitem__(self, key: int) -> str:
        return self.data[key % len(self.data)]


def test_treerow_existing_positions():
    treerow = TreeRow("..##.")
    assert treerow[0] == "."
    assert treerow[2] == "#"


def test_treerow_far_positions():
    treerow = TreeRow("..##.")
    assert treerow[5] == "."
    assert treerow[13] == "#"


# if __name__ == "__main__":
#     with open((Path(__file__).parent / "input.txt")) as f:
#         passwords = [PasswordPolicy.from_text_line(line) for line in f.readlines()]
#     print(valid_password_counter(passwords))
