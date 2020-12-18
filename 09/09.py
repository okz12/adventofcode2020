from collections import defaultdict
from typing import Dict

def valid_encoding(string: str, preamble: int) -> int:
    nums = [int(x) for x in string.split()]
    eviction_priority = defaultdict(list)
    valid_sums: Dict[int, int] = defaultdict(int)

    for i, vi in enumerate(nums):
        if not valid_sums[vi] and i >= preamble:
            return vi

        for vj in nums[i + 1:]:
            valid_sums[vi + vj] += 1
            eviction_priority[i].append(vi + vj)

        for x in eviction_priority[i-preamble]:
            valid_sums[x] -= 1
        del eviction_priority[i-preamble]
    raise RuntimeError("Not Found")

def find_contiguous(string: str, num: int) -> int:
    nums = [int(x) for x in string.split()]
    cumsum = nums[:]
    for i in range(1, len(cumsum)):
        cumsum[i] += cumsum[i-1]

    i, j = 0, 1
    while j < len(nums):
        if cumsum[j] - cumsum[i] > num:
            i += 1
        elif cumsum[j] - cumsum[i] < num:
            j += 1
        else:
          return min(nums[i+1:j]) + max(nums[i+1: j])
    raise RuntimeError("Not Found")




if __name__ == "__main__":
    testcase = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert valid_encoding(testcase, 5) == 127
    print(valid_encoding(data, 25))

    assert find_contiguous(testcase, valid_encoding(testcase, 5)) == 62
    print(find_contiguous(data, valid_encoding(data, 25)))