from pathlib import Path
from typing import List, Tuple, Any, Mapping, Type, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int


class ShipAction(ABC):
    def __init__(self, value: int):
        self._value = value

    def __eq__(self, other: Any):
        if isinstance(other, self.__class__) and self._value == other._value:
            return True
        return False

    @abstractmethod
    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        pass


class MoveWaypointSouth(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        return ship.position, Coordinates(
            ship.waypoint.x + self._value, ship.waypoint.y
        )


class MoveWaypointNorth(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        return ship.position, Coordinates(
            ship.waypoint.x - self._value, ship.waypoint.y
        )


class MoveWaypointWest(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        return ship.position, Coordinates(
            ship.waypoint.x, ship.waypoint.y - self._value
        )


class MoveWaypointEast(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        return ship.position, Coordinates(
            ship.waypoint.x, ship.waypoint.y + self._value
        )


class MoveShipToWaypoint(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        return (
            Coordinates(
                ship.position.x + (ship.waypoint.x * self._value),
                ship.position.y + (ship.waypoint.y * self._value),
            ),
            ship.waypoint,
        )


class RotateWaypointClockwise(ShipAction):
    _DEGREES_TO_FN: Mapping[int, Callable[[Coordinates], Coordinates]] = {
        90: lambda waypoint: Coordinates(waypoint.y, waypoint.x * -1),
        180: lambda waypoint: Coordinates(waypoint.x * -1, waypoint.y * -1),
        270: lambda waypoint: Coordinates(waypoint.y * -1, waypoint.x),
    }

    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        return ship.position, self._DEGREES_TO_FN[self._value](ship.waypoint)


class RotateWaypointCounterclockwise(ShipAction):
    def perform(self, ship: "Ship") -> Tuple[Coordinates, Coordinates]:
        return RotateWaypointClockwise((self._value * -1) % 360).perform(ship)


class Ship:
    def __init__(self):
        self._position: Coordinates = Coordinates(0, 0)
        self._waypoint: Coordinates = Coordinates(-1, 10)

    def __repr__(self) -> str:
        return f"Ship{self.position} - Waypoint{self.waypoint}"

    @property
    def position(self) -> Coordinates:
        return self._position

    @property
    def waypoint(self) -> Coordinates:
        return self._waypoint

    def manhattan_distance_from_origin(self) -> int:
        return abs(self.position.x) + abs(self.position.y)

    def operate(self, action: ShipAction) -> None:
        self._position, self._waypoint = action.perform(self)


def process_actions(actions: List[ShipAction]) -> int:
    ship = Ship()
    for action in actions:
        ship.operate(action)
    return ship.manhattan_distance_from_origin()


def line_to_action(line: str) -> ShipAction:
    CHAR_TO_CLASS: Mapping[str, Type[ShipAction]] = {
        "N": MoveWaypointNorth,
        "S": MoveWaypointSouth,
        "E": MoveWaypointEast,
        "W": MoveWaypointWest,
        "F": MoveShipToWaypoint,
        "R": RotateWaypointClockwise,
        "L": RotateWaypointCounterclockwise,
    }
    char, value = line[0], int(line[1:])
    return CHAR_TO_CLASS[char](value)


def test_waypoint_movement():
    ship = Ship()
    ship.operate(MoveWaypointNorth(4))
    ship.operate(RotateWaypointCounterclockwise(270))
    assert ship.waypoint == Coordinates(10, 5)


def test_move_to_waypoint():
    ship = Ship()
    ship.operate(MoveShipToWaypoint(2))
    ship.operate(MoveShipToWaypoint(3))
    assert ship.position == Coordinates(-5, 50)


def test_process_actions():
    assert (
        process_actions(
            [
                MoveShipToWaypoint(10),
                MoveWaypointNorth(3),
                MoveShipToWaypoint(7),
                RotateWaypointClockwise(90),
                MoveShipToWaypoint(11),
            ]
        )
        == 286
    )


def test_line_to_action():
    assert line_to_action("N90") == MoveWaypointNorth(90)
    assert line_to_action("S90") == MoveWaypointSouth(90)
    assert line_to_action("E90") == MoveWaypointEast(90)
    assert line_to_action("W90") == MoveWaypointWest(90)
    assert line_to_action("F90") == MoveShipToWaypoint(90)
    assert line_to_action("R90") == RotateWaypointClockwise(90)
    assert line_to_action("L90") == RotateWaypointCounterclockwise(90)


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        actions = [line_to_action(line.rstrip("\n")) for line in f]

    print(process_actions(actions))
