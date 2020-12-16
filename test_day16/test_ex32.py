import re
import functools
import operator
from pathlib import Path
from typing import List, Set, Dict
from collections import defaultdict


Ticket = List[int]


class TicketValidation:
    def __init__(self, name: str, valid_numbers: Set[int]) -> None:
        self._name = name
        self._valid_numbers = valid_numbers

    @staticmethod
    def build_from_line(line: str) -> "TicketValidation":
        match = re.match(r"([\w\s]*): (\d*)-(\d*) or (\d*)-(\d*)", line)
        name, low_start, low_end, high_start, high_end = match.group(1, 2, 3, 4, 5)  # type: ignore
        return TicketValidation(
            name,
            {n for n in range(int(low_start), int(low_end) + 1)}
            ^ {n for n in range(int(high_start), int(high_end) + 1)},
        )

    @property
    def name(self) -> str:
        return self._name

    def is_valid(self, number: int) -> bool:
        return number in self._valid_numbers


def find_invalid_ticket_fields(
    ticket: Ticket, validations: List[TicketValidation]
) -> List[int]:
    return [
        field
        for field in ticket
        if not any(validation.is_valid(field) for validation in validations)
    ]


def guess_field_order(
    tickets: List[Ticket], validations: List[TicketValidation]
) -> List[str]:
    # I tried backtracking, but was infinite... and seems like greedy matching
    # works for this exercise :D
    possible_positions = _get_all_possible_positions(tickets, validations)
    less_to_more_possibilities = [
        key
        for key in sorted(
            possible_positions.keys(), key=lambda k: len(possible_positions[k])
        )
    ]

    field_order = [""] * len(validations)
    used_indexes: Set[int] = set()
    for key in less_to_more_possibilities:
        index = (possible_positions[key] - used_indexes).pop()
        used_indexes.add(index)
        field_order[index] = key

    return field_order


def _get_all_possible_positions(
    tickets: List[Ticket], validations: List[TicketValidation]
) -> Dict[str, Set[int]]:
    possible_positions: Dict[str, Set[int]] = defaultdict(set)
    for validation in validations:
        validation_matrix = [
            [validation.is_valid(field) for field in ticket] for ticket in tickets
        ]
        trasposed = zip(*validation_matrix)
        for i in (i for i, col in enumerate(trasposed) if all(col)):
            possible_positions[validation.name].add(i)
    return possible_positions


def test_ticket_validation():
    validation = TicketValidation("class", {1, 2, 3, 5, 6, 7})
    assert validation.is_valid(3) is True
    assert validation.is_valid(4) is False


def test_ticket_validation_build_from_line():
    validation = TicketValidation.build_from_line("row: 6-11 or 33-44")
    assert validation.is_valid(5) is False
    assert validation.is_valid(6) is True
    assert validation.is_valid(11) is True
    assert validation.is_valid(12) is False
    assert validation.is_valid(32) is False
    assert validation.is_valid(33) is True
    assert validation.is_valid(44) is True
    assert validation.is_valid(45) is False


def test_find_invalid_ticket_fields():
    validations = [
        TicketValidation.build_from_line("class: 1-3 or 5-7"),
        TicketValidation.build_from_line("row: 6-11 or 33-44"),
        TicketValidation.build_from_line("seat: 13-40 or 45-50"),
    ]
    assert find_invalid_ticket_fields([7, 3, 47], validations) == []
    assert find_invalid_ticket_fields([40, 4, 50], validations) == [4]
    assert find_invalid_ticket_fields([55, 2, 20], validations) == [55]
    assert find_invalid_ticket_fields([38, 6, 12], validations) == [12]


def test_guess_field_order():
    validations = [
        TicketValidation.build_from_line("class: 0-1 or 4-19"),
        TicketValidation.build_from_line("row: 0-5 or 8-19"),
        TicketValidation.build_from_line("seat: 0-13 or 16-19"),
    ]
    assert guess_field_order(
        [[11, 12, 13], [3, 9, 18], [15, 1, 5], [5, 14, 9]], validations
    ) == ["row", "class", "seat"]


if __name__ == "__main__":
    validations = []
    tickets = []
    with open((Path(__file__).parent / "input.txt")) as f:
        for line in f:
            clean_line = line.rstrip("\n")
            if clean_line in ["", "your ticket:", "nearby tickets:"]:
                continue
            if clean_line[0].isnumeric():
                tickets.append([int(field) for field in clean_line.split(",")])
            else:
                validations.append(TicketValidation.build_from_line(clean_line))
    my_ticket, tickets = tickets[0], tickets[1:]
    valid_tickets = [
        ticket
        for ticket in tickets
        if not find_invalid_ticket_fields(ticket, validations)
    ]
    field_names = guess_field_order([my_ticket] + valid_tickets, validations)

    departure_values = [
        my_ticket[field_names.index(field_name)]
        for field_name in (
            "departure location",
            "departure station",
            "departure platform",
            "departure track",
            "departure date",
            "departure time",
        )
    ]
    print(
        functools.reduce(
            operator.mul,
            departure_values,
        )
    )
