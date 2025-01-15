from collections import defaultdict, deque
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def strength(bridge: tuple[tuple[int, int], ...]):
    return sum(a + b for a, b in bridge)


def part_1() -> int:
    components_by_port = defaultdict[int, list[tuple[int, int]]](list)

    for line in input.read_text().splitlines():
        a, b = map(int, line.split("/"))
        components_by_port[a].append((a, b))
        components_by_port[b].append((a, b))

    roots = components_by_port[0]

    queue = deque[tuple[tuple[int, int], ...]]()
    queue.extend(
        (
            (0, 0),
            root,
        )
        for root in roots
    )

    paths = set[tuple[tuple[int, int], ...]]()

    while queue:
        path = queue.pop()
        if path in paths:
            continue
        paths.add(path)

        before_last_component, last_component = path[-2], path[-1]
        free_port = (
            last_component[0]
            if last_component[0] not in before_last_component
            else last_component[1]
        )

        potential_connections = components_by_port[free_port]
        for connection in potential_connections:
            if connection in path:
                continue  # already used
            bridge = (*path, connection)
            queue.append(bridge)

    return strength(max(paths, key=strength))


def part_2() -> int:
    components_by_port = defaultdict[int, list[tuple[int, int]]](list)

    for line in input.read_text().splitlines():
        a, b = map(int, line.split("/"))
        components_by_port[a].append((a, b))
        components_by_port[b].append((a, b))

    roots = components_by_port[0]

    queue = deque[tuple[tuple[int, int], ...]]()
    queue.extend(
        (
            (0, 0),
            root,
        )
        for root in roots
    )

    paths = set[tuple[tuple[int, int], ...]]()

    while queue:
        path = queue.pop()
        if path in paths:
            continue
        paths.add(path)

        before_last_component, last_component = path[-2], path[-1]
        free_port = (
            last_component[0]
            if last_component[0] not in before_last_component
            else last_component[1]
        )

        potential_connections = components_by_port[free_port]
        for connection in potential_connections:
            if connection in path:
                continue  # already used
            bridge = (*path, connection)
            queue.append(bridge)

    max_len = len(max(paths, key=len))
    tie = [path for path in paths if len(path) == max_len]
    return strength(max(tie, key=strength))


print(part_1())
print(part_2())
