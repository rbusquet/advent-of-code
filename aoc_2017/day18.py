from collections import defaultdict, deque
from itertools import takewhile
from pathlib import Path
from typing import Generator, Iterator

from more_itertools import last

input = Path(__file__).parent / "input.txt"


class Computer(defaultdict[str, int]):
    counter: int

    def __init__(self, *program: str, id: int | None = None) -> None:
        super().__init__(int)
        if id is not None:
            self["p"] = id
        self.id = id
        self.counter = 0
        self.queue = deque[int]()
        self.gen = self.run(*program)

    def get(self, address: str) -> int:
        if address.isalpha():
            return self[address]
        return int(address)

    def run(self, *program: str) -> Generator[int | None, int, None]:
        pointer = 0
        while True:
            if pointer >= len(program):
                return
            op, *args = program[pointer].split()
            if args[0] == "b":
                pass
            if op == "snd":
                sound = self.get(args[0])
                # print(f"{self.id} sounding {sound}")
                self.counter += 1
                yield sound
            if op == "set":
                self[args[0]] = self.get(args[1])
            if op == "add":
                self[args[0]] += self.get(args[1])
            if op == "mul":
                self[args[0]] *= self.get(args[1])
            if op == "mod":
                self[args[0]] %= self.get(args[1])
            if op == "rcv":
                received = yield
                if received is not None:
                    # print(f"{self.id} receives {received}")
                    self[args[0]] = received
                else:
                    continue
            if op == "jgz":
                if self.get(args[0]) > 0:
                    pointer += self.get(args[1])
                    continue
            pointer += 1

    def __str__(self) -> str:
        result = [f"ID: {self.id}"]
        for a, b in sorted(self.items()):
            result.append(f"{a}: {b}")
        return " ".join(result)

    def run_until_idle(self, input: deque[int]) -> Iterator[int]:
        out = list[int]()
        try:
            out = list(takewhile(lambda a: a is not None, self.gen))
            if input:
                next_sound = self.gen.send(input.popleft())
                if next_sound is not None:
                    out.append(next_sound)
        except StopIteration:
            out = []

        for o in out:
            if o is not None:
                yield o
                self.queue.append(o)


def part_1() -> int:
    program = Computer(*input.read_text().splitlines())

    out = program.run_until_idle(deque())
    return last(out)


def part_2() -> int:
    c0 = Computer(id=0, *input.read_text().splitlines())
    c1 = Computer(id=1, *input.read_text().splitlines())

    while True:
        out0 = list(c0.run_until_idle(c1.queue))
        out1 = list(c1.run_until_idle(c0.queue))

        if not out0 and not out1 and not c0.queue and not c1.queue:
            break
    return c1.counter


print(part_1())
print(part_2())
