from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

from typing import List

class state(Enum):
    floor = auto()
    empty = auto()
    occupied = auto()
    empty_to_occupied = auto()
    occupied_to_empty = auto()

    @classmethod
    def from_str(cls, label):
        map = {'L': cls.empty,
               '.': cls.floor,
               '#': cls.occupied}
        if label in map:
            return map[label]
        raise NotImplementedError

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        map = {"empty": "L", "floor": ".", "occupied": "#",
               "occupied_to_empty": "E", "empty_to_occupied": "O"}
        return map[self.name]

    @classmethod
    def update(cls, label):
        map = {cls.empty_to_occupied: cls.occupied,
               cls.occupied_to_empty: cls.empty}
        return map.get(label, label)


directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

@dataclass
class seatMap:
    seats : List[List[state]]
    nrows : int
    ncols : int
    stable : bool

    @staticmethod
    def parse(string: str) -> seatMap:
        seats = [list(map(state.from_str, list(x))) for x in string.split("\n")]
        return seatMap(seats, len(seats), len(seats[0]), False)

    def iter(self, mode: str = "adjacent"):
        if mode == "adjacent":
            count_func = self.count_adjacent
            val = 4
        else:
            count_func = self.count_across
            val = 5

        self.stable = True
        for y in range(self.nrows):
            for x in range(self.ncols):
                if self.seats[y][x] == state.empty and count_func(x, y) == 0:
                    self.seats[y][x] = state.empty_to_occupied
                    self.stable = False
                elif self.seats[y][x] == state.occupied and count_func(x, y) >= val:
                    self.seats[y][x] = state.occupied_to_empty
                    self.stable = False

        for y in range(self.nrows):
            for x in range(self.ncols):
                self.seats[y][x] = state.update(self.seats[y][x])

    def count_adjacent(self, x, y) -> int:
        adjacent_seats = 0
        for x_add, y_add in directions:
            x_, y_ = x + x_add, y + y_add
            if 0 <= x_ < self.ncols and 0 <= y_ < self.nrows:
                adjacent_seats += self.seats[y_][x_] == state.occupied or self.seats[y_][x_] == state.occupied_to_empty
        return adjacent_seats

    def count_across(self, x, y) -> int:
        across_seats = 0
        for x_add, y_add in directions:
            x_, y_ = x + x_add, y + y_add
            while 0 <= x_ < self.ncols and 0 <= y_ < self.nrows:
                if self.seats[y_][x_] in {state.occupied, state.empty, state.occupied_to_empty, state.empty_to_occupied}:
                    across_seats += self.seats[y_][x_] == state.occupied or self.seats[y_][x_] == state.occupied_to_empty
                    break
                x_, y_ = x_ + x_add, y_ + y_add
        return across_seats

    def run(self, mode: str = "adjacent") -> int:
        self.stable = False
        while not self.stable:
            self.iter(mode=mode)
        return sum(self.seats[y][x] == state.occupied for x in range(self.ncols) for y in range(self.nrows))

    def __repr__(self):
        return f"[{self.ncols}x{self.nrows}] - {'Stable' if self.stable else 'Unstable'}\n" + \
               "\n".join(" ".join(str(y) for y in x) for x in self.seats)


if __name__ == "__main__":
    testcase = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert seatMap.parse(testcase).run() == 37
    print(seatMap.parse(data).run())

    assert seatMap.parse(testcase).run("across") == 26
    print(seatMap.parse(data).run("across"))


