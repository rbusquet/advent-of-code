import argparse
import sys
from dataclasses import dataclass
from typing import Generator, TextIO

from more_itertools import sliding_window


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    def buffer() -> Generator[str, None, None]:
        while ch := args.infile.read(1).strip():
            yield ch

    for i, window in enumerate(sliding_window(buffer(), 4)):
        if len(set(window)) == len(window):
            print(i + 4)
            break

    args.infile.seek(0)
    for i, window in enumerate(sliding_window(buffer(), 14)):
        if len(set(window)) == len(window):
            print(i + 14)
            break
