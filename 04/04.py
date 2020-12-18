from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Tuple


@dataclass
class Passport:
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: str

    @staticmethod
    def parse(passport) -> Passport:
        lines = passport.replace("\n", " ").split(" ")
        passport_ = {x: None for x in "byr iyr eyr hgt hcl ecl pid cid".split(" ")}
        for line in lines:
            key, value = line.split(":")
            passport_[key] = value
        return Passport(**passport_)

    def isvalid(self) -> bool:
        return all(
            x is not None
            for x in [
                self.byr,
                self.iyr,
                self.eyr,
                self.hgt,
                self.hcl,
                self.ecl,
                self.pid,
            ]
        )

    def isvalid2(self) -> bool:
        return (
            all(
                [
                    self.byr.isdigit() and 1920 <= int(self.byr) <= 2002,
                    self.iyr.isdigit() and 2010 <= int(self.iyr) <= 2020,
                    self.eyr.isdigit() and 2020 <= int(self.eyr) <= 2030,
                    self.valid_height(),
                    re.match(r"#[0-9a-f]{6}", self.hcl),
                    self.ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
                    self.pid.isdigit() and len(self.pid) == 9,
                ]
            )
            if self.isvalid()
            else False
        )

    def valid_height(self) -> bool:
        val, units = self.hgt[:-2], self.hgt[-2:]
        return val.isdigit() and (
            (150 <= int(val) <= 193 and units == "cm")
            or (59 <= int(val) <= 76 and units == "in")
        )


def count(string: str) -> Tuple[int, int]:
    pw = [Passport.parse(x) for x in string.split("\n\n")]
    return sum(x.isvalid() for x in pw), sum(x.isvalid2() for x in pw)


if __name__ == "__main__":
    testcase = """\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
    assert count(testcase) == (2, 2)

    with open("input.txt", "r") as f:
        data = f.read()

    print(count(data))
