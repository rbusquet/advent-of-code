import argparse
import re
import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


GRAB_REGEX = re.compile(r"(\d+) (red|blue|green)")
CONTENTS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def part_1(file: TextIO) -> int:
    CONTENTS = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    valid_ids = 0
    for line in file:
        if not line.strip():
            continue
        game_id_str, grab_str = line.split(":")
        game_id = int(game_id_str.split(" ")[1])

        grabs = grab_str.strip().split(";")
        for grab in grabs:
            matches = GRAB_REGEX.findall(grab)
            invalid = False
            for grab_count_str, color in matches:
                grab_count = int(grab_count_str.split(" ")[0])
                if invalid := grab_count > CONTENTS[color]:
                    break
            if invalid:
                break
        else:
            valid_ids += game_id

    return valid_ids


def part_2(file: TextIO) -> int:
    total_power = 0
    for line in file:
        if not line.strip():
            continue
        game_id_str, grab_str = line.split(":")

        grabs = grab_str.strip().split(";")
        min_contents = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for grab in grabs:
            matches = GRAB_REGEX.findall(grab)
            for grab_count_str, color in matches:
                grab_count = int(grab_count_str.split(" ")[0])
                min_contents[color] = max(min_contents[color], grab_count)
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
