from collections import Counter
def count_answers(A: str) -> int:
    groups = A.split("\n\n")
    answers, consensus = 0, 0
    for group in groups:
        c = Counter(list(group.replace("\n", "")))
        l = group.count("\n") + 1
        answers += len(c.keys())
        consensus += sum(v==l for _, v in c.items())
    return answers, consensus

if __name__ == "__main__":
    testcase =\
    """\
abc

a
b
c

ab
ac

a
a
a
a

b"""
    assert count_answers(testcase) == (11, 6)
    with open('input.txt', 'r') as f:
        data = f.read()
    print(count_answers(data))