from pathlib import Path
from typing import List, Tuple, Any, Mapping, Type
from abc import ABC, abstractmethod


class ShipAction(ABC):
    def __init__(self, value: int):
        self._value = value

    def __eq__(self, other: Any):
        if isinstance(other, self.__class__) and self._value == other._value:
            return True
        return False

    @abstractmethod
    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        pass


class MoveSouth(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        return ship.x + self._value, ship.y, ship.direction


class MoveNorth(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        return ship.x - self._value, ship.y, ship.direction


class MoveWest(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        return ship.x, ship.y - self._value, ship.direction


class MoveEast(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        return ship.x, ship.y + self._value, ship.direction


class MoveForward(ShipAction):
    _DIRECTION_TO_ACTION: Mapping[int, Type[ShipAction]] = {
        0: MoveEast,
        90: MoveSouth,
        180: MoveWest,
        270: MoveNorth,
    }

    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        return self._DIRECTION_TO_ACTION[ship.direction](self._value).perform(ship)


class TurnRigth(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        return ship.x, ship.y, (ship.direction + self._value) % 360


class TurnLeft(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[int, int, int]:
        return ship.x, ship.y, (ship.direction - self._value) % 360


class Ship:
    def __init__(self):
        self._x: int = 0
        self._y: int = 0
        self._direction: int = 0

    def __repr__(self) -> str:
        return f"Ship{self.position} - {self.direction}º"

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def direction(self) -> int:
        return self._direction

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def manhattan_distance_from_origin(self) -> int:
        return abs(self.x) + abs(self.y)

    def operate(self, action: ShipAction) -> None:
        self._x, self._y, self._direction = action.perform(self)


def process_actions(actions: List[ShipAction]) -> int:
    ship = Ship()
    for action in actions:
        ship.operate(action)
    return ship.manhattan_distance_from_origin()


def line_to_action(line: str) -> ShipAction:
    CHAR_TO_CLASS: Mapping[str, Type[ShipAction]] = {
        "N": MoveNorth,
        "S": MoveSouth,
        "E": MoveEast,
        "W": MoveWest,
        "F": MoveForward,
        "R": TurnRigth,
        "L": TurnLeft,
    }
    char, value = line[0], int(line[1:])
    return CHAR_TO_CLASS[char](value)


def test_cardinal_move_ship():
    ship = Ship()
    ship.operate(MoveSouth(10))
    ship.operate(MoveNorth(5))
    ship.operate(MoveWest(4))
    ship.operate(MoveEast(1))
    assert ship.position == (5, -3)


def test_forward_rotate_move_ship():
    ship = Ship()
    ship.operate(MoveForward(5))
    ship.operate(TurnLeft(90))
    ship.operate(MoveForward(5))
    ship.operate(TurnRigth(270))
    ship.operate(MoveForward(3))
    assert ship.position == (-5, 2)


def test_manhattan_distance():
    ship = Ship()
    ship.operate(MoveNorth(5))
    ship.operate(MoveEast(10))
    assert ship.manhattan_distance_from_origin() == 15


def test_process_actions():
    assert (
        process_actions(
            [
                MoveForward(10),
                MoveNorth(3),
                MoveForward(7),
                TurnRigth(90),
                MoveForward(11),
            ]
        )
        == 25
    )


def test_line_to_action():
    assert line_to_action("N90") == MoveNorth(90)
    assert line_to_action("S90") == MoveSouth(90)
    assert line_to_action("E90") == MoveEast(90)
    assert line_to_action("W90") == MoveWest(90)
    assert line_to_action("F90") == MoveForward(90)
    assert line_to_action("R90") == TurnRigth(90)
    assert line_to_action("L90") == TurnLeft(90)


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        actions = [line_to_action(line.rstrip("\n")) for line in f]

    print(process_actions(actions))
