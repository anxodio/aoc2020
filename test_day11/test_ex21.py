from pathlib import Path
from typing import List, Any
from collections import Counter


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

    def _get_seat_next_state(self, row_index, col_index) -> str:
        seat = self._rows[row_index][col_index]
        neighbours = self._count_neighbours(row_index, col_index)
        if seat == self.EMPTY and neighbours[self.OCCUPIED] == 0:
            return self.OCCUPIED
        elif seat == self.OCCUPIED and neighbours[self.OCCUPIED] >= 4:
            return self.EMPTY
        return seat

    def _count_neighbours(self, row_index, col_index) -> Counter:
        counter: Counter = Counter()
        for row in self._rows[
            max(row_index - 1, 0) : min(row_index + 2, len(self._rows))
        ]:
            counter.update(row[max(col_index - 1, 0) : col_index + 2])
        counter.subtract({self._rows[row_index][col_index]: 1})
        return counter


def test_count_occupied_seats():
    assert SeatLayout(["#.", "L#"]).count_occupied_seats() == 2


def test_empty_to_occupied():
    seat_layout = SeatLayout(["L.L", "LLL", "L.L"]).get_next_state()
    assert seat_layout.count_occupied_seats() == 7


def test_occupied_to_empty():
    seat_layout = SeatLayout(["..#", "###", "#.#"]).get_next_state()
    assert seat_layout.count_occupied_seats() == 5


def test_equal_seat_layouts():
    assert SeatLayout(["L.L", "LLL"]) == SeatLayout(["L.L", "LLL"])
    assert SeatLayout(["L.L", "LLL"]) != SeatLayout(["#.#", "###"])


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
    assert seat_layout.count_occupied_seats() == 37


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        rows = [line.rstrip("\n") for line in f]

    print(SeatLayout(rows).iterate_until_no_changes().count_occupied_seats())
