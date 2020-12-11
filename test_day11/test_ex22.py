from pathlib import Path
from typing import List, Any, Generator, Tuple


class SeatLayout:
    FLOOR = "."
    OCCUPIED = "#"
    EMPTY = "L"

    def __init__(self, rows: List[str]):
        self._rows = rows

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SeatLayout):
            return False
        return self._rows == other._rows

    def count_occupied_seats(self) -> int:
        return sum(1 for row in self._rows for seat in row if seat == self.OCCUPIED)

    def iterate_until_no_changes(self) -> "SeatLayout":
        actual_state = self
        while True:
            next_state = actual_state.get_next_state()
            if actual_state == next_state:
                break
            actual_state = next_state
        return actual_state

    def get_next_state(self) -> "SeatLayout":
        return SeatLayout(
            [
                "".join(
                    [
                        self._get_seat_next_state(row_index, col_index)
                        for col_index in range(len(self._rows[row_index]))
                    ]
                )
                for row_index in range(len(self._rows))
            ]
        )

    def _get_seat_next_state(self, row_index: int, col_index: int) -> str:
        seat = self._rows[row_index][col_index]
        visible_seats = self._count_visible_occupied_seats(row_index, col_index)
        if seat == self.EMPTY and visible_seats == 0:
            return self.OCCUPIED
        elif seat == self.OCCUPIED and visible_seats >= 5:
            return self.EMPTY
        return seat

    def _count_visible_occupied_seats(self, row_index: int, col_index: int) -> int:
        row_length = len(self._rows)
        col_length = len(self._rows[row_index])

        def _asc_range(actual_index: int, max_index: int):
            return range(actual_index + 1, max_index)

        def _desc_range(actual_index: int):
            return range(actual_index - 1, -1, -1)

        down_direction = ((i, col_index) for i in _asc_range(row_index, row_length))
        up_direction = ((i, col_index) for i in _desc_range(row_index))
        right_direction = ((row_index, j) for j in _asc_range(col_index, col_length))
        left_direction = ((row_index, j) for j in _desc_range(col_index))
        downright_direction = (
            (i, j)
            for i, j in zip(
                _asc_range(row_index, row_length),
                _asc_range(col_index, col_length),
            )
        )
        downleft_direction = (
            (i, j)
            for i, j in zip(_asc_range(row_index, row_length), _desc_range(col_index))
        )
        upright_direction = (
            (i, j)
            for i, j in zip(_desc_range(row_index), _asc_range(col_index, col_length))
        )
        upleft_direction = (
            (i, j) for i, j in zip(_desc_range(row_index), _desc_range(col_index))
        )

        return sum(
            self._direction_has_visible_occupied_seat(direction)
            for direction in [
                down_direction,
                up_direction,
                right_direction,
                left_direction,
                downright_direction,
                downleft_direction,
                upright_direction,
                upleft_direction,
            ]
        )

    def _direction_has_visible_occupied_seat(
        self, direction: Generator[Tuple[int, int], None, None]
    ) -> bool:
        for row_index, col_index in direction:
            seat = self._rows[row_index][col_index]
            if seat == self.EMPTY:
                return False
            elif seat == self.OCCUPIED:
                return True
        return False


def test_count_occupied_seats():
    assert SeatLayout(["#.", "L#"]).count_occupied_seats() == 2


def test_equal_seat_layouts():
    assert SeatLayout(["L.L", "LLL"]) == SeatLayout(["L.L", "LLL"])
    assert SeatLayout(["L.L", "LLL"]) != SeatLayout(["#.#", "###"])


def test_count_in_eight_directions():
    seat_layout = SeatLayout(
        [
            ".......#.",
            "...#.....",
            ".#.......",
            ".........",
            "..#L....#",
            "....#....",
            ".........",
            "#........",
            "...#.....",
        ]
    )
    assert seat_layout._count_visible_occupied_seats(4, 3) == 8

    seat_layout = SeatLayout(
        [
            ".##.##.",
            "#.#.#.#",
            "##...##",
            "...L...",
            "##...##",
            "#.#.#.#",
            ".##.##.",
        ]
    )
    assert seat_layout._count_visible_occupied_seats(3, 3) == 0


def test_free_seat_stops_visibility():
    seat_layout = SeatLayout(
        [
            ".............",
            ".L.L.#.#.#.#.",
            ".............",
        ]
    )
    assert seat_layout._count_visible_occupied_seats(1, 1) == 0


def test_final_occupied_count():
    seat_layout = SeatLayout(
        [
            "L.LL.LL.LL",
            "LLLLLLL.LL",
            "L.L.L..L..",
            "LLLL.LL.LL",
            "L.LL.LL.LL",
            "L.LLLLL.LL",
            "..L.L.....",
            "LLLLLLLLLL",
            "L.LLLLLL.L",
            "L.LLLLL.LL",
        ]
    )
    seat_layout = seat_layout.iterate_until_no_changes()
    assert seat_layout.count_occupied_seats() == 26


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        rows = [line.rstrip("\n") for line in f]

    print(SeatLayout(rows).iterate_until_no_changes().count_occupied_seats())
