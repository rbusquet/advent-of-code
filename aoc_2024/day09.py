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
        # clean up empty space at the end
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
    index: int


def checksum_v2(memory: list[File]) -> int:
    counter = count()
    total = 0
    for file in memory:
        if file.id == -1:
            continue
        total += next(counter) * file.id
    return total


class DiskMap(list[File]):
    def __str__(self):
        result = ""
        s = sorted(self, key=lambda x: x.index)
        for i, file in enumerate(s):
            result += f"{file.id}" * file.size
            if i + 1 >= len(self):
                return result
            next_file = s[i + 1]
            empty = next_file.index - file.index - file.size
            result += "." * empty
        return result

    def checksum(self) -> int:
        checksum = 0
        for file in self:
            for i in range(file.index, file.index + file.size):
                checksum += i * file.id
        return checksum


def part_2() -> int:
    disk_map = input.read_text()

    files = DiskMap()
    empty_space = list[File]()
    counter = count()
    index = 0
    for i, size in enumerate(map(int, disk_map)):
        if i % 2 == 0:
            file_id = next(counter)
            files.append(File(file_id, size, index))
        else:
            empty_space.append(File(-1, size, index))
        index += size

    moved = DiskMap()
    while files:
        file_to_move = files.pop()

        for empty in empty_space:
            if empty.index > file_to_move.index:
                break
            if empty.size >= file_to_move.size:
                file_to_move.index = empty.index
                empty.index += file_to_move.size
                empty.size -= file_to_move.size
                if empty.size == 0:
                    empty_space.remove(empty)
                break
        moved.append(file_to_move)

    return moved.checksum()


print(part_1())
print(part_2())
