from typing import Tuple

seat_id = lambda x: int(
    "".join(map({"B": "1", "F": "0", "L": "0", "R": "1"}.get, x)), 2
)


def get_seats(passes: str) -> Tuple[int, int]:
    passes_ = [seat_id(pass_) for pass_ in passes.split("\n")]
    sum_, min_, max_ = sum(passes_), min(passes_), max(passes_)
    return max_, int(((max_ - min_ + 1) * (max_ + min_) / 2) - sum_)


if __name__ == "__main__":
    assert seat_id("BFFFBBFRRR") == 567
    assert seat_id("FFFBBBFRRR") == 119
    assert seat_id("BBFFBBFRLL") == 820

    with open("input.txt", "r") as f:
        data = f.read()

    print(get_seats(data))
