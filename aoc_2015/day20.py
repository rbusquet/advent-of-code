from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    house = 1
    min_presents = int(input.read_text())

    upper_bound = min_presents // 40

    houses = [0] * (upper_bound + 1)

    for elf in range(1, upper_bound + 1):
        for house in range(elf, upper_bound + 1, elf):
            houses[house] += 10 * elf
            print(house, houses[house])

    for house, presents in enumerate(houses):
        if presents >= min_presents:
            return house

    return -1


def part_2() -> int:
    return 0


print(part_1())
print(part_2())
