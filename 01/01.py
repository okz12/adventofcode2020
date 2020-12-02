from typing import List

# Part 1: 2-Sum
def twosum(inputs: List[int], target: int = 2020) -> int:
    values = set()
    for x in inputs:
        if x in values:
            return x * (target-x)
        values.add(target-x)
    return 0

# Part 2: 3-Sum
def threesum(inputs: List[int]) -> int:
    for xi, x in enumerate(inputs[:-2]):
        target = 2020-x
        if res := twosum(inputs[xi:-1], target):
            return x * res
    return 0

if __name__ == "__main__":
    testcase = [1721, 979, 366, 299, 675, 1456]
    assert(twosum(testcase) == 514579)
    assert(threesum(testcase) == 241861950)

    with open('input.txt', 'r') as f:
        data = [int(x) for x in f.read().splitlines()]

    print(twosum(data))
    print(threesum(data))