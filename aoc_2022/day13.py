from __future__ import annotations

import argparse
import enum
import sys
from dataclasses import dataclass
from typing import TextIO

from more_itertools import grouper

Packet = list["Packet"] | int


class Comparison(enum.Enum):
    CORRECT = 1
    INCORRECT = 2
    UNDEFINED = 3


def compare(left: Packet, right: Packet) -> Comparison:
    # print(f"   compare {left} vs {right}")
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return Comparison.UNDEFINED
        elif left < right:
            return Comparison.CORRECT
        else:
            return Comparison.INCORRECT

    left = left if isinstance(left, list) else [left]
    right = right if isinstance(right, list) else [right]
    for le, ri in zip(left, right):
        result = compare(le, ri)
        if result != Comparison.UNDEFINED:
            return result
    if len(right) == len(left):
        return Comparison.UNDEFINED
    if len(right) < len(left):
        return Comparison.INCORRECT
    return Comparison.CORRECT


def bubble_sort(packets: list[Packet]) -> None:
    """
    Damn I need to memorize this.
    """
    n = len(packets)

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if compare(packets[j], packets[j + 1]) == Comparison.INCORRECT:
                packets[j], packets[j + 1] = packets[j + 1], packets[j]


def main(args: Arguments) -> None:
    indexes_sum = 0

    all_packets = list[Packet]()

    for i, (first_line, second_line, _) in enumerate(
        grouper(args.infile, 3, incomplete="fill", fillvalue="")
    ):
        left = eval(first_line)
        right = eval(second_line)
        result = compare(left, right)
        # print(
        #     dedent(
        #         f"""
        #         == Pair {i + 1} ==
        #         Compare {first_line.strip()} vs {second_line.strip()}
        #         Right order? {result.name}
        #         """
        #     )
        # )
        if result == Comparison.CORRECT:
            indexes_sum += i + 1
        all_packets.append(left)
        all_packets.append(right)
    print(indexes_sum)

    divider_2: Packet = [[2]]
    divider_6: Packet = [[6]]
    all_packets.append(divider_2)
    all_packets.append(divider_6)

    bubble_sort(all_packets)
    for item in all_packets:
        print(item)

    first_divider_index = all_packets.index(divider_2) + 1
    second_divider_index = all_packets.index(divider_6) + 1
    print(first_divider_index * second_divider_index)


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)
    main(args)
