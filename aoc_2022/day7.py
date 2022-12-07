from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Literal, TextIO


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


@dataclass
class Node:
    name: str
    type: Literal["d", "f"]
    parent: Node | None = None
    size: int = 0

    def qual_name(self) -> str:
        if self.parent:
            return f"{self.parent.qual_name()}/{self.name}"
        return self.name

    def add_size(self, size: int) -> None:
        self.size += size
        if self.parent:
            self.parent.add_size(size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    current_dir = root_dir = Node("/", type="d")
    nodes = {current_dir.qual_name(): current_dir}
    for line in args.infile:
        match line.split():
            case ("$", "ls"):
                continue
            case ("$", "cd", "/"):
                current_dir = root_dir
            case ("$", "cd", ".."):
                current_dir = current_dir.parent or root_dir
            case ("$", "cd", name):
                qual_name = f"{current_dir.qual_name()}/{name}"
                current_dir = nodes.setdefault(
                    qual_name, Node(name, parent=current_dir, type="d")
                )
            case ("dir", name):
                qual_name = f"{current_dir.qual_name()}/{name}"
                nodes.setdefault(qual_name, Node(name, parent=current_dir, type="d"))
            case (size, name):
                qual_name = f"{current_dir.qual_name()}/{name}"
                file = nodes.setdefault(
                    qual_name, Node(name, parent=current_dir, type="f")
                )
                if file.size == 0:
                    file.add_size(int(size))
            case _:
                break

    at_most_100k = 0
    for node in nodes.values():
        if node.type == "d" and node.size <= 100_000:
            at_most_100k += node.size
    print(at_most_100k)

    total_size = 70000000
    free_space = total_size - nodes["/"].size
    needed_space = 30000000

    smallest = nodes["/"].size
    for node in nodes.values():
        if node.type == "d":
            if free_space + node.size >= needed_space:
                # print(f"can delete {node.qual_name()}...", end=" ")
                if node.size < smallest:
                    # print(
                    #     f"and with size {node.size} it's smaller than the current smallest one ({smallest})"
                    # )
                    smallest = node.size
                # else:
                # print(
                #     f"but with size {node.size} it's larger than the current smallest one ({smallest})"
                # )
    print(smallest)
