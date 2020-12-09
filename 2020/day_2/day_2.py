import re
from collections import Counter
from typing import List


def read_file():
    with open("./input.txt") as f:
        return f.readlines()


def part_1(passwords: List[str]):
    valid = 0

    expression = re.compile(r"(\d+)-(\d+) (.): (.*)")
    for password in passwords:
        if match := expression.match(password):
            min_, max_, letter, password = match.groups()
            count = Counter(password)[letter]
            if count >= int(min_) and count <= int(max_):
                valid += 1
    print(valid)


def part_2(passwords: List[str]):
    valid = 0

    expression = re.compile(r"(\d+)-(\d+) (.): (.*)")
    for password in passwords:
        if match := expression.match(password):
            pos_1, pos_2, letter, password = match.groups()
            letters = {password[int(pos_1) - 1], password[int(pos_2) - 1]}
            if len(letters) == 2 and letter in letters:
                valid += 1
    print(valid)


if __name__ == "__main__":
    passwords = read_file()
    part_1(passwords)
    part_2(passwords)
