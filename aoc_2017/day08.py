import operator
from collections import defaultdict
from pathlib import Path

input = Path(__file__).parent / "input.txt"


operators = {
    "==": operator.eq,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
    "!=": operator.ne,
    "inc": operator.add,
    "dec": operator.sub,
}


def part_1() -> int:
    memory = defaultdict[str, int](int)
    for line in input.read_text().splitlines():
        reg, op, offset, _, test_reg, test, val = line.split()

        if operators[test](memory[test_reg], int(val)):
            memory[reg] = operators[op](memory[reg], int(offset))

    return max(memory.values())


class Memory(defaultdict[str, int]):
    def __init__(self):
        self.max_value = 0
        return super().__init__(int)

    def __setitem__(self, key: str, value: int) -> None:
        self.max_value = max(self.max_value, value)
        return super().__setitem__(key, value)


def part_2() -> int:
    memory = Memory()
    for line in input.read_text().splitlines():
        reg, op, offset, _, test_reg, test, val = line.split()

        if operators[test](memory[test_reg], int(val)):
            memory[reg] = operators[op](memory[reg], int(offset))

    return memory.max_value


print(part_1())
print(part_2())
