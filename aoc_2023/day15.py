import argparse
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


def hash(value: str) -> int:
    result = 0
    for char in value:
        result += ord(char)
        result *= 17
        result %= 256
    # print(f"hash({value}) = {result}")
    return result


class Box:
    EMPTY = ("", 0)

    def __init__(self) -> None:
        self._data: list[tuple[str, int]] = []
        self._map: dict[str, int] = {}

    def add(self, key: str, value: int):
        if key in self._map:
            index = self._map[key]
            self._data[index] = (key, value)
            return
        self._data.append((key, value))
        self._map[key] = len(self._data) - 1

    def remove(self, key: str):
        if key not in self._map:
            return
        index = self._map.pop(key)
        self._data[index] = self.EMPTY

    def empty(self) -> bool:
        return len(self._data) == 0 or all(t == self.EMPTY for t in self._data)

    def __str__(self):
        data = [f"[{t[0]} {t[1]}]" for t in self._data if t != self.EMPTY]
        return " ".join(data)

    def total_power(self) -> int:
        slot = 1
        total = 0
        for key, value in self._data:
            if key == "":
                continue
            total += slot * value
            slot += 1
        return total


class HashMap:
    def __init__(self) -> None:
        self._data: list[Box | None] = [None] * 256

    def __setitem__(self, key: str, value: int):
        index = hash(key)
        box = self._data[index]
        if box is None:
            box = self._data[index] = Box()
        box.add(key, value)

    def __delitem__(self, key: str):
        index = hash(key)
        box = self._data[index]
        if box is None:
            return
        box.remove(key)

    def print(self) -> None:
        for i, box in enumerate(self._data):
            if box is None or box.empty():
                continue
            print(f"Box {i}: {box}")
        print()

    def total_power(self) -> int:
        total = 0
        for i, box in enumerate(self._data):
            if box is None or box.empty():
                continue
            total += box.total_power() * (i + 1)
        return total

    def process(self, word: str) -> None:
        if "-" in word:
            label = word[:-1]
            del self[label]
        else:
            label, value = word.split("=")
            self[label] = int(value)


def part_1(file: TextIO) -> int:
    file.seek(0)

    words = file.read().split(",")
    total = 0
    for word in words:
        total += hash(word)

    return total


def part_2(file: TextIO) -> int:
    file.seek(0)

    words = file.read().split(",")
    m = HashMap()
    for word in words:
        m.process(word)
        # print(f'After "{word}":')
        # m.print()
    return m.total_power()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
