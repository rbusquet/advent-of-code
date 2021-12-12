from collections import defaultdict, deque
from pathlib import Path

Graph = defaultdict[str, list[str]]


def paths(graph: Graph, root: str = "start") -> int:
    queue = deque([(root, {root})])
    paths = 0
    while queue:
        current, path = queue.pop()
        if current == "END":
            paths += 1
            continue
        for n in graph[current]:
            if not n.islower() or n not in path:
                queue.append((n, path | {n}))
    return paths


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        graph = Graph(list)
        for line in file:
            src, dst = line.strip().replace("end", "END").split("-")
            graph[src].append(dst)
            graph[dst].append(src)
        return paths(graph)


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        graph = Graph(list)
        for line in file:
            src, dst = line.strip().replace("end", "END").split("-")
            graph[src].append(dst)
            graph[dst].append(src)
        # return paths_reviewed(graph)
    return 0


if __name__ == "__main__":
    print(part_1())
    print(part_2())
