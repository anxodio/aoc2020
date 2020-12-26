from pathlib import Path
from typing import Set, List, Generator, Any
from itertools import takewhile, combinations
import functools
import operator


class Tile:
    def __init__(self, tile_id: int, tile_data: List[str]) -> None:
        self._id = tile_id
        self._data = tile_data
        self._adjacent_tiles: Set[Tile] = set()

    @staticmethod
    def from_chunk_of_lines(chunk: List[str]) -> "Tile":
        tile_id = int(chunk[0][5:-1])
        tile_data = chunk[1:]
        return Tile(tile_id, tile_data)

    @property
    def id(self) -> int:
        return self._id

    @property
    def borders(self) -> Set[str]:
        return set(
            (
                self._data[0],
                self._data[0][::-1],
                self._data[-1],
                self._data[-1][::-1],
                "".join(row[0] for row in self._data),
                "".join(row[0] for row in self._data)[::-1],
                "".join(row[-1] for row in self._data),
                "".join(row[-1] for row in self._data)[::-1],
            )
        )

    @property
    def adjacent_tiles(self) -> Set["Tile"]:
        return self._adjacent_tiles

    def is_adjacent_tile(self, other: "Tile") -> bool:
        return self != other and bool(len(self.borders & other.borders))

    def add_adjacent_tile(self, other: "Tile") -> None:
        self._adjacent_tiles.add(other)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Tile):
            return False
        return self._id == other._id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Tile({self.id})"


def find_tileset_corner_multiplication(tileset: List[Tile]) -> int:
    for tile1, tile2 in combinations(tileset, 2):
        if tile1.is_adjacent_tile(tile2):
            tile1.add_adjacent_tile(tile2)
            tile2.add_adjacent_tile(tile1)
    corners = [tile for tile in tileset if len(tile.adjacent_tiles) == 2]
    return functools.reduce(operator.mul, (corner.id for corner in corners), 1)


def generate_chunks_of_lines(raw_lines: List[str]) -> Generator[List[str], None, None]:
    raw_lines_iterator = iter(raw_lines)
    while (lines := list(takewhile(lambda line: line != "", raw_lines_iterator))) :
        yield lines


def test_build_tile_from_chunk_of_lines() -> None:
    tile = Tile.from_chunk_of_lines(
        [
            "Tile 2311:",
            "..##.#..#.",
            "##..#.....",
            "#...##..#.",
            "####.#...#",
            "##.##.###.",
            "##...#.###",
            ".#.#.#..##",
            "..#....#..",
            "###...#.#.",
            "..###..###",
        ]
    )
    assert tile.id == 2311
    assert tile.borders == {
        "..##.#..#.",
        ".#..#.##..",
        ".#####..#.",
        ".#..#####.",
        "...#.##..#",
        "#..##.#...",
        "..###..###",
        "###..###..",
    }


def test_find_tileset_corner_multiplication() -> None:
    with open((Path(__file__).parent / "input_test.txt")) as f:
        raw_lines = [line.rstrip("\n") for line in f]

    tiles = [
        Tile.from_chunk_of_lines(chunk_of_lines)
        for chunk_of_lines in generate_chunks_of_lines(raw_lines)
    ]
    assert find_tileset_corner_multiplication(tiles) == 20899048083289


def test_generate_chunks_of_lines() -> None:
    assert list(
        generate_chunks_of_lines(["a", "b", "", "c", "d", "", "e", "f", "g"])
    ) == [["a", "b"], ["c", "d"], ["e", "f", "g"]]


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        raw_lines = [line.rstrip("\n") for line in f]

    tiles = [
        Tile.from_chunk_of_lines(chunk_of_lines)
        for chunk_of_lines in generate_chunks_of_lines(raw_lines)
    ]
    print(find_tileset_corner_multiplication(tiles))
