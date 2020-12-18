from collections import Counter
from typing import Tuple


def count_answers(forms: str) -> Tuple[int, int]:
    groups = forms.split("\n\n")
    answers, consensus = 0, 0
    for group in groups:
        counts = Counter(list(group.replace("\n", "")))
        people = group.count("\n") + 1
        answers += len(counts.keys())
        consensus += sum(v == people for _, v in counts.items())
    return answers, consensus


if __name__ == "__main__":
    testcase = """\
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
    with open("input.txt", "r") as f:
        data = f.read()
    print(count_answers(data))
