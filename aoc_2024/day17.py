from dataclasses import dataclass, field
from math import trunc
from pathlib import Path
from typing import Generator

input = Path(__file__).parent / "input.txt"


@dataclass
class Computer:
    a: int = 0
    b: int = 0
    c: int = 0

    program: list[int] = field(repr=False, default_factory=list)
    pointer: int = field(repr=False, default=0)

    def loop(self) -> Generator[int, None, None]:
        while self.pointer < len(self.program):
            op = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            if op == 0:
                numerator = self.a
                denominator = 2 ** self.combo(operand)
                self.a = trunc(numerator / denominator)
                self.pointer += 2
            elif op == 1:
                self.b ^= operand
                self.pointer += 2
            elif op == 2:
                self.b = self.combo(operand) % 8
                self.pointer += 2
            elif op == 3:
                if self.a:
                    self.pointer = operand
                else:
                    self.pointer += 2
            elif op == 4:
                self.b = self.b ^ self.c
                self.pointer += 2
            elif op == 5:
                yield self.combo(operand) % 8
                self.pointer += 2
            elif op == 6:
                numerator = self.a
                denominator = 2 ** self.combo(operand)
                self.b = trunc(numerator / denominator)
                self.pointer += 2
            elif op == 7:
                numerator = self.a
                denominator = 2 ** self.combo(operand)
                self.c = trunc(numerator / denominator)
                self.pointer += 2
            else:
                raise Exception("invalid op")

    def combo(self, value: int) -> int:
        if value <= 3:
            return value
        if value == 4:
            return self.a
        if value == 5:
            return self.b
        if value == 6:
            return self.c
        raise Exception("invalid combo")


def part_1() -> str:
    information = input.read_text().splitlines()
    a = int(information[0].split()[-1])
    b = int(information[1].split()[-1])
    c = int(information[2].split()[-1])

    program = list(map(int, information[4].split()[-1].split(",")))

    computer = Computer(a, b, c, program)
    print(computer)
    out = list(computer.loop())
    print(computer)
    return ",".join(map(str, out))


def part_1_decompiled():
    information = input.read_text().splitlines()
    a = int(information[0].split()[-1])
    b = c = 0
    outputs = []
    while a:  # 3, 0 (end of program)
        b = a % 8  # 2,4
        b ^= 3  # 1,3
        c = a >> b  # 7,5
        b ^= 5  # 1,5
        a = a >> 3  # 0,3
        b = b ^ c  # 4,3
        outputs.append(b % 8)  # 5,5
    return outputs


def decompiled(a: int) -> list[int]:
    b = c = 0
    outputs = []
    while a:  # 3, 0 (end of program)
        b = a % 8  # 2,4
        b ^= 3  # 1,3
        c = a >> b  # 7,5
        b ^= 5  # 1,5
        a = a >> 3  # 0,3
        b = b ^ c  # 4,3
        outputs.append(b % 8)  # 5,5
    return outputs


def part_2() -> int:
    information = input.read_text().splitlines()

    program = list(map(int, information[4].split()[-1].split(",")))

    def solve(a, index) -> int | None:
        print(oct(a), "->", a)
        if index == -1:
            return a
        for digit in range(8):
            test_a = a + digit * 8**index
            output = decompiled(test_a)
            try:
                if output[index] == program[index]:
                    result = solve(test_a, index - 1)
                    if result:
                        return result
            except IndexError:
                pass
        return None

    return solve(0, len(program) - 1) or 0


print(part_1())
print(part_1_decompiled())
print(part_2())
