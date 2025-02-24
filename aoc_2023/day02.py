import argparse
import re
import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


GRAB_REGEX = re.compile(r"(\d+) (red|blue|green)")


def process_line(line: str) -> tuple[int, list[list[tuple[str, str]]]]:
    game_id_str, grab_str = line.split(":")
    game_id = int(game_id_str.split(" ")[1])
    grabs = [GRAB_REGEX.findall(grab) for grab in grab_str.strip().split(";")]
    return game_id, grabs


def part_1(file: TextIO) -> int:
    CONTENTS = {"red": 12, "green": 13, "blue": 14}
    valid_ids = 0
    for line in file:
        game_id, grabs = process_line(line)
        for grab in grabs:
            for grab_count_str, color in grab:
                if int(grab_count_str.split(" ")[0]) > CONTENTS[color]:
                    break
            else:
                continue
            break
        else:
            valid_ids += game_id
    return valid_ids


def part_2(file: TextIO) -> int:
    total_power = 0
    for line in file:
        _game_id, grabs = process_line(line)
        min_contents = {"red": 0, "green": 0, "blue": 0}
        for grab in grabs:
            for grab_count_str, color in grab:
                min_contents[color] = max(
                    min_contents[color], int(grab_count_str.split(" ")[0])
                )
        total_power += (
            min_contents["red"] * min_contents["green"] * min_contents["blue"]
        )
    return total_power


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    args.file.seek(0)
    print(part_2(args.file))
