from __future__ import annotations
from dataclasses import dataclass

@dataclass
class BoardingPass:
    row: int
    col: int

    @staticmethod
    def parse(string: str) -> BoardingPass:
        row_, col_ = string[:-3], string[-3:]
        return BoardingPass(
            int(row_.replace("F", "0").replace("B", "1"), 2),
            int(col_.replace("L", "0").replace("R", "1"), 2)
        )

    @property
    def id(self) -> int:
        return self.row * 8 + self.col


def get_seats(passes: str) -> int:
    passes_ = [BoardingPass.parse(pass_).id for pass_ in passes.split("\n")]
    sum_, min_, max_ = sum(passes_), min(passes_), max(passes_)
    return max_, int(((max_ - min_ + 1) * (max_ + min_) / 2) - sum_)

if __name__ == "__main__":
    assert BoardingPass.parse("BFFFBBFRRR").id == 567
    assert BoardingPass.parse("FFFBBBFRRR").id == 119
    assert BoardingPass.parse("BBFFBBFRLL").id == 820

    with open('input.txt', 'r') as f:
        data = f.read()

    print(get_seats(data))
