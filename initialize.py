import argparse
from pathlib import Path

DAY_TEMPLATE = """from pathlib import Path


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        pass


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        pass


if __name__ == "__main__":
    print(part_1())
    print(part_2())
"""


parser = argparse.ArgumentParser()
parser.add_argument("year", help="Advent of code year", default=2021, type=int)

args = parser.parse_args()

if __name__ == "__main__":

    for i in range(1, 26):
        dir = Path(f"{args.year}", f"{i:02}")
        file = dir / f"day{i}.py"
        input_file = dir / "input.txt"
        dir.mkdir(exist_ok=True, parents=True)
        file.touch(exist_ok=True)
        input_file.touch(exist_ok=True)

        with open(file, "w") as mod:
            mod.write(DAY_TEMPLATE)
