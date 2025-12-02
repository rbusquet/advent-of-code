from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    invalid_ids = 0
    ranges = input.read_text().split(",")

    for r in ranges:
        start, end = r.split("-")
        if len(start) % 2 != 0 and len(end) % 2 != 0:
            # no invalid IDs
            continue

        for item_id in range(int(start), int(end) + 1):
            str_id = str(item_id)
            if len(str_id) % 2 != 0:
                continue
            mid = len(str_id) // 2
            left = str_id[:mid]
            right = str_id[mid:]
            if left == right:
                invalid_ids += item_id
    return invalid_ids


def part_2() -> int:
    invalid_ids = 0
    ranges = input.read_text().split(",")

    for r in ranges:
        start, end = r.split("-")

        for item_id in range(int(start), int(end) + 1):
            str_id = str(item_id)
            length = len(str_id)

            for size in range(1, length // 2 + 1):
                if length % size != 0:
                    continue
                chunk = str_id[:size]
                times = length // size
                if chunk * times == str_id:
                    invalid_ids += item_id
                    break

    return invalid_ids


print(part_1())
print(part_2())
