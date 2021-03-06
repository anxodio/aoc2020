from pathlib import Path
from typing import List, Set
from dataclasses import dataclass
from collections import UserDict

import pytest


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int
    z: int
    w: int

    @property
    def neighbours(self) -> Set["Coordinates"]:
        return {
            Coordinates(x, y, z, w)
            for x in range(self.x - 1, self.x + 2)
            for y in range(self.y - 1, self.y + 2)
            for z in range(self.z - 1, self.z + 2)
            for w in range(self.w - 1, self.w + 2)
            if Coordinates(x, y, z, w) != self
        }


class PocketDimension(UserDict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, coordinates: Coordinates) -> bool:
        return self.data.get(coordinates, False)

    def __setitem__(self, coordinates: Coordinates, state: bool) -> None:
        self.data[coordinates] = state

    def next_cycle(self) -> "PocketDimension":
        new = PocketDimension()
        to_analyze = set(self.data.keys()).union(
            *(coodinates.neighbours for coodinates in self.data.keys())
        )
        for coordinates in to_analyze:
            active_neighbours = sum(
                self[neighbour] for neighbour in coordinates.neighbours
            )
            new[coordinates] = (not self[coordinates] and active_neighbours == 3) or (
                self[coordinates] and active_neighbours in (2, 3)
            )
        return new

    def count_active_cubes(self) -> int:
        return sum(self.data.values())


def build_pocket_dimension_from_lines(lines: List[str]) -> PocketDimension:
    dimension = PocketDimension()
    for x, line in enumerate(lines):
        for y, state in enumerate(line):
            dimension[Coordinates(x, y, 0, 0)] = state == "#"
    return dimension


def test_empty_pocket_dimension() -> None:
    dimension = PocketDimension()
    assert dimension[Coordinates(0, 0, 0, 0)] is False
    assert dimension[Coordinates(42, -3, 125, 0)] is False


def test_fill_pocket_dimension() -> None:
    dimension = PocketDimension()
    dimension[Coordinates(1, -1, 0, 1)] = True
    assert dimension[Coordinates(0, 0, 0, 0)] is False
    assert dimension[Coordinates(1, -1, 0, 1)] is True


def test_build_pocket_dimension_from_lines() -> None:
    dimension = build_pocket_dimension_from_lines([".#.", "..#", "###"])
    assert dimension[Coordinates(0, 0, 0, 0)] is False
    assert dimension[Coordinates(0, 1, 0, 0)] is True
    assert dimension[Coordinates(1, 2, 0, 0)] is True
    assert dimension[Coordinates(2, 0, 0, 0)] is True
    assert dimension[Coordinates(3, 1, 0, 0)] is False


def test_get_coordinates_neighbours() -> None:
    neighbours = Coordinates(0, 0, 0, 0).neighbours
    assert Coordinates(0, 0, 0, 0) not in neighbours
    assert Coordinates(-1, -1, -1, -1) in neighbours
    assert Coordinates(-1, -1, -1, -2) not in neighbours
    assert Coordinates(-1, 1, 0, -1) in neighbours
    assert Coordinates(-1, 1, 0, 0) in neighbours
    assert Coordinates(-1, 1, 0, 1) in neighbours


def test_fast_pocket_dimension_count_active() -> None:
    dimension = build_pocket_dimension_from_lines([".#.", "..#", "###"])
    dimension = dimension.next_cycle()
    assert dimension.count_active_cubes() == 29


@pytest.mark.skip("Slow test, run it manually 🙏")
def test_pocket_dimension_count_active() -> None:
    dimension = build_pocket_dimension_from_lines([".#.", "..#", "###"])
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    assert dimension.count_active_cubes() == 848


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]

    # Slow, it lasts ~1m20s
    dimension = build_pocket_dimension_from_lines(lines)
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    dimension = dimension.next_cycle()
    print(dimension.count_active_cubes())
