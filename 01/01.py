from typing import List

# Part 1: 2-Sum
def twosum(inputs: List[int]) -> int:
    values = set()
    for x in inputs:
        if x in values:
            return x * (2020-x)
        values.add(2020-x)

# Part 2: 3-Sum
def threesum(inputs: List[int]) -> int:
    for xi, x in enumerate(inputs[:-2]):
        target = 2020-x
        values = set()
        for y in inputs[xi:-1]:
            if y in values:
                return x * y * (target-y)
            values.add(target-y)

if __name__ == "__main__":
    testcase = [1721, 979, 366, 299, 675, 1456]
    assert(twosum(testcase) == 514579)
    assert(threesum(testcase) == 241861950)

    with open('input.txt', 'r') as f:
        data = [int(x) for x in f.read().splitlines()]

    print(twosum(data))
    print(threesum(data))