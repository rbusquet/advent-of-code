from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    layers = dict()
    for line in input.read_text().splitlines():
        layer, depth = map(int, line.split(": "))
        layers[layer] = depth

    severity = 0
    for layer, depth in layers.items():
        if layer % (2 * depth - 2) == 0:
            severity += layer * depth
    return severity


def part_2() -> int:
    layers = dict()
    for line in input.read_text().splitlines():
        layer, depth = map(int, line.split(": "))
        layers[layer] = depth

    delay = 0
    while True:
        for layer, depth in layers.items():
            if (layer + delay) % (2 * depth - 2) == 0:
                break
        else:
            return delay
        delay += 1


print(part_1())
print(part_2())
