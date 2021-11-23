from collections import defaultdict, deque
from typing import Iterator


def read_file() -> Iterator[str]:
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


to_containers = defaultdict[str, set[str]](set)
to_contents = defaultdict[str, dict[str, int]](dict)

for rule in read_file():
    bag_info, contents = rule.split(" contain ")
    if "no other bags" in contents:
        continue
    style, color, _ = bag_info.split(" ")
    container = f"{style} {color}"
    for content in contents.split(", "):
        # number, style, color, "bags."
        count, style, color, _ = content.split(" ")
        bag = f"{style} {color}"
        containers = to_containers[bag]
        containers.add(container)

        content_count = to_contents[container]
        content_count[bag] = int(count)

visited = set()


def part_1(initial: str) -> None:
    stack = deque([initial])
    while stack:
        current = stack.pop()
        for container in to_containers[current]:
            visited.add(container)
            stack.append(container)

    print("--- part 1 ---")
    print(len(visited))


def part_2(initial: str) -> None:
    stack = deque([(1, initial)])

    total = 0
    while stack:
        multiplier, bag = stack.pop()
        for content, count in to_contents[bag].items():
            actual_count = multiplier * count
            total += actual_count
            stack.append((actual_count, content))

    print("--- part 2 ---")
    print(total)


part_1("shiny gold")
part_2("shiny gold")
