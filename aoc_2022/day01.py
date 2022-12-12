from heapq import heappush, nlargest
from pathlib import Path


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        elf = []
        elves = []
        for line in file:
            if line.strip():
                elf.append(int(line))
            else:
                elves.append(elf)
                elf = []
        return sum(max(elves, key=lambda e: sum(e)))


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        elf = []
        elves = list[int]()
        for line in file:
            if line.strip():
                elf.append(int(line))
            else:
                heappush(elves, sum(elf))
                elf = []
        return sum(nlargest(3, elves))


if __name__ == "__main__":
    print(part_1())
    print(part_2())
