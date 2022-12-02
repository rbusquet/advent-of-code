from collections import defaultdict


def read_file():
    with open("./input.txt") as f:
        yield from (c.strip() for c in f.readlines())


adapters = set(map(int, read_file()))

diffs = defaultdict[int, int](int)

current_joltage = 0
while adapters:
    for diff in range(1, 4):  # [1,2,3]
        need_joltage = current_joltage + diff
        if need_joltage in adapters:
            current_joltage = need_joltage
            diffs[diff] += 1
            adapters.remove(need_joltage)
            break

one_diff = diffs[1]
three_diff = diffs[3] + 1
print("--- part 1 ---")
print(one_diff * three_diff)


adapters = set(map(int, read_file()))
max_voltage = max(adapters) + 3
adapters.add(0)
adapters.add(max_voltage)

current_joltage = 0

# paths[n] is the total paths from 0 to n
paths = defaultdict[int, int](int)
paths[0] = 1
for adapter in sorted(adapters):
    for diff in range(1, 4):
        next_adapter = adapter + diff
        if next_adapter in adapters:
            paths[next_adapter] += paths[adapter]

print("--- part 2 ---")
print(paths[max_voltage])
