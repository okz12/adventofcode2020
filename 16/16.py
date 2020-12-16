from __future__ import annotations
from typing import List, NamedTuple, Tuple
from dataclasses import dataclass
from collections import defaultdict
import math
import re

@dataclass
class rangelimit:
    min_ : int
    max_ : int

    def valid(self, value: int) -> bool:
        return self.min_ <= value <= self.max_

@dataclass
class requirement:
    name: str
    range1: rangelimit
    range2: rangelimit

    def valid(self, value: int) -> bool:
        return self.range1.valid(value) | self.range2.valid(value)

line_to_int = lambda x: tuple(int(i) for i in x.split(","))

@dataclass
class checker:
    requirements: List[requirement]
    my_ticket: Tuple
    nearby_tickets: List[Tuple]
    merged_limits: List[rangelimit]

    def __init__(self, string: str):
        string = string.replace("class", "class_") # reserved keyword class causing problems
        self.requirements = []
        for x in re.findall("[\\n]?([\w\s]+):\s(\d+)-(\d+)\sor\s(\d+)-(\d+)", string):
            self.requirements.append(requirement(x[0].replace(" ", "_"),
                                                 rangelimit(int(x[1]), int(x[2])),
                                                 rangelimit(int(x[3]), int(x[4]))
                                                 ))
        self.merged_limits = [r.range1 for r in self.requirements] + [r.range2 for r in self.requirements]
        self.merge_limit_intervals()
        self.my_ticket = line_to_int(string.split("your ticket:\n")[1].split("\n")[0])
        self.nearby_tickets = [line_to_int(x) for x in string.split("nearby tickets:\n")[1].split("\n")]

    def merge_limit_intervals(self) -> None: # Optional Optimisation - merging intervals
        self.merged_limits.sort(key = lambda x: x.min_)
        idx = 0
        while idx + 1 < len(self.merged_limits):
            if self.merged_limits[idx].max_ >= self.merged_limits[idx + 1].min_:
                self.merged_limits[idx] = rangelimit(self.merged_limits[idx].min_,
                                                     max(self.merged_limits[idx].max_, self.merged_limits[idx + 1].max_)
                                                     )
                self.merged_limits.pop(idx + 1)
            else:
                idx += 1

    def error_rate(self) -> int:
        return sum(value for ticket in self.nearby_tickets for value in ticket
                   if all(not limit.valid(value) for limit in self.merged_limits))

    def match_fields(self) -> int:
        # discard invalid tickets
        valid_tickets = [ticket for ticket in self.nearby_tickets
                         if not any(all(not limit.valid(value) for limit in self.merged_limits) for value in ticket)]

        # map valid columns for each requirement
        ticket_map = defaultdict(list)
        for ticket_col in range(len(self.requirements)):
            ticket_map[ticket_col] = [r_idx for r_idx, req in enumerate(self.requirements)
                                      if all(req.valid(vt[ticket_col]) for vt in valid_tickets)]

        # filter valid columns incrementally to find final mapping
        fin_ticket_map = {}
        while len(fin_ticket_map) < len(self.requirements):
            resolved = [(k, v[0]) for k, v in ticket_map.items() if len(v) == 1]
            for k in ticket_map.keys():
                for rk, rv in resolved:
                    fin_ticket_map[rv] = rk
                    if rv in ticket_map[k]:
                        ticket_map[k].pop(ticket_map[k].index(rv))

        ticket = NamedTuple("ticket", [(r.name, int) for r in self.requirements])
        my_ticket = ticket(*[self.my_ticket[fin_ticket_map[i]] for i in range(len(fin_ticket_map))])
        return math.prod(getattr(my_ticket, x) for x in my_ticket._fields if x.startswith("departure"))

if __name__ == "__main__":
    testcase = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    with open('input.txt', 'r') as f:
        data = f.read()

    assert checker(testcase).error_rate() == 71
    print(checker(data).error_rate())

    print(checker(data).match_fields())