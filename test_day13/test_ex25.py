from pathlib import Path
from typing import List
import math


def find_id_x_waiting(min_time: int, shuttles: List[int]) -> int:
    decimal_parts = [math.modf(min_time / shuttle)[0] for shuttle in shuttles]
    faster_pos = decimal_parts.index(max(decimal_parts))
    faster_shutter = shuttles[faster_pos]
    wait_time = (math.ceil(min_time / faster_shutter) * faster_shutter) - min_time
    return faster_shutter * wait_time


def test_find_id_x_waiting():
    assert find_id_x_waiting(939, [7, 13, 59, 31, 19]) == 295


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        min_time = int(next(f).rstrip("\n"))
        shuttles = [int(shuttle) for shuttle in next(f).split(",") if shuttle != "x"]

    print(find_id_x_waiting(min_time, shuttles))
