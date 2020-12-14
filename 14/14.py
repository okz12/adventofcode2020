from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import re


def create_ints(floating: int, one_mask: int, loc: int) -> List[int]:
    """
    Create list of all possible integers using the floating bits
    """
    res = [loc | one_mask]
    for i in range(36):
        if bit_mask := ((1 << i) & floating):
            nres = [bit_mask | x for x in res] + [~bit_mask & x for x in res]
            res = nres[:]
    return res

@dataclass
class Command:
    op: int # 0 for store in memory, 1 for update mask
    d1: int
    d2: int

    def __init__(self, string:str) -> None:
        if string[:4] == "mask":
            self.op = 1
            mask = string.split("\n")[0].split(" = ")[1]
            self.d1 = int("".join(x if x == "1" else "0" for x in mask), 2) # d1 = ones mask
            self.d2 = int("".join(x if x == "0" else "1" for x in mask), 2) # d2 = zeroes mask
        else:
            self.op = 0
            loc, val = re.match("mem\[(\d+)]\s=\s(\d+)", string).groups()
            self.d1 = int(loc) # d1 = memory location
            self.d2 = int(val) # d2 = value

@dataclass
class Computer:
    commands : List[Command]
    memory : Dict[int, int]
    one_mask : int
    zero_mask : int

    def __init__(self, string: str) -> None:
        self.commands = [Command(x) for x in string.split("\n")]
        self.memory, self.one_mask, self.zero_mask = {}, 0, 0

    def run(self) -> None:
        for command in self.commands:
            if command.op: # update mask
                self.one_mask = command.d1
                self.zero_mask = command.d2
            else: # store to memory
                self.store(command)
        return sum(self.memory.values())

    def store(self, command) -> None:
        raise NotImplementedError


class Decoder(Computer):
    def store(self, command) -> None:
        self.memory[command.d1] = (command.d2 & self.zero_mask) | self.one_mask


class MemAddrDecoder(Computer):
    def store(self, command) -> None:
        floating = ~self.one_mask & self.zero_mask
        locs = create_ints(floating, self.one_mask, command.d1)
        for loc in locs:
            self.memory[loc] = command.d2


if __name__ == "__main__":
    testcase = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert Decoder(testcase).run() == 165
    print(Decoder(data).run())

    testcase2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


    assert MemAddrDecoder(testcase2).run() == 208
    print(MemAddrDecoder(data).run())


