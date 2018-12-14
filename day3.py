import re
from typing import NamedTuple


print('--- DAY 03: part 1 ---')


class Claim(NamedTuple):
    id_: int
    x: int
    y: int
    w: int
    t: int


claims = []

regex = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
with open('input3.txt') as f:
    for line in f.readlines():
        match = regex.match(line)
        claims.append(Claim(*[int(x) for x in match.groups()]))


fabric = [[0] * 1000 for i in range(1000)]

for claim in claims:
    for w in range(claim.w):
        for t in range(claim.t):
            fabric[claim.y + t][claim.x + w] += 1

count = 0
for i in fabric:
    for j in i:
        if j > 1:
            count += 1

print(f'Total overlaps: {count}')


print('--- DAY 03: part 2 ---')
for claim in claims:
    test = []
    for w in range(claim.w):
        for t in range(claim.t):
            test.append(fabric[claim.y + t][claim.x + w])
    if all(t == 1 for t in test):
        print(f'Found valid claim: {claim.id_}')
