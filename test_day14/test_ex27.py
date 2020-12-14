import re
from pathlib import Path
from typing import List, Tuple, Union
from collections import UserDict


class DockingMemory(UserDict):
    _MASK_LEN = 36

    def __init__(self):
        self._mask: List[Union[str, None]] = [None] * self._MASK_LEN
        super().__init__()

    def set_mask(self, raw_mask: str) -> None:
        self._mask = [None if digit == "X" else digit for digit in raw_mask]

    def __setitem__(self, key: int, item: int) -> None:
        masked_item = self._apply_mask(item)
        self.data[key] = masked_item

    def _apply_mask(self, num: int) -> int:
        binary_str = f"{num:b}".zfill(self._MASK_LEN)
        masked_str = "".join(
            self._mask[i] or binary_str[i] for i in range(self._MASK_LEN)
        )
        return int(masked_str, 2)


def get_key_value_from_line(line: str) -> Tuple[int, int]:
    raw_key, raw_value = re.match(r"mem\[(\d+)\] = (\d+)", line).group(1, 2)  # type: ignore
    return int(raw_key), int(raw_value)


def get_mask_from_line(line: str) -> str:
    return line.split(" = ")[1]


def test_set_mask():
    memory = DockingMemory()
    memory.set_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    assert memory._mask[0] is None
    assert memory._mask[-1] is None
    assert memory._mask[-2] == "0"
    assert memory._mask[-3] is None
    assert memory._mask[-7] == "1"


def test_set_item():
    memory = DockingMemory()
    memory.set_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    memory[0] = 0
    memory[7] = 101
    memory[8] = 11
    assert memory[0] == 64
    assert memory[7] == 101
    assert memory[8] == 73


def test_get_key_value_from_line():
    assert get_key_value_from_line("mem[7186] = 199312871") == (7186, 199312871)


def test_get_mask_from_line():
    assert (
        get_mask_from_line("mask = 101000100011110111X110111011XXX00000")
        == "101000100011110111X110111011XXX00000"
    )


if __name__ == "__main__":
    memory = DockingMemory()
    with open((Path(__file__).parent / "input.txt")) as f:
        for line in f:
            clean_line = line.rstrip("\n")
            if clean_line.startswith("mask"):
                memory.set_mask(get_mask_from_line(clean_line))
            else:
                key, value = get_key_value_from_line(clean_line)
                memory[key] = value

    print(sum(value for value in memory.values()))
