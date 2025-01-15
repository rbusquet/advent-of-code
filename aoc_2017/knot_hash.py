import unittest
from functools import reduce

input = "129,154,49,198,200,133,97,254,41,6,2,1,255,0,191,108"


def knot_hash_step(
    lengths: list[int], numbers: list[int], current: int = 0, skip: int = 0
) -> tuple[list[int], int, int]:
    for length in lengths:
        loop = numbers[current : current + length]
        if current + length > len(numbers):
            loop += numbers[: current + length - len(numbers)]
        loop = loop[::-1]
        for i in range(length):
            numbers[(current + i) % len(numbers)] = loop[i]
        current += length + skip
        current %= len(numbers)
        skip += 1
    return numbers, current, skip


def knot_hash(value: str) -> str:
    suffix = [17, 31, 73, 47, 23]
    lengths = [ord(x) for x in value]

    numbers = list(range(256))
    current = 0
    skip = 0
    for _ in range(64):
        numbers, current, skip = knot_hash_step(
            lengths + suffix, numbers, current, skip
        )
    dense = []
    for i in range(0, 256, 16):
        block = numbers[i : i + 16]
        dense.append(reduce(lambda a, b: a ^ b, block))
    return "".join(f"{n:02x}" for n in dense)


class TestKnotHash(unittest.TestCase):
    def test_knot_hash(self) -> None:
        assert knot_hash("") == "a2582a3a0e66e6e86e3812dcb672a272"
        assert knot_hash("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
        assert knot_hash("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
        assert knot_hash("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"
        assert knot_hash(input) == "62e2204d2ca4f4924f6e7a80f1288786"


if __name__ == "__main__":
    unittest.main()
