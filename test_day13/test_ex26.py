from pathlib import Path
from typing import Dict
import functools
import operator


# It looked like a mathematical problem, I had to search it and I discovered
# in the reddit that is a https://en.wikipedia.org/wiki/Chinese_remainder_theorem
# I just adapted one implementation, but... I don't understand it a lot D:
def find_eatliest_timestamp(shuttles: Dict[int, int]) -> int:
    shuttle_ids = list(shuttles.values())
    remainders = [(shuttle - pos) % shuttle for pos, shuttle in shuttles.items()]
    product = functools.reduce(operator.mul, [shuttle for shuttle in shuttle_ids], 1)
    B = [product // shuttle for shuttle in shuttle_ids]
    x = [pow(Bi, -1, shuttle) for Bi, shuttle in zip(B, shuttle_ids)]
    sum_list = [Bi * xi * reminder for Bi, xi, reminder in zip(B, x, remainders)]
    return functools.reduce(operator.add, sum_list, 0) % product


def test_find_eatliest_timestamp():
    assert find_eatliest_timestamp({0: 3, 1: 5}) == 9
    assert find_eatliest_timestamp({0: 17, 2: 13, 3: 19}) == 3417
    assert find_eatliest_timestamp({0: 7, 1: 13, 4: 59, 6: 31, 7: 19}) == 1068781


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        _ = next(f)
        shuttles = {
            i: int(shuttle)
            for i, shuttle in enumerate(next(f).split(","))
            if shuttle != "x"
        }

    print(find_eatliest_timestamp(shuttles))
