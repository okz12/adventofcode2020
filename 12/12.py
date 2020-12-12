from __future__ import annotations
from typing import List

dir_map = {"N": 1j, "E": 1, "S": -1j, "W": -1, "L": 1j, "R": -1j}

class WaypointAndShip:

    def __init__(self, ship: complex = 0 + 0j, waypoint: complex = 1 + 0j, move_waypoint: bool = False):
        self.ship = ship
        self.waypoint = waypoint
        self.move_waypoint = move_waypoint

    def run(self, instructions: List[str]) -> int:
        for inst in instructions:
            op, val = inst[0], int(inst[1:])
            if op in {"L", "R"}:
                self.waypoint *= (dir_map[op] ** (val // 90))
            elif op == "F":
                self.ship += self.waypoint * val
            elif op in {'N', 'E', 'S', 'W'}:
                if self.move_waypoint:
                    self.waypoint += dir_map[op] * val
                else:
                    self.ship += dir_map[op] * val
            else:
                raise ValueError (f"{op} not a valid command")
            # print(f"{inst}:\t{self}")
        return int(abs(self.ship.real) + abs(self.ship.imag))

    def __str__(self) -> str:
        return f"Ship: {int(self.ship.real)}, {int(self.ship.imag)} \tWaypoint: {int(self.waypoint.real)}, {int(self.waypoint.imag)}"


if __name__ == "__main__":
    testcase = """\
F10
N3
F7
R90
F11"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert WaypointAndShip().run(testcase.split("\n")) == 25
    print(WaypointAndShip().run(data.split("\n")))

    assert WaypointAndShip(waypoint = 10 + 1j, move_waypoint = True).run(testcase.split("\n")) == 286
    print(WaypointAndShip(waypoint = 10 + 1j, move_waypoint = True).run(data.split("\n")))
