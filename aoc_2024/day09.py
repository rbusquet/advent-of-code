from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def checksum(memory: list[int]) -> int:
    total = 0
    for i, file_id in enumerate(memory):
        total += i * file_id
    return total


def part_1() -> int:
    disk_map = input.read_text()

    memory = list[int]()
    free_space = -1
    counter = count()
    for i, size in enumerate(map(int, disk_map)):
        if i % 2 == 0:
            file_id = next(counter)
            memory.extend(file_id for _ in range(size))
        else:
            memory.extend(free_space for _ in range(size))

    i = 0
    while i < len(memory) - 1:
        # cleanpup empty space at the end
        while memory[-1] == -1:
            memory.pop()
        if i >= len(memory):
            break  # done
        if memory[i] == -1:
            memory[i] = memory.pop()
        i += 1
    return checksum(memory)


@dataclass
class File:
    id: int
    size: int


def checksum_v2(memory: list[File]) -> int:
    counter = count()
    total = 0
    for file in memory:
        if file.id == -1:
            continue
        total += next(counter) * file.id
    return total


def part_2() -> int:
    disk_map = input.read_text()

    memory = list[File]()
    counter = count()
    for i, size in enumerate(map(int, disk_map)):
        if i % 2 == 0:
            file_id = next(counter)
            memory.append(File(file_id, size))
        else:
            memory.append(File(-1, size))

    left = 0

    while left < len(memory):
        # find first empty block
        while memory[left].id != -1:
            left += 1
        empty_space = memory[left]
        # find first file from the back that fits in empty space
        right = len(memory) - 1
        while memory[right].id == -1 or memory[right].size > empty_space.size:
            right -= 1
            if right <= left:
                # nothing fits
                left += 1
                break
        else:
            file = memory.pop(right)
            memory.insert(left, file)
            empty_space.size -= file.size

    return checksum_v2(memory)


print(part_1())
print(part_2())
