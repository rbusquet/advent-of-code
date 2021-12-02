from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    children_count: int
    metadata_count: int
    children: list[Node] = field(init=False, default_factory=list)
    metadata: list[int] = field(init=False, default_factory=list)


def next_input():
    with open("input8.txt") as f:
        number = ""
        while True:
            read = f.read(1)

            if not read or read == " ":
                yield int(number)
                number = ""
            else:
                number += read
            if not read:
                break


items = next_input()
# print(list(next_input()))
queue = []
nodes = []

current_parent: Node = None
while True:
    try:
        current_parent = queue[-1] if queue else None
        if (
            current_parent
            and len(current_parent.children) == current_parent.children_count
        ):
            queue.pop()
            for _ in range(current_parent.metadata_count):
                current_parent.metadata.append(next(items))
            continue
        children_count, metadata_count = next(items), next(items)

        node = Node(children_count, metadata_count)
        nodes.append(node)

        if current_parent:
            current_parent.children.append(node)

        if children_count:
            queue.append(node)
            continue
        else:
            for _ in range(metadata_count):
                node.metadata.append(next(items))

    except StopIteration:
        break


total = 0
for node in nodes:
    for m in node.metadata:
        total += m

print(f"Metadata sum: {total}")


def value(node: Node):
    if not node.children:
        return sum(node.metadata)
    else:
        total = 0
        for m in node.metadata:
            if m:
                try:
                    total += value(node.children[m - 1])
                except IndexError:
                    continue
        return total


print(f"Value of root node: {value(nodes[0])}")
