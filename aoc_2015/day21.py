import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterator

input = Path(__file__).parent / "input.txt"


@dataclass
class Item:
    name: str
    cost: int = 0
    damage: int = 0
    armor: int = 0


@dataclass
class Character:
    hit_points: int
    damage: int = 0
    armor: int = 0

    def can_damage(self, enemy: "Character") -> bool:
        total_damage = self.damage - enemy.armor
        return total_damage > 0

    def hit(self, enemy: "Character") -> None:
        total_damage = self.damage - enemy.armor
        if total_damage > 0:
            enemy.hit_points -= total_damage


WEAPONS = [
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
]

ARMOR = [
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
]

RINGS = [
    Item("Damage +1", 25, 1, 0),
    Item("Damage +2", 50, 2, 0),
    Item("Damage +3", 100, 3, 0),
    Item("Defense +1", 20, 0, 1),
    Item("Defense +2", 40, 0, 2),
    Item("Defense +3", 80, 0, 3),
]


def generate_items() -> Iterator[list[Item]]:
    for weapon in WEAPONS:
        yield [weapon]
        for armor in ARMOR:
            yield [weapon, armor]
            for ring in RINGS:
                yield [weapon, armor, ring]
            for pair in combinations(RINGS, 2):
                yield [weapon, armor, *pair]
        for ring in RINGS:
            yield [weapon, ring]
        for pair in combinations(RINGS, 2):
            yield [weapon, *pair]


def part_1() -> int:
    boss = Character(104, 8, 1)
    player = Character(100)

    min_cost = sys.maxsize
    for items in generate_items():
        cost = sum(i.cost for i in items)
        if cost > min_cost:
            continue
        player.damage = sum(i.damage for i in items)
        player.armor = sum(i.armor for i in items)

        if not player.can_damage(boss):
            continue

        boss_hp = boss.hit_points
        player_hp = player.hit_points
        boss_damage = max(0, boss.damage - player.armor)
        player_damage = max(0, player.damage - boss.armor)

        while True:
            boss_hp -= player_damage
            # print(
            #     f"The player deals {player_damage}; the boss goes down to {boss_hp} points"
            # )
            if boss_hp <= 0:
                # print("player wins")
                min_cost = min(min_cost, cost)
                break
            player_hp -= boss_damage

            # print(
            #     f"The boss deals {player_damage}; the player goes down to {boss_hp} points"
            # )
            if player_hp <= 0:
                # print("boss wins")
                break

    return min_cost


def part_2() -> int:
    boss = Character(104, 8, 1)
    player = Character(100)

    max_cost = 0
    for items in generate_items():
        cost = sum(i.cost for i in items)
        if cost < max_cost:
            continue
        player.damage = sum(i.damage for i in items)
        player.armor = sum(i.armor for i in items)

        if not player.can_damage(boss):
            continue

        boss_hp = boss.hit_points
        player_hp = player.hit_points
        boss_damage = max(0, boss.damage - player.armor)
        player_damage = max(0, player.damage - boss.armor)

        while True:
            boss_hp -= player_damage
            if boss_hp <= 0:
                # print(f"player wins, player spends {cost}")
                break
            player_hp -= boss_damage

            if player_hp <= 0:
                # print(f"boss wins, player spends {cost}")
                max_cost = max(cost, max_cost)
                break

    return max_cost


print(part_1())
print(part_2())
