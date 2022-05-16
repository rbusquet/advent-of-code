from hashlib import md5
from itertools import count
from pathlib import Path


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        secret = file.readline()
    for number in count():
        result = md5(f"{secret}{number}".encode())
        init = result.hexdigest()[:5]
        if init == "00000":
            return number
    return -1


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        secret = file.readline()
    for number in count():
        result = md5(f"{secret}{number}".encode())
        init = result.hexdigest()[:6]
        if init == "000000":
            return number
    return -1


if __name__ == "__main__":
    print(part_1())
    print(part_2())
