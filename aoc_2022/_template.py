import argparse
import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")

    args = Arguments()
    parser.parse_args(namespace=args)
    path = args.infile if isinstance(args.infile, str) else args.infile.name
    with open(path) as file:
        args.infile = file
