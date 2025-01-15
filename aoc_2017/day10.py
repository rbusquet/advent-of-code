from knot_hash import knot_hash, knot_hash_step

input = "129,154,49,198,200,133,97,254,41,6,2,1,255,0,191,108"


def part_1():
    numbers = list(range(256))
    numbers, _, _ = knot_hash_step(list(map(int, input.split(","))), numbers)

    return numbers[0] * numbers[1]


def part_2():
    return knot_hash(input)


print(part_1())
print(part_2())
