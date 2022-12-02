from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Dict, Iterator


def read_file() -> Iterator[str]:
    with open("./input.txt") as f:
        yield from (c.strip() for c in f.readlines())


program = [(x[0], x[1]) for instruction in read_file() if (x := instruction.split(" "))]


class Instruction(ABC):
    @abstractmethod
    def run(self, computer: Computer, *args: int) -> None:
        pass


class Acc(Instruction):
    def run(self, computer: Computer, *args: int) -> None:
        increment = args[0]
        computer.acc += increment
        computer.pointer += 1


class Jmp(Instruction):
    def run(self, computer: Computer, *args: int) -> None:
        increment = args[0]
        computer.pointer += increment


class Noop(Instruction):
    def run(self, computer: Computer, *args: int) -> None:
        computer.pointer += 1


@dataclass
class Computer:
    program: list
    acc: int = 0
    pointer: int = 0
    instructions: ClassVar[Dict[str, Instruction]] = {}

    def detect_loop(self) -> list[int]:
        visited_addresses = []
        while self.pointer not in visited_addresses:
            visited_addresses.append(self.pointer)
            instruction, arg = self.program[self.pointer]
            # print(f'{instruction} {arg}')
            self.instructions[instruction].run(computer, int(arg))
        return visited_addresses

    @classmethod
    def register_instruction(cls, name: str, instruction: Instruction):
        cls.instructions[name] = instruction


Computer.register_instruction("acc", Acc())
Computer.register_instruction("jmp", Jmp())
Computer.register_instruction("nop", Noop())

computer = Computer(program=program)

visited = computer.detect_loop()

print(computer.acc)


changed_addresses = set()

flip = {"jmp": "nop", "nop": "jmp"}
print(visited)
print(computer.pointer)
while True:
    changed_address = None
    changed_instruction = None
    for address in range(len(program)):
        if address in changed_addresses:
            continue
        if program[address][0] != "acc":
            changed_address = address
            changed_instruction = program[address]
            program[address] = (flip[program[address][0]], program[address][1])
            break
    # print(program[changed_address])
    computer = Computer(program=program)
    try:
        visited_this_time = computer.detect_loop()
    except IndexError:
        print(computer.acc)
        print(computer.pointer)
        break
    print(computer.pointer, len(program))
    if computer.pointer > len(program):
        print(computer.acc)
        break
    if changed_address and changed_instruction:
        changed_addresses.add(changed_address)
        program[changed_address] = changed_instruction
