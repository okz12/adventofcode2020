from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

from typing import List, Tuple

class op(Enum):
    nop = auto()
    jmp = auto()
    acc = auto()

    @classmethod
    def from_str(cls, label):
        map = {'nop': cls.nop,
               'jmp': cls.jmp,
               'acc': cls.acc}
        if label in map:
            return map[label]
        raise NotImplementedError


@dataclass
class Computer:
    instructions: List[Tuple[op, int]]
    acc: int = 0
    loc: int = 0

    @staticmethod
    def parse(commands: str) -> Computer:
        instructions = []
        for command in commands.split("\n"):
            operation, value = command.split(" ")
            instructions.append((op.from_str(operation), int(value)))
        return Computer(instructions)

    def reset(self):
        self.acc = self.loc = 0

    def run(self, loop=True) -> int:
        visited = set()
        while self.loc != len(self.instructions):
            if self.loc in visited:
                if loop:
                    return self.acc
                else:
                    raise RecursionError(f"Visited Loc {self.loc} Already")
            visited.add(self.loc)
            self.iter()
        return self.acc

    def iter(self) -> None:
        command, value = self.instructions[self.loc]
        if command == op.jmp:
            self.loc += value
        elif command == op.acc:
            self.acc += value
            self.loc += 1
        elif command == op.nop:
            self.loc += 1
        else:
            raise ValueError(command)


def find_switch(cpu: Computer) -> int:
    switch_map = {op.nop: op.jmp, op.jmp: op.nop}
    for i, (command, value) in enumerate(cpu.instructions):
        if command in switch_map:
            cpu.instructions[i] = (switch_map[command], value)
            try:
                cpu.reset()
                return cpu.run(loop=False)
            except:
                cpu.instructions[i] = command, value
    raise ValueError("No Suitable Value Found")


if __name__ == "__main__":
    testcase = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert Computer.parse(testcase).run(loop=True) == 5
    print(Computer.parse(data).run(loop=True))

    assert find_switch(Computer.parse(testcase)) == 8
    print(find_switch(Computer.parse(data)))