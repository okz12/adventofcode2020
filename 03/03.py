from functools import reduce

def count_trees(data: str, x_mv: int = 3, y_mv: int = 1)-> int:
    lines = data.splitlines()
    nrows, ncols = len(lines), len(lines[0])
    return sum(data[y][(i*x_mv) % ncols] == "#" for i, y in enumerate(range(0, nrows, y_mv)))

prod = lambda iterable: reduce(lambda x, y: x*y, iterable) # multiply ints in iterable / math.prod

if __name__ == "__main__":
    testcase =\
"""\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert count_trees(testcase) == 7
    print(count_trees(data))


    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    assert prod(count_trees(testcase, x, y) for x, y in slopes) == 336
    print(prod((count_trees(data, x, y) for x, y in slopes)))