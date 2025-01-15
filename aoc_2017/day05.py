from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    instructions = list(map(int, input.read_text().splitlines()))
    pointer = 0
    steps = 0
    while pointer < len(instructions):
        instruction = instructions[pointer]
        instructions[pointer] += 1
        pointer += instruction
        steps += 1
    return steps


def part_2() -> int:
    instructions = list(map(int, input.read_text().splitlines()))
    pointer = 0
    steps = 0
    while pointer < len(instructions):
        instruction = instructions[pointer]
        if instruction >= 3:
            instructions[pointer] -= 1
        else:
            instructions[pointer] += 1
        pointer += instruction
        steps += 1
    return steps


print(part_1())
print(part_2())
