from pathlib import Path


def letters_to_position(letters: str) -> int:
    mapper = letters.maketrans("BRFL", "1100")
    return int(letters.translate(mapper), 2)


def get_seat_id(letters: str) -> int:
    row = letters_to_position(letters[0:7])
    col = letters_to_position(letters[7:])
    return row * 8 + col


def test_letters_to_position():
    assert letters_to_position("BBFFBBF") == 102
    assert letters_to_position("RLL") == 4


def test_get_seat_id():
    assert get_seat_id("BFFFBBFRRR") == 567
    assert get_seat_id("FFFBBBFRRR") == 119


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        seat_ids = [get_seat_id(line.rstrip("\n")) for line in f]
    max_id = max(seat_ids)
    missing_ids = [seat_id for seat_id in range(max_id) if seat_id not in seat_ids]
    print(missing_ids)  # manually see the different seat, it's easy :P
