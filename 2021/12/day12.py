from collections import defaultdict, deque
from pathlib import Path

Graph = defaultdict[str, list[str]]


def paths(graph: Graph, root: str = "start") -> int:
    queue = deque[tuple[str, list[str]]]([(root, [])])
    paths = 0
    while queue:
        current, path = queue.pop()
        path.append(current)
        if current == "END":
            # print(path)
            paths += 1
            continue
        for n in graph[current]:
            if not n.islower() or n not in path:
                queue.append((n, path[:]))
    return paths


def paths_reviewed(graph: Graph, root: str = "start") -> int:
    queue = deque[tuple[str, list[str], bool]]([(root, [], True)])
    paths = 0
    while queue:
        current, path, can_visit_twice = queue.pop()
        path.append(current)
        if current.islower() and path.count(current) == 2:
            can_visit_twice = False
        if current == "END":
            # print(path)
            paths += 1
            continue
        for n in graph[current]:
            if can_visit_twice and n != "start":
                queue.append((n, path[:], can_visit_twice))
                continue
            if not n.islower() or n not in path:
                queue.append((n, path[:], can_visit_twice))
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
        return paths_reviewed(graph)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
