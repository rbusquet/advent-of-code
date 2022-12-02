import re
from collections import defaultdict
from functools import reduce
from operator import and_


def read_file():
    with open("./input.txt") as f:
        yield from (c.strip() for c in f.readlines())


allergen_to_recipes = defaultdict(list)

food_re = re.compile(r"(.*)\(contains([\s\w,]*)\)")

all_foods = []

for line in read_file():
    if match := food_re.match(line):
        food, allergens = match.groups()
    else:
        continue
    ingredients = food.strip().split(" ")
    all_foods.append(ingredients)

    allergens = [a.strip() for a in allergens.split(",")]

    for allergen in allergens:
        allergen_to_recipes[allergen].append(set(ingredients))


dangerous = set()

for foods in allergen_to_recipes.values():
    appears_in_all = reduce(and_, foods)
    dangerous |= appears_in_all

count = 0
for food in all_foods:
    for ingredient in food:
        if ingredient not in dangerous:
            count += 1
print(count)

matched_allergens = dict[str, str]()

while len(matched_allergens) < len(dangerous):
    dangerous_to_allergen = defaultdict(set)
    for allergen, foods in allergen_to_recipes.items():
        if allergen in matched_allergens.values():
            continue
        appears_in_all = reduce(and_, foods)
        for danger in appears_in_all:
            dangerous_to_allergen[danger].add(allergen)
    for food, allergens in dangerous_to_allergen.items():
        if len(allergens) == 1:
            matched_allergens[food] = allergens.pop()
            break

cannonical_list = ",".join(
    sorted(matched_allergens.keys(), key=lambda food: matched_allergens[food])
)
print(cannonical_list)
