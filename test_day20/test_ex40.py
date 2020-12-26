from pathlib import Path
from typing import Set, List, Generator, Any
from itertools import takewhile


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
    def borders(self) -> Set["Border"]:
        return set(
            (
                Border("up", self._data[0], False),
                Border("up", self._data[0][::-1], True),
                Border("down", self._data[-1], False),
                Border("down", self._data[-1][::-1], True),
                Border("left", "".join(row[0] for row in self._data), False),
                Border("left", "".join(row[0] for row in self._data)[::-1], True),
                Border("right", "".join(row[-1] for row in self._data), False),
                Border("right", "".join(row[-1] for row in self._data)[::-1], True),
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


class Border:
    def __init__(self, name: str, data: str, inverted: bool) -> None:
        self.name = name
        self.data = data
        self.inverted = inverted

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Border):
            return False
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def __repr__(self) -> str:
        return f"Border({self.name}, Inverted: {self.inverted})"


class Image:
    def __init__(self) -> None:
        self._data: List[str] = []


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
        Border("up", "..##.#..#.", False),
        Border("up", ".#..#.##..", True),
        Border("down", ".#####..#.", False),
        Border("down", ".#..#####.", True),
        Border("left", "...#.##..#", False),
        Border("left", "#..##.#...", True),
        Border("right", "..###..###", False),
        Border("right", "###..###..", True),
    }


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
    # TO BE CONTINUED
