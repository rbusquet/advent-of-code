import operator
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    wires = defaultdict[str, int](int)
    gates = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}

    instructions = dict[str, tuple[str, str, Callable[[int, int], int]]]()
    for line in input.read_text().splitlines():
        match line.split():
            case [wire, value]:
                wires[wire[:-1]] = int(value)
            case [a, op, b, "->", c]:
                instructions[c] = a, b, gates[op]

    def solve(wire: str) -> int:
        if wire in wires:
            return wires[wire]
        if wire in instructions:
            a, b, op = instructions[wire]
            result = op(solve(a), solve(b))
            wires[wire] = result
            return result
        raise Exception("invalid wire")

    z_wires = []
    for wire in instructions:
        if wire.startswith("z"):
            z_wires.append(wire)
            solve(wire)
    z_wires.sort()
    z_wires.reverse()
    # for z in z_wires:
    #     print(f"{z}: {wires[z]}")
    output = "".join(str(wires[z]) for z in z_wires)

    return int(output, 2)


def part_2() -> int:
    return 0


print(part_1())
print(part_2())
