from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import TextIO


@dataclass
class CPU:
    x: int = 1
    signal_strength: int = 0
    watch_cycles: list[int] = field(default_factory=list)

    _cycle: int = 1

    @property
    def cycle(self) -> int:
        return self._cycle

    @cycle.setter
    def cycle(self, value: int) -> None:
        """
        Using the cycle setter to read state in each cycle change
        """
        for i in range(self._cycle, value):
            if i in self.watch_cycles:
                self.signal_strength += i * self.x

            self.light_pixel(i)
        self._cycle = value

    def light_pixel(self, cycle: int) -> None:
        column = (cycle - 1) % 40
        if column == 0:
            print()
        if column in [self.x - 1, self.x, self.x + 1]:
            print("█", end="")
        else:
            print(".", end="")

    def process(self, program: TextIO) -> None:
        for line in program:
            match line.split():
                case ["noop"]:
                    self.cycle += 1
                case ["addx", value]:
                    self.cycle += 2
                    self.x += int(value)


def main(args: Arguments) -> None:
    cpu = CPU(watch_cycles=[20, 60, 100, 140, 180, 220])
    cpu.process(args.infile)
    print()
    print(cpu.signal_strength)


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    main(args)
