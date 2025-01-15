from collections import Counter
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

input = Path(__file__).parent / "input.txt"


@dataclass
class Program:
    name: str
    weight: int = 0
    parent: "Program | None" = None
    leaves: list["Program"] = field(default_factory=list)

    @cached_property
    def tree_weight(self) -> int:
        base = self.weight
        if not self.leaves:
            return base
        return base + sum(leaf.tree_weight for leaf in self.leaves)

    @cached_property
    def balanced(self):
        sub_tree_weights = Counter(leaf.tree_weight for leaf in self.leaves)
        return len(sub_tree_weights) == 1


class Programs(dict[str, Program]):
    def get_or_create(self, name: str, weight: int = 0) -> Program:
        if name in self:
            if weight:
                self[name].weight = weight
            return self[name]
        return self.setdefault(name, Program(name, weight))

    def root(self) -> Program:
        for i in self.values():
            if not i.parent:
                return i
        raise Exception("No root found")


def part_1() -> str:
    programs = Programs()

    for line in input.read_text().splitlines():
        match line.split(" -> "):
            case [program_info, holding]:
                name, weight_info = program_info.split()
                weight = int(weight_info.strip("()"))
                root = programs.get_or_create(name, weight)
                for name in holding.split(", "):
                    leaf = programs.get_or_create(name)
                    leaf.parent = root
                    root.leaves.append(leaf)

    return programs.root().name


def part_2() -> int:
    programs = Programs()

    for line in input.read_text().splitlines():
        match line.split(" -> "):
            case [program_info, holding]:
                name, weight_info = program_info.split()
                weight = int(weight_info.strip("()"))
                root = programs.get_or_create(name, weight)
                for name in holding.split(", "):
                    leaf = programs.get_or_create(name)
                    leaf.parent = root
                    root.leaves.append(leaf)
            case [program_info]:
                name, weight_info = program_info.split()
                weight = int(weight_info.strip("()"))
                programs.get_or_create(name, weight)

    root = programs.root()

    while True:
        for leaf in root.leaves:
            if not leaf.balanced:
                print(f"{leaf.name} is unbalanced")
                root = leaf
                break
        else:
            print(f"{root.name} is unbalanced, but all its children are balanced.")
            for leaf in root.leaves:
                print(f"{leaf.name} weights {leaf.tree_weight}")
            weights = Counter(leaf.tree_weight for leaf in root.leaves)
            good, bad = weights.most_common()

            for leaf in root.leaves:
                if leaf.tree_weight == bad[0]:
                    answer = leaf.weight - abs(good[0] - bad[0])
                    print(f"{leaf.name} is the wrong one. it should weight {answer}")
                    return answer
            return 1
        continue


print(part_1())
print(part_2())
