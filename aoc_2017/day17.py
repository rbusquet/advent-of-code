from pathlib import Path

import progressbar

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    buffer = [0]
    steps = int(input.read_text())

    current_position = 0
    for i in range(1, 2018):
        next_position = (current_position + steps) % len(buffer)
        buffer = buffer[: next_position + 1] + [i] + buffer[next_position + 1 :]
        current_position = next_position + 1
        print(current_position, len(buffer))
    return buffer[(current_position + 1) % len(buffer)]


def part_2() -> int:
    out: int = -1
    len_buffer = 1
    steps = int(input.read_text())

    current_position = 0
    for i in progressbar.progressbar(range(1, 50_000_000 + 1)):
        next_position = (current_position + steps) % len_buffer + 1
        if next_position == 1:
            out = int(i)
        current_position = next_position
        len_buffer += 1
    return out


print(part_1())
print(part_2())
