from pathlib import Path

DAY_TEMPLATE = """from pathlib import Path


def part_1():
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        pass


def part_2():
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        pass
"""


for i in range(2, 26):
    dir = Path(f"{i:02}")
    file = dir / f"day{i}.py"
    input_file = dir / "input.txt"
    dir.mkdir(exist_ok=True)
    file.touch(exist_ok=True)
    input_file.touch(exist_ok=True)

    with open(file, "w") as mod:
        mod.write(DAY_TEMPLATE)
