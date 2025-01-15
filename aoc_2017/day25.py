from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import takewhile
from pathlib import Path
from typing import NamedTuple

input = Path(__file__).parent / "input.txt"


class Instruction(NamedTuple):
    write: int
    offset: int
    next_state: str


@dataclass
class State:
    id: str
    zero_instruction: Instruction
    one_instruction: Instruction

    @classmethod
    def from_instructions(cls, instructions: list[str]):
        state_id = instructions[0][-2]

        zero_instruction = Instruction(
            write=int(instructions[2][-2]),
            offset=1 if instructions[3].endswith("right.") else -1,
            next_state=instructions[4][-2],
        )
        one_instruction = Instruction(
            write=int(instructions[6][-2]),
            offset=1 if instructions[7].endswith("right.") else -1,
            next_state=instructions[8][-2],
        )
        return State(state_id, zero_instruction, one_instruction)


def part_1() -> int:
    lines = iter(input.read_text().splitlines())
    current_state_id = next(lines)[-2]
    tape = defaultdict[int, int](int)
    cursor = 0

    checksum_count = int(next(lines).split()[-2])
    empty = next(lines)
    assert empty == ""

    states = dict[str, State]()

    while instructions := list(takewhile(bool, lines)):
        state = State.from_instructions(instructions)
        states[state.id] = state

    for _ in range(checksum_count):
        current_state = states[current_state_id]
        if tape[cursor] == 0:
            write, offset, next_state = current_state.zero_instruction
        else:
            write, offset, next_state = current_state.one_instruction
        tape[cursor] = write
        cursor += offset
        current_state_id = next_state

    return Counter(tape.values())[1]


def part_2() -> int:
    return 0


print(part_1())
print(part_2())
