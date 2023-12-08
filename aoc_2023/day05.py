from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Iterable, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def part_1(file: TextIO) -> int:
    file.seek(0)
    seeds = [int(seed) for seed in next(file).strip().split(":")[1].strip().split()]
    mapped = set[int]()

    for line in file:
        if not line.strip():
            mapped = set[int]()
            continue
        if "map" in line:
            continue
        destination, source, length = map(int, line.strip().split())

        for i, seed in enumerate(seeds):
            if i in mapped:
                continue
            if seed >= source and seed <= source + length:
                seeds[i] = destination + seed - source
                mapped.add(i)
    return min(seeds)


@dataclass
class Range:
    start: int
    length: int
    mapped: bool = False

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def __and__(self, other: Range) -> Range | None:
        left = max(self.start, other.start)
        right = min(self.end, other.end)

        if right < left:
            return None

        length = right - left + 1
        return Range(left, length)

    @classmethod
    def start_to_end(cls, start: int, end: int) -> Range:
        length = end - start + 1
        return Range(start, length)


def parse_ranges(file: TextIO) -> list[Range]:
    seeds = [int(seed) for seed in next(file).strip().split(":")[1].strip().split()]
    return [Range(*range) for range in zip(seeds[::2], seeds[1::2])]


def strip_lines(file: TextIO) -> Iterable[str]:
    for line in file:
        yield line.strip()


def part_2(file: TextIO):
    file.seek(0)
    ranges = parse_ranges(file)

    for line in strip_lines(file):
        if not line:
            for range in ranges:
                range.mapped = False
            continue
        if "map" in line:
            continue

        destination, source_start, length = map(int, line.strip().split())
        source = Range(source_start, length)

        for range in ranges:
            if range.mapped:
                continue
            intersect = range & source

            if intersect is None:
                continue

            if range.start < intersect.start:
                # beginning of range is not mapped using current rule
                # range:  ____======...
                # inter:  ______====...
                # new:    ______====...
                # update: ____==____...
                # continue loop since this updated range won't update
                ranges.append(Range.start_to_end(intersect.start, range.end))
                range.length = Range.start_to_end(
                    range.start, intersect.start - 1
                ).length
                continue

            if range.end > intersect.end:
                # end of range is not mapped using current rule
                # range:  ...======____
                # inter:  ...====______
                # new:    _______==____
                # update: ...====______
                # keep loop, this range will update up to intersection length
                # new range won't match this rule anymore (may match future ones)
                ranges.append(Range.start_to_end(intersect.end + 1, range.end))
                range.length = intersect.length

            range.start = destination + range.start - source.start

            # individual updated ranges won't match future rules.
            # flag them so updates to new ranges aren't considered in this
            # map group
            range.mapped = True

    return min(r.start for r in ranges)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
