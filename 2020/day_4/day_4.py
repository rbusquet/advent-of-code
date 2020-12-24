import re
from typing import NamedTuple

size_re = re.compile(r"(\d+)(cm|in)")
hair_re = re.compile(r"^#[a-f0-9]{6}$")
pid_re = re.compile(r"^[0-9]{9}$")


class Passport(NamedTuple):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: str = ""

    def validate(self):
        assert 1920 <= int(self.byr) <= 2002
        assert 2010 <= int(self.iyr) <= 2020
        assert 2020 <= int(self.eyr) <= 2030
        h, unit = size_re.match(self.hgt).groups()
        if unit == "cm":
            assert 150 <= int(h) <= 193
        else:
            assert 59 <= int(h) <= 76
        assert hair_re.match(self.hcl)
        assert self.ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        assert pid_re.match(self.pid)


def read_file():
    with open("./input.txt") as f:
        yield from f.readlines()


def part_1():
    passports = []
    p = {}
    for line in read_file():
        if not line.strip():
            try:
                passports.append(Passport(**p))
            except TypeError:
                continue
            finally:
                p = {}
            continue
        values = line.strip().split(" ")
        for value in values:
            k, v = value.split(":")
            p[k] = v
    # last line
    passports.append(Passport(**p))
    return passports


first_pass_valid = part_1()
print(len(first_pass_valid))

valid = 0
for passport in first_pass_valid:
    try:
        passport.validate()
        valid += 1
    except Exception:
        continue

print(valid)
