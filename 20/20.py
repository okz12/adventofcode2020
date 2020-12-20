from __future__ import annotations
from typing import List
from math import sqrt, prod

TILE = List[str]

seamonster = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """


class Jigsaw:
    def __init__(self, string: str) -> None:
        self.tiles = {}
        for tile in string.split("\n\n"):
            id_ = int(tile.split(":")[0].split(" ")[1])
            tile_ = tile.split("\n")[1:]
            self.tiles[id_] = self.combinations(tile_)
        self.dim = int(sqrt(len(self.tiles)))
        self.tiles_matrix = [[None] * self.dim for _ in range(self.dim)]
        self.tiles_id_matrix = [[0] * self.dim for _ in range(self.dim)]

    @staticmethod
    def combinations(tile):
        def transpose(tile: TILE) -> TILE:
            return list("".join(row) for row in zip(*tile))

        def reverse(tile: TILE) -> TILE:
            return list("".join(reversed(row)) for row in tile)

        def rotate(tile: TILE) -> TILE:
            return reverse(transpose(tile))

        combs = [tile, transpose(tile)]
        for _ in range(3):
            combs.append(rotate(combs[-2]))  # rotate normal
            combs.append(rotate(combs[-2]))  # rotate transposed
        return combs

    def search(self, row: int, col: int) -> bool:
        if row == self.dim:
            return True
        for id_ in list(self.tiles.keys()):
            tile_combs = self.tiles[id_]
            del self.tiles[id_]

            for tile in tile_combs:
                if (row == 0 or (self.tiles_matrix[row - 1][col][-1] == tile[0])) and (
                    col == 0 or ([x[-1] for x in self.tiles_matrix[row][col - 1]] == list(x[0] for x in tile))):
                    self.tiles_matrix[row][col] = tile
                    self.tiles_id_matrix[row][col] = id_
                    if self.search(row + 1 if col == self.dim - 1 else row, 0 if col == self.dim - 1 else col + 1):
                        return True
            self.tiles[id_] = tile_combs
        return False

    def run(self) -> int:
        self.search(0, 0)
        return prod([self.tiles_id_matrix[0][0], self.tiles_id_matrix[0][-1],
                     self.tiles_id_matrix[-1][0], self.tiles_id_matrix[-1][-1]])

    def monster(self) -> int:
        def trim_tile(tile: TILE) -> TILE:
            return [row[1:-1] for row in tile[1:-1]]

        trimmed = [[trim_tile(x) for x in y] for y in self.tiles_matrix]
        sea = ["".join(col[i] for col in row) for row in trimmed for i in range(len(trimmed[0][0]))]

        total_hash = sum([line.count("#") for line in sea])
        counted = 0

        seamonster_combs = self.combinations(seamonster.split("\n"))
        for sm in seamonster_combs:
            points = [(ri, ci) for ri, row in enumerate(sm) for ci, pt in enumerate(row) if pt == "#" ]
            for yi, y in enumerate(sea):
                for xi, x in enumerate(y):
                    if all(0 <= yi + ri < len(sea) and 0 <= xi + ci < len(sea) and sea[yi + ri][xi + ci] in {"#", "O"} for (ri, ci) in points):
                        counted += 1

            if counted:
                return total_hash - (len(points) * counted)
        return 0


if __name__ == "__main__":
    with open("testcase.txt", "r") as f:
        testcase = f.read()
    with open("input.txt", "r") as f:
        data = f.read()

    test = Jigsaw(testcase)
    mypuzzle = Jigsaw(data)

    assert test.run() == 20899048083289
    print(mypuzzle.run())

    assert test.monster() == 273
    print(mypuzzle.monster())
