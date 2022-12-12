from __future__ import annotations

import argparse
import math
import re
import sys
from collections import defaultdict, deque
from collections.abc import Iterator
from dataclasses import dataclass, field
from heapq import heappush, nlargest
from operator import add, mul
from typing import ClassVar, Literal, TextIO


@dataclass
class Operation:
    operator: str
    value: int | Literal["self"]

    operators: ClassVar = {"+": add, "*": mul}

    def __call__(self, value: int) -> int:
        operator = self.operators[self.operator]
        if self.value == "self":
            return operator(value, value)
        else:
            return operator(value, self.value)


@dataclass
class Monkey:
    id: int = -1
    items: deque[int] = field(default_factory=deque)
    operation: Operation | None = None
    test: int = -1
    if_true: int = -1
    if_false: int = -1
    monkey_business: int = 0

    def turn_1(self) -> Iterator[tuple[int, int]]:
        print(f"Monkey {self.id}:")
        while self.items:
            item = self.items.popleft()
            print(f"Monkey inspects an item with a worry level of {item}.")
            self.monkey_business += 1
            assert self.operation is not None
            item = self.operation(item)
            print(f"Worry level increases to {item}.")
            item //= 3
            print(
                f"Monkey gets bored with item. Worry level is divided by 3 to {item}."
            )
            test = item % self.test == 0
            if test:
                print(f"Current worry level is divisible by {self.test}.")
                print(
                    f"Item with worry level {item} is thrown to monkey {self.if_true}."
                )
                yield item, self.if_true
            else:
                print(f"Current worry level is not divisible by {self.test}.")
                print(
                    f"Item with worry level {item} is thrown to monkey {self.if_false}."
                )
                yield item, self.if_false

    def turn_2(self, divisor: int) -> Iterator[tuple[int, int]]:
        while self.items:
            item = self.items.popleft()
            self.monkey_business += 1
            assert self.operation is not None
            item = self.operation(item)
            item %= divisor
            test = item % self.test == 0
            if test:
                yield item, self.if_true
            else:
                yield item, self.if_false


monkey_re = re.compile(r"Monkey (\d):")
items_re = re.compile(r"Starting items: ((?:\d+,?\s?)+)")
operation_re = re.compile(r"Operation: new = old (\*|\+) (\d+|old)")
test_re = re.compile(r"Test: divisible by (\d+)")
if_true_re = re.compile(r"If true: throw to monkey (\d+)")
if_false_re = re.compile(r"If false: throw to monkey (\d+)")


@dataclass
class Arguments:
    infile: TextIO = sys.stdin

    def parse_file(self) -> tuple[list[Monkey], dict[int, Monkey]]:
        self.infile.seek(0)
        monkey_map = defaultdict[int, Monkey](Monkey)
        monkeys = list[Monkey]()
        monkey: Monkey | None = None

        for line in args.infile:
            if match := monkey_re.fullmatch(line.strip()):
                monkey_id = int(match.group(1))

                monkey = monkey_map[monkey_id]
                monkey.id = monkey_id
                monkeys.append(monkey)
            assert monkey is not None
            if match := items_re.fullmatch(line.strip()):
                items = match.group(1)
                for item in items.split(", "):
                    monkey.items.append(int(item))
            if match := operation_re.fullmatch(line.strip()):
                operator, value = match.groups()
                if value == "old":
                    monkey.operation = Operation(operator, "self")
                else:
                    monkey.operation = Operation(operator, int(value))
            if match := test_re.fullmatch(line.strip()):
                test = match.group(1)
                monkey.test = int(test)
            if match := if_true_re.fullmatch(line.strip()):
                test = match.group(1)
                monkey.if_true = int(test)
            if match := if_false_re.fullmatch(line.strip()):
                test = match.group(1)
                monkey.if_false = int(test)
        return monkeys, monkey_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    monkeys, monkey_map = args.parse_file()

    for round in range(20):
        for monkey in monkeys:
            for item, throws in monkey.turn_1():
                receiving = monkey_map[throws]
                receiving.items.append(item)

    monkey_business = list[int]()
    for monkey in monkeys:
        heappush(monkey_business, monkey.monkey_business)

    one, two = nlargest(2, monkey_business)
    print("part 1:", one * two)

    monkeys, monkey_map = args.parse_file()

    divisor = math.prod([monkey.test for monkey in monkeys])
    for round in range(10_000):
        for monkey in monkeys:
            for item, throws in monkey.turn_2(divisor):
                receiving = monkey_map[throws]
                receiving.items.append(item)

    monkey_business = list[int]()
    for monkey in monkeys:
        heappush(monkey_business, monkey.monkey_business)

    one, two = nlargest(2, monkey_business)
    print("part 2:", one * two)
