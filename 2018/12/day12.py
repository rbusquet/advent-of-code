from pprint import pprint

INITIAL_STATE = ""
RULES: dict[str, str] = {}

with open("input12.txt") as f:
    first_line = next(f)
    INITIAL_STATE = first_line.split(" ")[-1].strip()
    print(RULES)
    next(f)
    for line in f:
        key, value = line.strip().split(" => ")
        RULES[key] = value
    pprint(RULES)


gutter = "....."
current_generation = INITIAL_STATE

last_generation_sum = 0
diff = 0
for generation in range(50000000000):
    if diff == 53:
        generation_sum = last_generation_sum + diff
        last_generation_sum = generation_sum
        print(
            f"For generation {generation} index sum is {generation_sum}, diff is {diff}"
        )
        print("so...........................")
        final_generation_sum = generation_sum + (50_000_000_000 - generation - 1) * diff
        print(f"For generation {50_000_000_000} index sum is {final_generation_sum}")
        break
    next_generation = ""
    current_generation = f"{gutter}{current_generation}{gutter}"
    # print(f'{generation}: {current_generation}')

    generation_sum = 0
    for index, pot in enumerate(range(len(current_generation))):
        l2 = current_generation[pot - 2] if pot - 2 >= 0 else "."
        l1 = current_generation[pot - 1] if pot - 1 >= 0 else "."
        r1 = current_generation[pot + 1] if pot + 1 < len(current_generation) else "."
        r2 = current_generation[pot + 2] if pot + 2 < len(current_generation) else "."

        result = RULES.get(l2 + l1 + current_generation[pot] + r1 + r2, ".")
        if result == "#":
            generation_sum += index - 5

        next_generation += result

    diff = generation_sum - last_generation_sum
    print(f"For generation {generation} index sum is {generation_sum}, diff is {diff}")
    current_generation = next_generation
    last_generation_sum = generation_sum
