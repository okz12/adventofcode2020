import re
from typing import Dict, Set

dirs = {"e": 2, "se": 1 - 1j, "ne": 1 + 1j, "w": -2, "sw": -1 - 1j, "nw": -1 + 1j}
# Use double spacing for east/west for hex structure


def string_to_loc(string: str) -> complex:
    return sum(map(dirs.get, re.findall(r"(se|ne|sw|nw|e|w)", string)))


def black_tiles(string: str) -> Set[complex]:
    floor: Set[complex] = set()
    for line in string.split("\n"):
        if (loc := string_to_loc(line)) in floor:
            floor.remove(loc)
        else:
            floor.add(loc)
    return floor


def count_neighbours(floor: Set[complex]) -> Dict[complex, int]:
    neighbours: Dict[complex, int] = {}
    for loc in floor:
        for dir in dirs.values():
            neighbours[loc + dir] = neighbours.get(loc + dir, 0) + 1
    return neighbours


def lobby_tiles(string: str) -> Set[complex]:
    floor = black_tiles(string)

    for _ in range(100):
        neighbours = count_neighbours(floor)
        floor = set(
            k for k, v in neighbours.items() if v == 2 or (k in floor and v == 1)
        )
        # print(f"Day:{_}: {len(floor)}")
    return floor


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

    assert len(black_tiles(testcase)) == 10
    print(len(black_tiles(data)))

    assert len(lobby_tiles(testcase)) == 2208
    print(len(lobby_tiles(data)))
