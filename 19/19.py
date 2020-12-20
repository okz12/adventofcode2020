from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class RegexGraph:
    cases: List[str]
    graph: Dict[str, str]
    res_graph: Dict[str, str]
    loop: bool

    @staticmethod
    def parse(string: str, loop=False) -> RegexGraph:
        rules, cases = string.split("\n\n", 1)
        rules_ = rules.split("\n")
        cases_ = cases.split("\n")
        graph = {x.split(":")[0]: x.split(":")[1].replace('"', "").strip() for x in rules_}
        return RegexGraph(cases_, graph, {}, loop)

    def gen_regex(self, rule: str):
        if rule in self.res_graph:
            return self.res_graph[rule]

        if self.graph[rule].isalpha() and len(self.graph[rule]) == 1:
            self.res_graph[rule] = self.graph[rule]
        elif self.loop and rule == "8":
            # 8: 42 | 42 8 = One or more of 42
            self.res_graph[rule] = self.gen_regex("42") + "+"
        elif self.loop and rule == "11":
            # 11: 42 31 | 42 11 31 = {1-n} x 42 + {1-n} x 31 - precompute for depth of n = 5
            self.res_graph[rule] = "(?:" + "|".join(
                    f'{self.gen_regex("42")}{{{n}}}{self.gen_regex("31")}{{{n}}}'
                    for n in range(1, 5)) + ")"
        else:
            ors = [x.strip() for x in self.graph[rule].split("|")]
            ands = ["".join([self.gen_regex(x.strip()) for x in o.split(" ")]) for o in ors]
            self.res_graph[rule] = "(?:" + "|".join(ands) + ")"
        return self.res_graph[rule]

    def run(self):
        return sum(bool(re.match(self.gen_regex("0") + "$", c)) for c in self.cases)


if __name__ == "__main__":
    testcase = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

    with open("input.txt", "r") as f:
        data = f.read()

    assert RegexGraph.parse(testcase).run() == 2
    print(RegexGraph.parse(data).run())

    testcase2 = """\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

    assert RegexGraph.parse(testcase2, True).run() == 12
    print(RegexGraph.parse(data, True).run())