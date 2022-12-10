from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from itertools import product
from typing import Callable, Generator, NamedTuple, TextIO


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


class Node(NamedTuple):
    x: int
    y: int

    def neighboors(self) -> Generator[Node, None, None]:
        for x, y in product([-1, 0, 1], repeat=2):
            neighbor = Node(self.x + x, self.y + y)
            yield neighbor

    def touches(self, other: Node) -> bool:
        return any(other == n for n in self.neighboors())

    def follow(self, other: Node) -> Node:
        if self.touches(other):
            return self
        x, y = self
        if self.y > other.y:
            y -= 1
        elif self.y < other.y:
            y += 1
        if self.x > other.x:
            x -= 1
        elif self.x < other.x:
            x += 1
        return Node(x, y)


Step = Callable[[Node], Node]


steps = dict[str, Step](
    U=lambda node: Node(node.x, node.y + 1),
    D=lambda node: Node(node.x, node.y - 1),
    L=lambda node: Node(node.x - 1, node.y),
    R=lambda node: Node(node.x + 1, node.y),
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    head = Node(0, 0)
    tail = Node(0, 0)
    rope = 10 * [Node(0, 0)]

    visited_part_1 = set[Node]()
    visited_part_2 = set[Node]()
    for line in args.infile:
        direction, count = line.split()
        step = steps[direction]
        for _ in range(int(count)):
            head = step(head)
            tail = tail.follow(head)

            rope[0] = step(rope[0])
            for i in range(1, 10):
                rope[i] = rope[i].follow(rope[i - 1])

            visited_part_1.add(tail)
            visited_part_2.add(rope[-1])
    print(len(visited_part_1))
    print(len(visited_part_2))
