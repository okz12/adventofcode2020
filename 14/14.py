from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import re


def create_ints(floating: int, one_mask: int, loc: int) -> List[int]:
    res = [loc | one_mask]
    for i in range(36):
        if bit_mask := ((1 << i) & floating):
            nres = [bit_mask | x for x in res] + [~bit_mask & x for x in res]
            res = nres[:]
    return res

@dataclass
class Command:
    op: int # 0 for update mask, 1 for store
    d1: int
    d2: int

    def __init__(self, string:str) -> None:
        if string[:4] == "mask":
            self.op = 1
            mask = string.split("\n")[0].split(" = ")[1]
            self.d1 = int("".join(x if x == "1" else "0" for x in mask), 2)
            self.d2 = int("".join(x if x == "0" else "1" for x in mask), 2)
        else:
            self.op = 0
            loc, val = re.match("mem\[(\d+)]\s=\s(\d+)", string).groups()
            self.d1 = int(loc)
            self.d2 = int(val)

@dataclass
class Computer:
    commands : List[Command]
    memory : Dict[int, int]
    one_mask : int
    zero_mask : int

    @staticmethod
    def parse(string: str) -> Computer:
        commands = [Command(x) for x in string.split("\n")]
        return Computer(commands, {}, 0, 0)

    def step(self, command: Command) -> None:
        if command.op:
            self.one_mask = command.d1
            self.zero_mask = command.d2
        else:
            self.memory[command.d1] = (command.d2 & self.zero_mask) | self.one_mask

    def step2(self, command: Command) -> None:
        if command.op:
            self.one_mask = command.d1
            self.zero_mask = command.d2
        else:
            floating = ~self.one_mask & self.zero_mask
            locs = create_ints(floating, self.one_mask, command.d1)
            for loc in locs:
                self.memory[loc] = command.d2

    def run(self, mode = 0) -> int:
        if mode == 0:
            [self.step(c) for c in self.commands]
        else:
            [self.step2(c) for c in self.commands]
        return sum(self.memory.values())

if __name__ == "__main__":
    testcase = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert Computer.parse(testcase).run(0) == 165
    print(Computer.parse(data).run(0))

    testcase2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


    assert Computer.parse(testcase2).run(1) == 208
    print(Computer.parse(data).run(1))


