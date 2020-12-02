from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Tuple

@dataclass
class Password:
    lo: int
    hi: int
    char: str
    password: str

    def isvalid1(self) -> bool:
        return self.lo <= self.password.count(self.char) <= self.hi

    def isvalid2(self) -> bool:
        return (self.password[self.lo-1] == self.char) ^ (self.password[self.hi-1] == self.char)

    @staticmethod
    def parse(string: str) -> Password:
        m = re.match("(\d+)-(\d+)\s([a-z]):\s([a-z]*)", string).groups()
        return Password(int(m[0]), int(m[1]), m[2], m[3])

def countvalid(passwords: str) -> Tuple[int, int]:
    passwords_ = [Password.parse(line) for line in passwords.splitlines()]
    return sum(pw.isvalid1() for pw in passwords_), sum(pw.isvalid2() for pw in passwords_)

if __name__ == "__main__":
    testcase = "1-3 a: abcde\n" \
               "1-3 b: cdefg\n" \
               "2-9 c: ccccccccc"
    assert(countvalid(testcase) == (2, 1))
    with open('input.txt', 'r') as f:
        data = f.read()
    print(countvalid(data))