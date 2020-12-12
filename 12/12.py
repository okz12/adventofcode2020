from __future__ import annotations
from dataclasses import dataclass

dirs = ["N", "E", "S", "W"]


@dataclass
class FloatingObject:
    x: int = 0
    y: int = 0

    def run(self, inst: str) -> None:
        op, val = inst[0], int(inst[1:])
        if op in {"L", "R", "F"}:
            self.rotate(op, val)
        else:
            self.move(op, val)

    def rotate(self, op, val):
        raise NotImplementedError

    def move(self, op, val):
        if op == "N":
            self.y += val
        elif op == "S":
            self.y -= val
        elif op == "E":
            self.x += val
        elif op == "W":
            self.x -= val
        else:
            raise ValueError({f"{op} not valid"})

    def m_dist(self):
        return abs(self.x) + abs(self.y)

@dataclass
class Ship(FloatingObject):
    d: str = "E"

    def rotate(self, op, val):
        if op == "L":
            self.d = dirs[dirs.index(self.d) - (val//90)]
        elif op == "R":
            self.d = dirs[(dirs.index(self.d) + (val//90)) % len(dirs)]
        elif op == "F":
            self.move(self.d, val)

    def __str__(self):
        return f"Ship: {self.x}, {self.y} D: {self.d}"

@dataclass
class Waypoint(FloatingObject):
    ship: Ship = None
    x: int = 10
    y: int = 1

    def __init__(self):
        self.ship = Ship()

    def rotate(self, op, val):
        if op == "F":
            self.ship.x += self.x * val
            self.ship.y += self.y * val
        elif val == 180:
            self.x, self.y = -self.x, -self.y
        elif (op, val) == ("L", 90) or (op, val) == ("R", 270):
            #
            self.x, self.y = -self.y, self.x
        elif (op, val) == ("R", 90) or (op, val) == ("L", 270):
            self.x, self.y = self.y, -self.x

    def m_dist(self):
        return self.ship.m_dist()

    def __str__(self):
        return f"Waypoint: {self.x}, {self.y} - {self.ship} "

def find_dist(string:str, fp: FloatingObject) -> int:
    instructions = string.split("\n")
    for i in instructions:
        fp.run(i)
        # print(f"{i}:\t{str(fp)}")
    return fp.m_dist()

if __name__ == "__main__":
    testcase = """\
F10
N3
F7
R90
F11"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert find_dist(testcase, Ship()) == 25
    print(find_dist(data, Ship()))

    assert find_dist(testcase, Waypoint()) == 286
    print(find_dist(data, Waypoint()))
