import argparse
import operator
import re
import sys
from dataclasses import dataclass, field
from typing import Iterator, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


RULE_REGEX = re.compile(r"(\w+)([<>])(\d+)")


@dataclass
class Rule:
    operation: str
    next: str

    def next_workflow(self, item: dict[str, int]) -> str | None:
        return self.next if self.execute(item) else None

    def execute(self, item: dict[str, int]) -> bool:
        operations = {"<": operator.lt, ">": operator.gt}

        if not self.operation:
            return True
        match = RULE_REGEX.match(self.operation)
        if match is None:
            raise ValueError(f"Invalid rule: {self.operation}")
        key, opcode, value = match.groups()

        return operations[opcode](item[key], int(value))


@dataclass
class Workflow:
    name: str
    rules: list[Rule] = field(default_factory=list)

    def execute(self, item: dict[str, int]) -> str:
        for rule in self.rules:
            next_workflow = rule.next_workflow(item)
            if next_workflow is not None:
                return next_workflow
        raise ValueError(f"Invalid item: {item}")


WORKFLOW_REGEX = re.compile(r"(\w+){(.+)}")


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
        print(item)
    return sum(sum(item.values()) for item in accepted)


def part_2(file: TextIO) -> int:
    file.seek(0)
    return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
