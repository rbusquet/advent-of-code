from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    lines = input.read_text().splitlines()
    molecule = lines[-1]
    molecules = set[str]()

    for line in lines:
        if not line:
            break
        left, right = line.split(" => ")

        start = -1
        while (start := molecule.find(left, start + 1)) >= 0:
            molecules.add(f"{molecule[:start]}{right}{molecule[start + len(left):]}")

    return len(molecules)


def part_2() -> int:
    lines = input.read_text().splitlines()
    molecule = lines[-1]

    replacements = []

    for line in lines:
        if not line:
            break
        replacements.append(line.split(" => "))

    count = 0
    current = molecule
    replacements = sorted(replacements, key=lambda x: len(x[1]), reverse=True)
    while current != "e":
        for replacement in replacements:
            before, after = replacement
            if after not in current:
                continue
            current = current.replace(after, before, 1)
            count += 1
            break

    return count


print(part_1())
print(part_2())
