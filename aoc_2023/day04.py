import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def process_file(file: TextIO):
    file.seek(0)
    for line in file:
        card, numbers = line.split(":")
        winning_numbers, scratch_numbers = numbers.split("|")
        yield card, winning_numbers.strip().split(), scratch_numbers.strip().split(" ")


def part_1(file: TextIO) -> int:
    total = 0
    for card, winning_numbers, scratch_numbers in process_file(file):
        common_numbers = set(winning_numbers) & set(scratch_numbers)
        if not common_numbers:
            continue
        # 1 point for the first common number, any additional doubles the points
        total += 2 ** (len(common_numbers) - 1)
    return total


def part_2(file: TextIO) -> int:
    card_counter = defaultdict[int, int](int)
    for card, winning_numbers, scratch_numbers in process_file(file):
        current_card_id = int(card.split()[1])
        card_counter[current_card_id] += 1

        current_count = card_counter[current_card_id]
        common_numbers = set(winning_numbers) & set(scratch_numbers)

        wins = len(common_numbers)
        for i in range(wins):
            card_counter[current_card_id + i + 1] += current_count

    return sum(card_counter.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
