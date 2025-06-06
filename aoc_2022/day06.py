from __future__ import annotations

import argparse
import sys
from collections.abc import Generator
from dataclasses import dataclass
from typing import TextIO

from more_itertools import sliding_window


def main(args: Arguments) -> None:
    def buffer() -> Generator[str]:
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


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)
    main(args)
