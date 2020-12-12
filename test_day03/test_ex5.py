from pathlib import Path
from typing import List, Any
from collections import UserList
from itertools import count


class TreeRow(UserList):
    def __getitem__(self, key: Any) -> Any:
        return self.data[key % len(self.data)]


TreeMap = List[TreeRow]


def slope_tree_count(treemap: TreeMap) -> int:
    col = count(3, 3)
    return sum(1 for treerow in treemap[1:] if treerow[next(col)] == "#")


def test_treerow_existing_positions():
    treerow = TreeRow("..##.")
    assert treerow[0] == "."
    assert treerow[2] == "#"


def test_treerow_far_positions():
    treerow = TreeRow("..##.")
    assert treerow[5] == "."
    assert treerow[13] == "#"


def test_treemap_access():
    treemap = [TreeRow("..##."), TreeRow("#...#")]
    assert treemap[1][9] == "#"


def test_treemap_slope_tree_count():
    treemap = [
        TreeRow("..##......."),
        TreeRow("#...#...#.."),
        TreeRow(".#....#..#."),
        TreeRow("..#.#...#.#"),
        TreeRow(".#...##..#."),
        TreeRow("..#.##....."),
        TreeRow(".#.#.#....#"),
        TreeRow(".#........#"),
        TreeRow("#.##...#..."),
        TreeRow("#...##....#"),
        TreeRow(".#..#...#.#"),
    ]
    assert slope_tree_count(treemap) == 7


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        treemap = [TreeRow(line.rstrip("\n")) for line in f]
    print(slope_tree_count(treemap))
