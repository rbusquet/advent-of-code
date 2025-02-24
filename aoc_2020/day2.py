import re
from collections import Counter


def read_file() -> list[str]:
    with open("./input.txt") as f:
        return f.readlines()


def part_1(passwords: list[str]) -> int:
    valid = 0

    expression = re.compile(r"(\d+)-(\d+) (.): (.*)")
    for password in passwords:
        if match := expression.match(password):
            min_, max_, letter, password = match.groups()
            count = Counter(password)[letter]
            if count >= int(min_) and count <= int(max_):
                valid += 1
    return valid


def part_2(passwords: list[str]) -> int:
    valid = 0

    expression = re.compile(r"(\d+)-(\d+) (.): (.*)")
    for password in passwords:
        if match := expression.match(password):
            pos_1, pos_2, letter, password = match.groups()
            letters = {password[int(pos_1) - 1], password[int(pos_2) - 1]}
            if len(letters) == 2 and letter in letters:
                valid += 1
    return valid


if __name__ == "__main__":
    passwords = read_file()
    print(part_1(passwords))
    print(part_2(passwords))
