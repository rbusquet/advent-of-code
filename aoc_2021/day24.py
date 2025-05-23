from __future__ import annotations

import typing as tp
from collections import defaultdict
from pathlib import Path

type Var = tp.Literal["w", "x", "y", "z"]


class ALUDecompiler(defaultdict[Var, str]):
    __instructions: tp.ClassVar[dict[str, Instruction]] = {}

    def __init__(self) -> None:
        self.functions = list[str]()
        return super().__init__(str)

    @classmethod
    def register(cls, name: str) -> tp.Callable[[Instruction], Instruction]:
        def decorator(fn: Instruction) -> Instruction:
            cls.__instructions[name] = fn
            return fn

        return decorator

    def run(self, program: tp.Iterable[str]) -> None:
        for instruction in program:
            match instruction.split():
                case [inst, a]:
                    self.__instructions[inst](self, a)
                case [inst, a, "w" | "x" | "y" | "z" as b]:
                    self.__instructions[inst](self, a, b)
                case [inst, a, b]:
                    self.__instructions[inst](self, a, int(b))

    def register_function(self) -> None:
        if not self.functions:
            self.functions.append("lambda w, z: print(w, z)")
            return
        self.functions.append(self["z"])


class Instruction(tp.Protocol):
    def __call__(self, alu: ALUDecompiler, *vars: Var | int) -> None: ...


@ALUDecompiler.register("inp")
def inp(alu: ALUDecompiler, *vars: Var | int) -> None:
    alu.register_function()
    variable = vars[0]
    assert isinstance(variable, str)
    alu.update(dict.fromkeys(["w", "x", "y"], "0"))
    alu[variable] = variable
    alu["z"] = "z"


def op_factory(operator: str) -> Instruction:
    def base(alu: ALUDecompiler, *vars: Var | int) -> None:
        a, b = vars
        assert isinstance(a, str)
        if isinstance(b, str):
            result = alu[b] or "0"
        else:
            result = str(b)
        alu[a] = f"({alu[a] or 0}{operator}{result})"

    return base


ALUDecompiler.register("add")(op_factory("+"))
ALUDecompiler.register("mul")(op_factory("*"))
ALUDecompiler.register("div")(op_factory("/"))
ALUDecompiler.register("mod")(op_factory("%"))
ALUDecompiler.register("eql")(op_factory("=="))


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        program = file.readlines()
    decompiler = ALUDecompiler()
    decompiler.run(program)

    z = 0

    for fun in decompiler.functions[1:]:
        z = eval(fun, {"w": w, "z": z})  # type: ignore[name-defined]  # noqa: F821

    return 0


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        pass
    return 0


if __name__ == "__main__":
    print(part_1())
    print(part_2())
