from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from typing import Generator, Iterable, TextIO


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


def count_visible(row: Iterable[str]) -> Generator[int, None, None]:
    heighest = -1
    for i, tree in enumerate(row):
        if int(tree) > heighest:
            heighest = int(tree)
            yield i


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    forest = list[str]()
    for line in args.infile:
        if line := line.strip():
            forest.append(line)
        else:
            break

    seen = set[tuple[int, int]]()
    for i, row in enumerate(forest):
        seen.update((i, j) for j in count_visible(row))
        seen.update((i, len(row) - 1 - j) for j in count_visible(row[::-1]))

    for j in range(len(forest[0])):
        column = [row[j] for row in forest]
        seen.update((i, j) for i in count_visible(column))
        seen.update((len(column) - 1 - i, j) for i in count_visible(column[::-1]))
    # for i, row in enumerate(forest):
    #     for j, tree in enumerate(row):
    #         if (i, j) in seen:
    #             print(tree, end="")
    #         else:
    #             print(" ", end="")
    #     print()
    print(len(seen))

    max_score = 0
    for i, j in seen:
        height = int(forest[i][j])
        # up
        scores = []
        for ii in range(i - 1, -1, -1):
            if height <= int(forest[ii][j]):
                scores.append(i - ii)
                break
        else:
            scores.append(i)
        # down
        for ii in range(i + 1, len(forest)):
            if height <= int(forest[ii][j]):
                scores.append(ii - i)
                break
        else:
            scores.append(len(forest) - 1 - i)
        for jj in range(j - 1, -1, -1):
            if height <= int(forest[i][jj]):
                scores.append(j - jj)
                break
        else:
            scores.append(j)
        for jj in range(j + 1, len(forest)):
            if height <= int(forest[i][jj]):
                scores.append(jj - j)
                break
        else:
            scores.append(len(forest) - 1 - j)

        score = math.prod(scores)
        if score > max_score:
            max_score = score
    print(max_score)
