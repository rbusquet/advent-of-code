from collections import deque
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

input = Path(__file__).parent / "input.txt"


@dataclass
class Group:
    parent: "Group | None" = None
    garbage: bool = False
    contents: str = ""

    @cached_property
    def score(self) -> int:
        if self.parent:
            return self.parent.score + 1
        return 1


def part_1_and_2() -> tuple[int, int]:
    it = iter(input.read_text())
    queue = deque[Group]()

    contents = ""

    groups = list[Group]()
    garbages = list[Group]()
    for ch in it:
        if not queue:
            queue.append(Group())
            continue
        parent = queue.pop()
        if ch == "!":
            # contents += ch + next(it)
            next(it)
            queue.append(parent)
        elif parent.garbage:
            if ch == ">":
                parent.contents = contents
                garbages.append(parent)
                contents = ""
                continue
            contents += ch
            queue.append(parent)
        elif ch == "{":
            # new group
            group = Group(parent=parent)
            queue.append(parent)
            queue.append(group)
        elif not parent.garbage and ch == "}":
            groups.append(parent)
        elif not parent.garbage and ch == "<":
            garbage = Group(parent=parent, garbage=True)
            queue.append(parent)
            queue.append(garbage)

        else:
            queue.append(parent)

    return sum(g.score for g in groups), sum(len(g.contents) for g in garbages)


print(part_1_and_2())
