from collections import defaultdict
from pprint import pprint


def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


lines = read_file()

rules = defaultdict(list)
for line in lines:
    if not line:
        break
    rule, options = line.split(": ")
    options = options.strip('"')
    if options in ["a", "b"]:
        rules[rule] = options
        continue
    for OR in options.strip('"').split(" | "):
        poo = []
        for AND in OR.split(" "):
            poo.append(AND)
        rules[rule].append(poo)

pprint(rules)


def decode_rule(rule_id):
    rule = rules[rule_id]

    if rule in ["a", "b"]:
        return {rule}

    possibilities = set()
    for branch in rule:
        decoded_for_branch = set()
        for rule_id in branch:
            decoded_for_rule = decode_rule(rule_id)
            if not decoded_for_branch:
                decoded_for_branch = decoded_for_rule
            else:
                combined_decoded = set()
                for value in decoded_for_branch:
                    combined_decoded |= {
                        f"{value}{new_value}" for new_value in decoded_for_rule
                    }
                decoded_for_branch = combined_decoded
        possibilities |= decoded_for_branch
    return possibilities


valid = decode_rule("0")
total = 0
all_lines = []
for line in lines:
    all_lines.append(line)
    if line in valid:
        print(line)
        total += 1

print(total)

"""
Part 2
0: 8 11
0: (42 | 42 8) (42 31 | 42 11 31)
(42)...(42)(31)
(42)...(42)(42)(31)(31)
(42)...(42)(42)(42)(31)(31)(31)
"""

valid_42 = decode_rule("42")
valid_31 = decode_rule("31")
print(valid_42)
print(valid_31)


def has_match(valid_lines, line):
    for valid in valid_lines:
        if line.startswith(valid):
            return valid
    return False


total = 0
for line in all_lines:
    # exaust 42
    matches_42 = 0

    while matched := has_match(valid_42, line):
        print(matched)
        print(line)
        line = line[len(matched) :]
        matches_42 += 1
    if not matches_42:
        continue
    matches_31 = 0
    while matched := has_match(valid_31, line):
        print(matched)
        print(line)
        line = line[len(matched) :]
        matches_31 += 1

    if not matches_31 or len(line) != 0:
        continue
    """
    Part 2
    0: 8 11
    0: (42 | 42 8) (42 31 | 42 11 31)
    (42)...(42)(31)
    (42)...(42)(42)(31)(31)
    (42)...(42)(42)(42)(31)(31)(31)
    """
    full_match = matches_31 >= 1 and matches_42 > matches_31
    if full_match:
        total += 1
print(total)
