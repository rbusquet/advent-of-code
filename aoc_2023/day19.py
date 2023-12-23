import argparse
import functools
import operator
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Iterator, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


RULE_REGEX = re.compile(r"(\w+)([<>])(\d+)")
WORKFLOW_REGEX = re.compile(r"(\w+){(.+)}")


@dataclass
class Rule:
    operation: str
    next: str

    def terms(self) -> tuple[str, str, int]:
        match = RULE_REGEX.match(self.operation)
        if match is None:
            raise ValueError(f"Invalid rule: {self.operation}")
        key, opcode, value = match.groups()
        return key, opcode, int(value)

    def execute(self, item: dict[str, int]) -> str | None:
        if not self.operation:
            return self.next

        operations = {"<": operator.lt, ">": operator.gt}
        key, opcode, value = self.terms()

        result = operations[opcode](item[key], value)
        return self.next if result else None

    def match_range(
        self, item: dict[str, range]
    ) -> tuple[dict[str, range], dict[str, range]]:
        if not self.operation:
            return item, {}

        key, opcode, value = self.terms()
        current_range = item[key]

        if opcode == "<":
            return (
                {**item, key: range(current_range.start, value)},
                {**item, key: range(value, current_range.stop)},
            )
        if opcode == ">":
            return (
                {**item, key: range(value + 1, current_range.stop)},
                {**item, key: range(current_range.start, value + 1)},
            )
        raise ValueError(f"Invalid opcode: {opcode}")


@dataclass
class Workflow:
    name: str
    rules: list[Rule] = field(default_factory=list)

    def execute(self, item: dict[str, int]) -> str:
        for rule in self.rules:
            next_workflow = rule.execute(item)
            if next_workflow is not None:
                return next_workflow
        raise ValueError(f"Invalid item: {item}")

    def match_range(self, item: dict[str, range]):
        unmatched = item
        for rule in self.rules:
            matched, unmatched = rule.match_range(unmatched)
            yield rule.next, matched


def parse_workflow(line: str) -> Workflow:
    match = WORKFLOW_REGEX.match(line)
    if match is None:
        raise ValueError(f"Invalid line: {line}")
    name, rules = match.groups()
    workflow = Workflow(name=name)
    for rule in rules.split(","):
        if ":" not in rule:
            workflow.rules.append(Rule("", rule))
            continue
        operation, next_workflow = rule.split(":")
        workflow.rules.append(Rule(operation, next_workflow))
    return workflow


def parse_item(line: str) -> dict[str, int]:
    regex = re.compile(r"(\w)=(\d+)")
    return dict((key, int(value)) for key, value in regex.findall(line))


def part_1(file: TextIO) -> int:
    file.seek(0)

    workflows = dict[str, Workflow]()
    for line in strip_lines(file):
        if not line:
            break
        workflow = parse_workflow(line)
        workflows[workflow.name] = workflow

    accepted = list[dict[str, int]]()
    for line in strip_lines(file):
        if not line:
            break
        item = parse_item(line)
        workflow = workflows["in"]
        while workflow is not None:
            result = workflow.execute(item)
            if result == "A":
                accepted.append(item)
                break
            if result == "R":
                break
            workflow = workflows[result]
    return sum(sum(item.values()) for item in accepted)


def part_2(file: TextIO) -> int:
    file.seek(0)

    workflows = dict[str, Workflow]()
    for line in strip_lines(file):
        if not line:
            break
        workflow = parse_workflow(line)
        workflows[workflow.name] = workflow

    queue = deque(
        [
            (
                workflows["in"],
                {
                    "x": range(1, 4000 + 1),
                    "m": range(1, 4000 + 1),
                    "a": range(1, 4000 + 1),
                    "s": range(1, 4000 + 1),
                },
            )
        ]
    )

    total = 0

    while queue:
        workflow, to_match = queue.pop()

        for next_workflow, next_item in workflow.match_range(to_match):
            if next_workflow == "A":
                combinations = 1
                for r in next_item.values():
                    combinations *= len(r)
                total += combinations
            elif next_workflow == "R":
                continue
            else:
                queue.append((workflows[next_workflow], next_item))

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
