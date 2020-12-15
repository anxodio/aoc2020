from typing import List


def play_memory_game(starting_numbers: List[int]) -> int:
    memory = starting_numbers.copy()
    for i in range(len(memory), 2020):
        try:
            last_index = len(memory) - memory[-2::-1].index(memory[i - 1]) - 1
            memory.append(i - last_index)
        except ValueError:
            memory.append(0)
    return memory[-1]


def test_play_memory_game():
    assert play_memory_game([0, 3, 6]) == 436
    assert play_memory_game([1, 2, 3]) == 27
    assert play_memory_game([3, 1, 2]) == 1836


if __name__ == "__main__":
    print(play_memory_game([13, 16, 0, 12, 15, 1]))
