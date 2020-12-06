from collections import Counter
from typing import List, Tuple

def read_file():
    with open('./input.txt') as f:
        yield from map(lambda c: c.strip(), f.readlines())


groups: List[Tuple[Counter, int]] = []

current_group = Counter()
group_size = 0
for line in read_file():
    if line:
        current_group += Counter(line)
        group_size += 1
    else:
        groups.append([current_group, group_size])
        current_group = Counter()
        group_size = 0

groups.append([current_group, group_size])
print("--- part 1 ---")
print(sum(map(lambda c: len(c[0]), groups)))

print("--- part 2 ---")

total_count = 0
for group, count in groups:
    for ans, ans_count in group.most_common():
        if ans_count == count:
            total_count += 1
        else:
            break

print(total_count)



