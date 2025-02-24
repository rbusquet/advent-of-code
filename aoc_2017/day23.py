import math
from collections import defaultdict, deque
from collections.abc import Generator, Iterator
from itertools import takewhile
from pathlib import Path

input = Path(__file__).parent / "input.txt"


class Computer(defaultdict[str, int]):
    def __init__(self, *program: str, id: int | None = None) -> None:
        super().__init__(int)
        if id is not None:
            self["p"] = id
        self.id = id
        self.op_counter = defaultdict[str, int](int)
        self.queue = deque[int]()
        self.gen = self.run(*program)

    def get_value(self, address: str) -> int:
        if address.isalpha():
            return self[address]
        return int(address)

    def run(self, *program: str) -> Generator[int | None, int]:
        pointer = 0
        while True:
            if pointer >= len(program):
                return
            op, *args = program[pointer].split()
            self.op_counter[op] += 1
            print(self)
            if args[0] == "b":
                pass
            if op == "snd":
                sound = self.get_value(args[0])
                # print(f"{self.id} sounding {sound}")
                yield sound
            if op == "set":
                self[args[0]] = self.get_value(args[1])
            if op == "add":
                self[args[0]] += self.get_value(args[1])
            if op == "sub":
                self[args[0]] -= self.get_value(args[1])
            if op == "mul":
                self[args[0]] *= self.get_value(args[1])
            if op == "mod":
                self[args[0]] %= self.get_value(args[1])
            if op == "rcv":
                received = yield
                if received is not None:
                    # print(f"{self.id} receives {received}")
                    self[args[0]] = received
                else:
                    continue
            if op in "jgz":
                if self.get_value(args[0]) > 0:
                    pointer += self.get_value(args[1])
                    continue
            if op in "jnz":
                if self.get_value(args[0]) != 0:
                    pointer += self.get_value(args[1])
                    continue
            pointer += 1

    def __str__(self) -> str:
        result = [f"ID: {self.id}"]
        for a, b in sorted(self.items()):
            result.append(f"{a}: {b}")
        return " ".join(result)

    def run_until_idle(self, input: deque[int] | None = None) -> Iterator[int]:
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

    def count_op(self, op: str) -> int:
        return self.op_counter[op]


def part_1() -> int:
    computer = Computer(*input.read_text().splitlines())
    list(computer.run_until_idle())
    return computer.count_op("mul")


def decompiled_program(a: int):
    b = 65
    c = 65

    if a == 1:
        b = 106500
        c = 123500

    h = 0

    for b in range(b, c + 1, 17):
        f = 1
        # pairwise multiplying every number between 2 and b
        # and finding if any of them results in b. if it does,
        # b is not prime
        for d in range(2, b):
            for e in range(2, b):
                if d * e == b:
                    f = 0
                    break
            if f == 0:
                break

        if f == 0:
            h += 1
    return h


def optimized_program():
    b = 106500
    c = 123500

    # Function to check if a number is prime
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    non_prime_count = 0
    for current_value in range(b, c + 1, 17):
        if not is_prime(current_value):
            non_prime_count += 1

    return non_prime_count


def part_2() -> int:
    return optimized_program()


# print(part_1())
print(part_2())
