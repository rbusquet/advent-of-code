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

    def aggregated_version(self) -> int:
        return self.version() + sum(p.aggregated_version() for p in self.sub_packets)

    def evaluate(self) -> int:
        # fmt: off
        match int(self.full_value[3:6], 2):
            case 0: return sum(self.evaluate_all())
            case 1: return functools.reduce(lambda a, b: a * b, self.evaluate_all(), 1)
            case 2: return min(self.evaluate_all())
            case 3: return max(self.evaluate_all())
            case 4:
                parts = process_literal(6, self.full_value)
                return int("".join(parts), 2)
            case 5:
                first, second = self.evaluate_all()
                return first > second
            case 6:
                first, second = self.evaluate_all()
                return first < second
            case 7:
                first, second = self.evaluate_all()
                return first == second
            case _: raise Exception("Unknown type")
        # fmt: on

    def evaluate_all(self) -> Iterator[int]:
        for p in self.sub_packets:
            yield p.evaluate()


def parse_packet(pointer: int, packet: str) -> Packet:
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
                next_packet = parse_packet(pointer, packet)
                pointer += len(next_packet.full_value)
                sub_packets.append(next_packet)
        else:
            number_of_packets = int(packet[pointer : pointer + 11], 2)
            pointer += 11

            end_count = len(sub_packets) + number_of_packets
            while len(sub_packets) < end_count:
                next_packet = parse_packet(pointer, packet)
                pointer += len(next_packet.full_value)
                sub_packets.append(next_packet)

    return Packet(packet[initial:pointer], sub_packets)


def hex_to_packet(packet: str) -> Packet:
    bits = ""
    for char in packet:
        bits += f"{int(char, base=16):04b}"
    return parse_packet(0, bits)


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        return hex_to_packet(file.readline()).aggregated_version()


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        return hex_to_packet(file.readline()).evaluate()


class TestHexToPacket(TestCase):
    def test(self) -> None:
        self.assertEqual(hex_to_packet("C200B40A82").evaluate(), 3)
        self.assertEqual(hex_to_packet("04005AC33890").evaluate(), 54)
        self.assertEqual(hex_to_packet("880086C3E88112").evaluate(), 7)
        self.assertEqual(hex_to_packet("CE00C43D881120").evaluate(), 9)
        self.assertEqual(hex_to_packet("D8005AC2A8F0").evaluate(), 1)
        self.assertEqual(hex_to_packet("F600BC2D8F").evaluate(), 0)
        self.assertEqual(hex_to_packet("9C005AC2F8F0").evaluate(), 0)
        self.assertEqual(hex_to_packet("9C0141080250320F1802104A08").evaluate(), 1)


if __name__ == "__main__":
    main()
