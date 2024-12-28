# mypy: ignore-errors
from pathlib import Path
from typing import Literal

Operators = Literal["AND", "OR", "LSHIFT", "RSHIFT"]
Negate = tuple[Literal["NOT"], str | int]
Operation = tuple[str | int, Operators, str | int]
Single = tuple[str | int]


class Solver:
    operators = {
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
        "LSHIFT": lambda a, b: a << b,
        "RSHIFT": lambda a, b: a >> b,
    }

    def __init__(self) -> None:
        results = dict[str, Negate | Operation | Single | int]()

        with open(Path(__file__).parent / "input.txt") as file:
            for line in file:
                match line.split():
                    case ["NOT", a, "->", b]:
                        results[b] = ("NOT", a)
                    case [a, "->", b]:
                        if a.isdigit():
                            a = int(a)
                        results[b] = (a,)
                    case [
                        a,
                        "AND"
                        | "OR"
                        | "LSHIFT"
                        | "RSHIFT" as operator,
                        b,
                        "->",
                        c,
                    ]:
                        results[c] = (a, operator, b)
        self.results = results

    def do_work(self, wire: str | int) -> int:
        if isinstance(wire, int) or wire.isdigit():
            return int(wire)
        value = self.results[wire]
        match value:
            case int():
                result = value
            case ("NOT", a):
                result = ~self.do_work(a)
            case (a,):
                result = self.do_work(a)
            case (a, operator, b):
                op = self.operators[operator]
                result = op(self.do_work(a), self.do_work(b))
        self.results[wire] = result
        return result


def part_1() -> int:
    solver = Solver()
    solver.do_work("a")
    if isinstance(solver.results["a"], int):
        return int(solver.results["a"])
    raise Exception


def part_2(part_1_result) -> int:
    solver = Solver()
    solver.results["b"] = part_1_result
    solver.do_work("a")
    if isinstance(solver.results["a"], int):
        return int(solver.results["a"])
    raise Exception


if __name__ == "__main__":
    result = part_1()
    print(result)
    print(part_2(result))
