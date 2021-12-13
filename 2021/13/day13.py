from io import StringIO
from pathlib import Path
from typing import NamedTuple


class Dot(NamedTuple):
    x: int
    y: int


class Instruction(NamedTuple):
    axis: str
    value: int


def parse_file() -> tuple[list[Dot], list[Instruction]]:
    dots = list[Dot]()
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


def fold(paper: list[Dot], instruction: Instruction):
    match instruction:
        case Instruction("x", x):
            return fold_left(paper, x)
        case Instruction("y", y):
            return fold_up(paper, y)


def fold_up(paper: list[Dot], line: int) -> list[Dot]:
    folded = set[Dot]()

    for dot in paper:
        match dot:
            case Dot(x, y) if y > line:
                folded.add(Dot(x, 2 * line - y))
            case _:
                folded.add(dot)
    return list(folded)


def fold_left(paper: list[Dot], line: int) -> list[Dot]:
    folded = set[Dot]()

    for dot in paper:
        match dot:
            case Dot(x, y) if x > line:
                folded.add(Dot(2 * line - x, y))
            case _:
                folded.add(dot)
    return list(folded)


def render(paper: list[Dot]) -> str:
    max_y = max(dot[1] for dot in paper)
    max_x = max(dot[0] for dot in paper)

    mapped = {dot: dot for dot in paper}
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


def part_1() -> int:
    dots, instructions = parse_file()
    return len(fold(dots, instructions[0]))


def part_2() -> str:
    dots, instructions = parse_file()

    for instruction in instructions:
        dots = fold(dots, instruction)
    return render(dots)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
