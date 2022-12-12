import argparse
import copy
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from operator import itemgetter
from typing import TextIO


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


def build_stacks(file: TextIO) -> dict[int, deque[str]]:
    stacks = defaultdict[int, deque[str]](deque)
    crate_exp = re.compile(r"\[(\w)\]")

    for line in file:
        added_crater = False
        for crate in crate_exp.finditer(line):
            index = crate.start(1)
            stacks[index].appendleft(crate.group(1))
            added_crater = True
        if not added_crater:
            for stack_id in re.finditer(r"\d", line):
                index = stack_id.start()
                stacks[int(stack_id.group())] = stacks.pop(index)
            break

    return stacks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    stacks_1 = build_stacks(args.infile)
    stacks_2 = copy.deepcopy(stacks_1)

    for line in args.infile:
        if not line.strip():
            continue
        instruction = line.split()
        count, from_, to = itemgetter(1, 3, 5)(instruction)

        stacks_2_move = deque[str]()
        for _ in range(int(count)):
            stacks_1[int(to)].append(stacks_1[int(from_)].pop())
            stacks_2_move.appendleft(stacks_2[int(from_)].pop())
        stacks_2[int(to)].extend(stacks_2_move)
        # pprint(stacks_2)

    print("")
    for _, stack in sorted(stacks_1.items()):
        print(stack.pop(), end="")
    print()
    for _, stack in sorted(stacks_2.items()):
        print(stack.pop(), end="")
    print()
