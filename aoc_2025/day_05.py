from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    lines = iter(input.read_text().splitlines())

    ranges = []

    for line in lines:
        if not line:
            break
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    result = 0
    for line in lines:
        if not line.strip():
            continue
        number = int(line)
        for start, end in ranges:
            if start <= number <= end:
                result += 1
                break
    return result


def part_2() -> int:
    """merge ranges--how many numbers are valid?"""
    lines = iter(input.read_text().splitlines())

    ranges = []
    for line in lines:
        if not line:
            break
        start, end = map(int, line.split("-"))
        ranges.append((start, end))
    ranges.sort()

    merged = []
    current_start, current_end = ranges[0]
    for start, end in ranges[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    merged.append((current_start, current_end))

    result = 0
    for merge_start, merge_end in merged:
        result += merge_end - merge_start + 1
    return result


print(part_1())
print(part_2())
