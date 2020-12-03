from pathlib import Path
from typing import List
from collections import UserList
from itertools import count


class TreeRow(UserList):
    def __getitem__(self, key: int) -> str:
        return self.data[key % len(self.data)]


TreeMap = list[TreeRow]


def slope_tree_count(treemap: TreeMap, right: int, down: int) -> int:
    col = count(right, right)
    return sum(1 for treerow in treemap[down::down] if treerow[next(col)] == "#")


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
    assert slope_tree_count(treemap, 1, 1) == 2
    assert slope_tree_count(treemap, 3, 1) == 7
    assert slope_tree_count(treemap, 5, 1) == 3
    assert slope_tree_count(treemap, 7, 1) == 4
    assert slope_tree_count(treemap, 1, 2) == 2


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        treemap = [TreeRow(line.rstrip("\n")) for line in f]
    a = slope_tree_count(treemap, 1, 1)
    b = slope_tree_count(treemap, 3, 1)
    c = slope_tree_count(treemap, 5, 1)
    d = slope_tree_count(treemap, 7, 1)
    e = slope_tree_count(treemap, 1, 2)

    print(a, b, c, d, e)
    print(a * b * c * d * e)
