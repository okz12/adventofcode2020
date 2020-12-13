def earliest_bus(string: str) -> int:
    timestamp, buses = string.split("\n", 1)
    ts = timestamp = int(timestamp)
    buses = [int(x) for x in buses.split(",") if x.isdigit()]
    while True:
        for n in buses:
            if ts % n == 0:
                return (ts - timestamp) * n
        ts += 1
    raise RuntimeError("Not Found")

def consecutive_buses(string: str) -> int:
    A = string.split("\n", 1)[1].split(",")
    nums, factors = [], []
    for i, v in enumerate(A):
        if v.isdigit():
            nums.append(int(v))
            factors.append(int(v) - i)
    return chinese_remainder(nums, factors)

###
# Chinese Remainder Theorem from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
###

def matching_timetable(string: str) -> int:
    buses = string.split("\n", 1)[1].split(",")


if __name__ == "__main__":
    testcase = """\
939
7,13,x,x,59,x,31,19"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert earliest_bus(testcase) == 295
    print(earliest_bus(data))

    assert consecutive_buses(testcase) == 1068781
    print(earliest_bus(data))
