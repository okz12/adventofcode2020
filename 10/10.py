make_int = lambda x: list(sorted(int(n) for n in x.split()))

def joltage_diff(string: str) -> int:
    A = make_int(string)
    diffs = [A[0]] + [A[n] - A[n-1] for n in range(1, len(A))] + [3]
    return diffs.count(1) * diffs.count(3)

def joltage_jumps(string: str) -> int:
    A = [0] + make_int(string)
    dp = [0] * len(A)
    dp[0] = 1
    for i in range(1, len(A)):
        for j in range(max(0, i-3), i):
            if 0 < A[i] - A[j] < 4:
                dp[i] += dp[j]
    return dp[-1]



if __name__ == "__main__":
    testcase = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert joltage_diff(testcase) == 220
    print(joltage_diff(data))

    assert joltage_jumps(testcase) == 19208
    print(joltage_jumps(data))