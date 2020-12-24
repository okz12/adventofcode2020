import re
from collections import defaultdict
from typing import Dict

dirs = {"e": 2, "se": 1 - 1j, "ne": 1 + 1j, "w": -2, "sw": -1 - 1j, "nw": -1 + 1j}


def string_to_loc(string: str) -> complex:
    return sum(map(dirs.get, re.findall(r"(se|ne|sw|nw|e|w)", string)))


def black_tiles(string: str) -> int:
    floor: Dict[complex, bool] = defaultdict(bool)
    for line in string.split("\n"):
        loc = string_to_loc(line)
        floor[loc] = not floor[loc]

    return sum(dict.values())


if __name__ == "__main__":
    testcase = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

    with open("input.txt", "r") as f:
        data = f.read()

    assert black_tiles(testcase) == 10
    print(black_tiles(data))
