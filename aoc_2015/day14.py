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
    return 0


print(part_1())
print(part_2())
