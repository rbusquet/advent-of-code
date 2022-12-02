from pathlib import Path


def part_1():
    with open(Path(__file__).parent / "input.txt") as file:
        horizontal = depth = 0
        for command in file:
            match command.split(" "):
                case ["forward", distance]:
                    horizontal += int(distance)
                case ["up", distance]:
                    depth -= int(distance)
                case ["down", distance]:
                    depth += int(distance)
        return horizontal * depth


def part_2():
    with open(Path(__file__).parent / "input.txt") as file:
        horizontal = depth = aim = 0
        for command in file:
            match command.split(" "):
                case ["forward", distance]:
                    horizontal += int(distance)
                    depth += int(distance) * aim
                case ["up", distance]:
                    aim -= int(distance)
                case ["down", distance]:
                    aim += int(distance)
        return horizontal * depth


if __name__ == "__main__":
    print(part_1())  # 1604850
    print(part_2())
