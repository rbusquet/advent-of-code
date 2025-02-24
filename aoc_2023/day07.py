from __future__ import annotations

import argparse
import enum
import sys
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property, total_ordering
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


class HandType(enum.IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


@total_ordering
class Hand:
    # cspell:words 23456789TJQKA
    CARDS = "23456789TJQKA"

    def __init__(self, cards: str, bid: int = 0) -> None:
        self.cards = cards
        self.bid = bid
        self.counter = Counter(cards)

    def __repr__(self) -> str:
        return f"{self.cards!r}: {self.type.name}"

    @cached_property
    def type(self) -> HandType:
        if len(self.counter) == 1:
            # five of a kind
            return HandType.FIVE_OF_A_KIND
        if len(self.counter) == 2:
            if 4 in self.counter.values():
                # four of a kind
                return HandType.FOUR_OF_A_KIND
            # full house
            return HandType.FULL_HOUSE
        if len(self.counter) == 3:
            if 3 in self.counter.values():
                # three of a kind
                return HandType.THREE_OF_A_KIND
            # two pair
            return HandType.TWO_PAIR
        if len(self.counter) == 4:
            # one pair
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    @cached_property
    def strength(self) -> int:
        return sum(
            self.CARDS.index(card) * 13**i for i, card in enumerate(self.cards[::-1])
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return self.type == other.type and self.strength == other.strength

    def __gt__(self, other: Hand) -> bool:
        if self.type == other.type:
            return self.strength > other.strength
        return self.type > other.type


class JokerHand(Hand):
    # cspell:words J23456789TQKA
    CARDS = "J23456789TQKA"

    @cached_property
    def type(self) -> HandType:
        if "J" not in self.counter:
            return super().type
        if len(self.counter) == 1:
            # five of a kind
            return HandType.FIVE_OF_A_KIND

        def replace_joker() -> Iterable[HandType]:
            for count in range(1, self.counter["J"] + 1):
                for card, _ in self.counter.most_common():
                    if card == "J":
                        continue
                    yield Hand(self.cards.replace("J", card, count)).type

        return max(replace_joker())


def strip_lines(file: TextIO) -> Iterable[str]:
    for line in file:
        yield line.strip()


def part_1(file: TextIO) -> int:
    file.seek(0)
    hands = list[Hand]()
    for line in strip_lines(file):
        if not line:
            continue
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid)))
    hands.sort()
    return sum(i * hand.bid for i, hand in enumerate(hands, start=1))


def part_2(file: TextIO) -> int:
    file.seek(0)
    hands = list[JokerHand]()
    for line in strip_lines(file):
        if not line:
            continue
        cards, bid = line.split()
        hands.append(JokerHand(cards, int(bid)))
    hands.sort()
    return sum(i * hand.bid for i, hand in enumerate(hands, start=1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
