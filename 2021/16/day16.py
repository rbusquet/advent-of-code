from __future__ import annotations

import functools
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator
from unittest import TestCase, main


def process_literal(pointer: int, contents: str) -> list[str]:
    parts = list[str]()
    while True:
        word = contents[pointer : pointer + 5]
        parts.append(word[1:])
        if word[0] == "0":
            break
        pointer += 5
    return parts


@dataclass
class Packet:
    full_value: str
    sub_packets: list[Packet] = field(default_factory=list)

    def version(self) -> int:
        return int(self.full_value[:3], 2)

    def evaluate(self) -> int:
        match int(self.full_value[3:6], 2):
            case 4:
                parts = process_literal(6, self.full_value)
                return int("".join(parts), 2)
            case 0:
                return sum(self.evaluate_all())
            case 1:
                return functools.reduce(lambda a, b: a * b, self.evaluate_all(), 1)
            case 2:
                return min(self.evaluate_all())
            case 3:
                return max(self.evaluate_all())
            case 5:
                first, second = self.evaluate_all()
                return first > second
            case 6:
                first, second = self.evaluate_all()
                return first < second
            case 7:
                first, second = self.evaluate_all()
                return first == second
            case _:
                raise Exception("Unknown type")

    def evaluate_all(self) -> Iterator[int]:
        for p in self.sub_packets:
            yield p.evaluate()


def parse_packet(pointer: int, packet: str, all_packets: list[Packet]) -> Packet:
    if pointer >= len(packet):
        raise Exception()
    initial = pointer
    type_id = packet[pointer + 3 : pointer + 6]

    sub_packets = list[Packet]()
    if type_id == "100":
        pointer += 6
        parts = process_literal(pointer, packet)
        pointer += 5 * len(parts)
    else:
        pointer += 6
        length_type = packet[pointer : pointer + 1]
        pointer += 1
        if length_type == "0":
            length_in_bits = int(packet[pointer : pointer + 15], 2)
            pointer += 15
            end_pointer = pointer + length_in_bits
            while pointer < end_pointer:
                next_packet = parse_packet(pointer, packet, all_packets)
                pointer += len(next_packet.full_value)
                sub_packets.append(next_packet)
        else:
            number_of_packets = int(packet[pointer : pointer + 11], 2)
            pointer += 11

            end_count = len(sub_packets) + number_of_packets
            while len(sub_packets) < end_count:
                next_packet = parse_packet(pointer, packet, all_packets)
                pointer += len(next_packet.full_value)
                sub_packets.append(next_packet)

    result = Packet(packet[initial:pointer], sub_packets)
    all_packets.append(result)
    return result


def evaluate(packet: str, all_packets: list[Packet]) -> int:
    bits = ""
    for char in packet:
        bits += f"{int(char, base=16):04b}"
    return parse_packet(0, bits, all_packets).evaluate()


def part_1() -> int:
    all_packets = list[Packet]()
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        evaluate(file.readline(), all_packets)

    versions = 0
    for p in all_packets:
        versions += p.version()
    return versions


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        return evaluate(file.readline(), [])


class TestEvaluate(TestCase):
    def test_everything(self) -> None:
        self.assertEqual(evaluate("C200B40A82", []), 3)
        self.assertEqual(evaluate("04005AC33890", []), 54)
        self.assertEqual(evaluate("880086C3E88112", []), 7)
        self.assertEqual(evaluate("CE00C43D881120", []), 9)
        self.assertEqual(evaluate("D8005AC2A8F0", []), 1)
        self.assertEqual(evaluate("F600BC2D8F", []), 0)
        self.assertEqual(evaluate("9C005AC2F8F0", []), 0)
        self.assertEqual(evaluate("9C0141080250320F1802104A08", []), 1)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
    main()
