from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> tuple[int, tuple[int, ...]]:
    memory = list(map(int, input.read_text().split()))
    visited = set[tuple[int, ...]]()

    cycles = 0

    while True:
        max_blocks = max(memory)
        max_index = memory.index(max_blocks)
        memory[max_index] = 0
        for _ in range(max_blocks):
            max_index += 1
            memory[max_index % len(memory)] += 1
        cycles += 1
        if (m := tuple(memory)) in visited:
            return cycles, m

        visited.add(m)


def part_2(initial: tuple[int, ...]) -> int:
    memory = list(initial)

    cycles = 0
    while True:
        max_blocks = max(memory)
        max_index = memory.index(max_blocks)
        memory[max_index] = 0
        for _ in range(max_blocks):
            max_index += 1
            memory[max_index % len(memory)] += 1
        cycles += 1
        if tuple(memory) == initial:
            return cycles


cycles, memory = part_1()
print(cycles)
print(part_2(memory))
