from collections import defaultdict
from functools import partial
from pathlib import Path
from string import ascii_uppercase, digits, punctuation

mapping = ascii_uppercase + punctuation + digits


print("--- DAY 06: part 1 ---")

coordinates = []
with open(Path(__file__).parent / "input.txt") as f:
    for line in f.readlines():
        coordinates.append(tuple(map(int, line.split(", "))))


def min_max(lst):
    min_ = max_ = -1
    for i in lst:
        if i < min_:
            min_ = i
        if i > max_:
            max_ = i
    return min_, max_


def distance(p, q):
    px, py = p
    qx, qy = q
    return abs(px - qx) + abs(py - qy)


min_x, max_x = min_max(c[0] for c in coordinates)
min_y, max_y = min_max(c[1] for c in coordinates)


def part_1(M=0):
    areas = defaultdict(int)

    for x in range(min_x - M, max_x + M):
        for y in range(min_y - M, max_y + M):
            p = x, y
            closest_points = sorted(coordinates, key=partial(distance, p))
            if distance(p, closest_points[0]) != distance(p, closest_points[1]):
                areas[closest_points[0]] += 1
    return max(areas.values())


def part_2():
    in_region = 0
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            total = 0
            p = (x, y)
            for point in coordinates:
                total += distance(point, p)
                if total >= 10_000:
                    break
            if total < 10_000:
                in_region += 1
    return in_region


print(part_2())
