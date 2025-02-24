from collections import Counter


def part_1() -> None:
    data = []
    with open("input.txt") as f:
        for item in f.readlines():
            data.append(item.strip())

    count2 = 0
    count3 = 0
    for item in data:
        counter = Counter(item.strip())
        rev = {v: k for (k, v) in counter.items()}
        if rev.get(2):
            count2 += 1
        if rev.get(3):
            count3 += 1
    print(f"Checksum: {count2 * count3}")


def part_2() -> None:
    data = []
    with open("input.txt") as f:
        for line in f.readlines():
            data.append(line.strip())

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            diffs = []
            for x, letter in enumerate(data[i]):
                if data[j][x] != letter:
                    diffs.append(x)
            if len(diffs) == 1:
                print(f"boxes {data[i]} and {data[j]}")
                item = list(data[i])
                item.pop(diffs[0])
                print(f"common letters {''.join(item)}")
                break


print("--- DAY 02: part 1 ---")
part_1()

print("--- DAY 02: part 2 ---")
part_2()
