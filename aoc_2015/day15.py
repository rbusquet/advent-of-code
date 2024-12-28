from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations_with_replacement
from operator import mul
from pathlib import Path

input = Path(__file__).parent / "input.txt"


@dataclass
class Ingredient:
    name: str
    capacity: int = field(default=0, repr=False)
    durability: int = field(default=0, repr=False)
    flavor: int = field(default=0, repr=False)
    texture: int = field(default=0, repr=False)
    calories: int = field(default=0, repr=False)

    @classmethod
    def from_line(cls, line: str) -> "Ingredient":
        name, contents = line.split(": ")
        ingredient = cls(name=name)
        for property in contents.split(", "):
            name, value = property.split(" ")
            setattr(ingredient, name, int(value))
        return ingredient


def part_1() -> int:
    ingredients = {
        ingredient.name: ingredient
        for line in input.read_text().splitlines()
        if (ingredient := Ingredient.from_line(line))
    }

    names = list(ingredients.keys())

    max_score = 0
    for a in combinations_with_replacement(names, 100):
        counter = Counter(a)
        components = [0, 0, 0, 0]
        calories = 0
        for name, count in counter.items():
            ingredient = ingredients[name]
            components[0] += ingredient.capacity * count
            components[1] += ingredient.durability * count
            components[2] += ingredient.flavor * count
            components[3] += ingredient.texture * count

            calories += ingredient.calories * count

        score = reduce(mul, [max(s, 0) for s in components])
        if score > max_score:
            max_score = score
    return max_score


def part_2() -> int:
    ingredients = {
        ingredient.name: ingredient
        for line in input.read_text().splitlines()
        if (ingredient := Ingredient.from_line(line))
    }

    names = list(ingredients.keys())

    max_score = 0
    for a in combinations_with_replacement(names, 100):
        counter = Counter(a)
        components = [0, 0, 0, 0]
        calories = 0
        for name, count in counter.items():
            ingredient = ingredients[name]
            components[0] += ingredient.capacity * count
            components[1] += ingredient.durability * count
            components[2] += ingredient.flavor * count
            components[3] += ingredient.texture * count

            calories += ingredient.calories * count
        if calories != 500:
            continue
        score = reduce(mul, [max(s, 0) for s in components])
        if score > max_score:
            max_score = score
    return max_score


print(part_1())
print(part_2())
