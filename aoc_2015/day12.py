import json
from pathlib import Path
from typing import Any

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    with input.open() as file:
        data = json.load(file)

    def accumulate(d: Any) -> int:
        if isinstance(d, int):
            return d
        if isinstance(d, list):
            return sum(accumulate(v) for v in d)
        if isinstance(d, dict):
            return sum(accumulate(v) for v in d.values())
        return 0

    return accumulate(data)


def part_2() -> int:
    with input.open() as file:
        data = json.load(file)

    def accumulate(d: Any) -> int:
        if isinstance(d, int):
            return d
        if isinstance(d, list):
            return sum(accumulate(v) for v in d)
        if isinstance(d, dict):
            if "red" in d.values():
                return 0
            result = 0
            for v in d.values():
                result += accumulate(v)
            return result
        return 0

    return accumulate(data)


print(part_1())
print(part_2())
