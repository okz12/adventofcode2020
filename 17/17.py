from __future__ import annotations
from dataclasses import dataclass
import itertools
from typing import Tuple, List, Set

Point = Tuple[int, int, int, int]
Range = Tuple[int, int]


# Can be replaced by itertools.product
def grid_gen(X: Range, Y: Range, Z: Range, W: Range) -> List[Point]:
    return [
        (x, y, z, w)
        for w in range(W[0], W[1] + 1)
        for z in range(Z[0], Z[1] + 1)
        for y in range(Y[0], Y[1] + 1)
        for x in range(X[0], X[1] + 1)
    ]


@dataclass
class Grid:
    active: Set[Point]
    w_dim: bool

    @staticmethod
    def parse(string: str, w_dim: bool = False) -> Grid:
        grid = {
            (x, y, 0, 0)
            for y, line in enumerate(string.split("\n"))
            for x, char in enumerate(list(line))
            if char == "#"
        }
        return Grid(grid, w_dim)

    def cycle(self) -> None:
        x_, y_, z_, w_ = list(zip(*self.active))
        to_add, to_remove = set(), set()
        for point in itertools.product(
            range(min(x_) - 1, max(x_) + 2),
            range(min(y_) - 1, max(y_) + 2),
            range(
                max(min(z_) - 1, 0), max(z_) + 2
            ),  # opt 1: mirrored z and w dims, start from zero
            range(max(min(w_) - 1, 0), max(w_) + 2) if self.w_dim else range(0, 1),
        ):
            if point in self.active:
                if not (2 <= self.count_adjacent(*point) <= 3):
                    to_remove.add(point)
            elif self.count_adjacent(*point) == 3:
                to_add.add(point)

        self.active = self.active.difference(to_remove).union(to_add)

    def count_adjacent(self, x: int, y: int, z: int, w: int = 0) -> int:
        adjacent_cubes = 0
        for (x_, y_, z_, w_) in itertools.product(
            range(x - 1, x + 2),
            range(y - 1, y + 2),
            range(z - 1, z + 2),
            range(w - 1, w + 2) if self.w_dim else range(0, 1),
        ):
            if not (x_, y_, z_, w_) == (x, y, z, w):
                adjacent_cubes += 1 if (x_, y_, abs(z_), abs(w_)) in self.active else 0
                if adjacent_cubes > 3:  # optimization 2: don't count beyond 4
                    return adjacent_cubes
        return adjacent_cubes

    def run(self, cycles) -> int:
        for _ in range(cycles):
            self.cycle()
        # optimization 1: Planes are mirrored - count 1x for z & w == 0, 2x for z or w == 0, 4x for the rest
        return sum(2 ** (int(w != 0) + int(z != 0)) for (_, _, z, w) in self.active)

    def __repr__(self):
        grid = ""
        x_, y_, z_, w_ = list(zip(*self.active))
        for w in range(min(w_), max(w_) + 1):
            for z in range(min(z_), max(z_) + 1):
                grid += (
                    f"\n\nz={z} w={w} y=[{min(y_)}-{max(y_)}] x=[{min(x_)}-{max(x_)}]"
                )
                for y in range(min(y_), max(y_) + 1):
                    grid += "\n" + "".join(
                        "#" if (x, y, z, w) in self.active else "."
                        for x in range(min(x_), max(x_) + 1)
                    )
        return grid


if __name__ == "__main__":
    testcase = """\
.#.
..#
###"""

    with open("input.txt", "r") as f:
        data = f.read()

    assert Grid.parse(testcase).run(6) == 112
    print(Grid.parse(data).run(6))

    assert Grid.parse(testcase, w_dim=True).run(6) == 848
    print(Grid.parse(data, w_dim=True).run(6))
