from typing import List, Dict

import pytest


def play_memory_game(starting_numbers: List[int]) -> int:
    # Optimized version of ex29, ~10 seconds to 30 millions
    last_spoken = starting_numbers[-1]
    memory: Dict[int, int] = {num: i for i, num in enumerate(starting_numbers[:-1])}
    for i in range(len(starting_numbers), 30000000):
        last_index = memory.get(last_spoken, None)
        memory[last_spoken] = i - 1
        last_spoken = 0 if last_index is None else i - last_index - 1
    return last_spoken


@pytest.mark.skip("Slow test, run it manually 🙏")
def test_play_memory_game():
    assert play_memory_game([1, 2, 3]) == 261214


if __name__ == "__main__":
    print(play_memory_game([13, 16, 0, 12, 15, 1]))
