from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import NamedTuple


class Dot(NamedTuple):
    x: int
    y: int


class Instruction(NamedTuple):
    axis: str
    value: int


class Paper(list[Dot]):
    def fold(self, instruction: Instruction) -> Paper:
        match instruction:
            case Instruction("x", x):
                return self._fold_left(x)
            case Instruction("y", y):
                return self._fold_up(y)

    def render(self) -> str:
        max_y = max(dot[1] for dot in self)
        max_x = max(dot[0] for dot in self)

        mapped = {dot: dot for dot in self}
        io = StringIO()
        for i in range(max_y + 1):
            for j in range(max_x + 1):
                if mapped.get((j, i)):
                    print("🀫", end="", file=io)
                else:
                    print(" ", end="", file=io)
            print(file=io)
        io.seek(0)
        return io.read()

    def _fold_up(self, line: int) -> Paper:
        to_remove = list[Dot]()
        for dot in self:
            match dot:
                case Dot(x, y) if y > line:
                    to_remove.append(dot)
                    new_dot = Dot(x, 2 * line - y)
                    if new_dot not in self:
                        self.append(new_dot)
        for dot in to_remove:
            self.remove(dot)
        return self

    def _fold_left(self, line: int) -> Paper:
        to_remove = list[Dot]()
        for dot in self:
            match dot:
                case Dot(x, y) if x > line:
                    to_remove.append(dot)
                    new_dot = Dot(2 * line - x, y)
                    if new_dot not in self:
                        self.append(new_dot)
        for dot in to_remove:
            self.remove(dot)
        return self


def parse_file() -> tuple[Paper, list[Instruction]]:
    dots = Paper()
    instructions = list[Instruction]()
    with open(Path(__file__).parent / "input.txt") as file:
        while line := next(file).strip():
            x, y = map(int, line.split(","))
            dots.append(Dot(x, y))
        for line in file:
            instruction = line.split(" ")[-1].strip()
            axis, value = instruction.split("=")
            instructions.append(Instruction(axis, int(value)))
    return dots, instructions


def part_1() -> int:
    dots, instructions = parse_file()
    return len(dots.fold(instructions[0]))


def part_2() -> str:
    dots, instructions = parse_file()

    for instruction in instructions:
        dots.fold(instruction)
    return dots.render()


if __name__ == "__main__":
    print(part_1())
    print(part_2())
