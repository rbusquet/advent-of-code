from collections import defaultdict
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    reindeers = dict[str, tuple[int, int, int]]()

    for line in input.read_text().splitlines():
        words = line.split()
        reindeers[words[0]] = int(words[3]), int(words[6]), int(words[13])

    distances = dict[str, int]()

    total_time = 2_503

    for reindeer, info in reindeers.items():
        speed, time, rest = info

        stretches = total_time // (time + rest)
        remaining = total_time - stretches * (time + rest)

        distances[reindeer] = stretches * speed * time
        if remaining <= time:
            distances[reindeer] += speed * remaining
        else:
            distances[reindeer] += speed * time

    return max(distances.values())


def part_2() -> int:
    reindeers = dict[str, tuple[int, int, int]]()

    for line in input.read_text().splitlines():
        words = line.split()
        reindeers[words[0]] = int(words[3]), int(words[6]), int(words[13])

    points = defaultdict[str, int](int)

    distances = dict[str, int]()
    total_time = 2_503

    for seconds in range(1, total_time + 1):
        # print(f"Time: {seconds}s")
        for reindeer, info in reindeers.items():
            speed, time, rest = info

            stretches = seconds // (time + rest)
            remaining = seconds - stretches * (time + rest)

            distances[reindeer] = stretches * speed * time
            if remaining <= time:
                distances[reindeer] += speed * remaining
            else:
                distances[reindeer] += speed * time

        lead = max(distances.values())
        for name, distance in distances.items():
            if distance == lead:
                # print(f"{name} on the lead at {lead}km!")
                points[name] += 1

    return max(points.values())


print(part_1())
print(part_2())
