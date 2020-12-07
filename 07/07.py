from typing import Dict, List, Tuple
import re

class GoldGraph:

    def __init__(self, lines):
        self.graph = self.build_graph(lines)
        self.solved_graph = {}

    @staticmethod
    def parse_statement(line: str) -> Tuple[str, List[Tuple[int, str]]]:
        left, right = line.split(" bags contain ", 1)
        if right == "no other bags.":
            right_ = []
        else:
            right_ = re.findall(r'(\d*)\s([a-z]*\s[a-z]*)\sbag', right)
        return left, [(x[1], int(x[0])) for x in right_]

    def build_graph(self, lines: str) -> Dict:
        graph = {}
        for line in lines.split("\n"):
            l, r = self.parse_statement(line)
            graph[l] = r
        return graph

    def dfs(self, vertex: str) -> int:
        if vertex not in self.solved_graph:
            self.solved_graph[vertex] = 0
            for elem, count in self.graph[vertex]:
                if elem == "shiny gold":
                    self.solved_graph[vertex] += count
                else:
                    self.dfs(elem)
                    self.solved_graph[vertex] += self.solved_graph[elem] * count
        return self.solved_graph[vertex]

    def count(self) -> int:
        return sum(self.dfs(x) > 0 for x in self.graph.keys())

    def dfs2(self, vertex: str) -> int:
        bag_count = 0
        for elem, count in self.graph[vertex]:
            bag_count += (self.dfs2(elem) + 1) * count
        return bag_count

if __name__ == "__main__":
    testcase = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

    assert GoldGraph(testcase).count() == 4

    with open('input.txt', 'r') as f:
        data = f.read()

    print(GoldGraph(data).count())

    testcase2 = """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

    assert GoldGraph(testcase2).dfs2("shiny gold") == 126

    print(GoldGraph(data).dfs2("shiny gold"))