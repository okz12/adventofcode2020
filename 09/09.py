from collections import defaultdict

def valid_encoding(string: str, preamble: int) -> int:
    nums = [int(x) for x in string.split()]
    eviction_priority = defaultdict(list)
    digits_count = defaultdict(int)

    for i, vi in enumerate(nums):
        if not digits_count[vi] and i >= preamble:
            return vi

        for vj in nums[i + 1:]:
            digits_count[vi + vj] += 1
            eviction_priority[i].append(vi + vj)

        for x in eviction_priority[i-preamble]:
            digits_count[x] -= 1
        del eviction_priority[i-preamble]
    raise RuntimeError("Not Found")

def find_contiguous(string: str, num: int) -> int:
    nums = [int(x) for x in string.split()]
    cumsum = nums[:]
    for i in range(1, len(cumsum)):
        cumsum[i] += cumsum[i-1]

    for i in range(len(cumsum)):
        for j in range(i+1, len(cumsum)):
            if cumsum[j] - cumsum[i] == num:
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