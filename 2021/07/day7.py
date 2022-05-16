from pathlib import Path


def best_alignment(crabs: list[int]) -> int:
    min_fuel = sum(crabs)
    for position in range(len(crabs)):
        # print(f"testing {position=}")
        fuel = 0
        for crab in crabs:
            fuel += abs(crab - position)
            # print(f"Move from {crab} to {position}: {fuel=}")
            if fuel > min_fuel:
                # print(f"{position=} is already bad")
                break
        if fuel < min_fuel:
            min_fuel = fuel
    return min_fuel


def sum_n(n: int) -> int:
    return n * (n + 1) // 2


def best_alignment_part_2(crabs: list[int]) -> int:
    min_fuel = sum(sum_n(crab) for crab in crabs)
    for position in range(len(crabs)):
        # print(f"testing {position=}")
        fuel = 0
        for crab in crabs:
            steps = abs(crab - position)
            # sum of first n integers => n(n+1)/2
            fuel += sum_n(steps)
            # print(f"Move from {crab} to {position}: {fuel=}")
            if fuel > min_fuel:
                # print(f"{position=} is already bad")
                break
        if fuel < min_fuel:
            min_fuel = fuel
    return min_fuel


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        crabs = list(map(int, file.readline().split(",")))
    return best_alignment(crabs)


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        crabs = list(map(int, file.readline().split(",")))
    return best_alignment_part_2(crabs)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
