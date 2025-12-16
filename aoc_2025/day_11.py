from collections import defaultdict
from graphlib import TopologicalSorter
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    graph = defaultdict[str, list[str]](list)
    for line in input.read_text().splitlines():
        from_node, *nodes = line.replace(":", "").split()
        for to_node in nodes:
            graph[to_node].append(from_node)

    ts = TopologicalSorter(graph)
    paths = defaultdict[str, int](int)
    paths["you"] = 1

    for node in ts.static_order():
        if node not in graph:
            continue

        for neighbor in graph[node]:
            paths[node] += paths[neighbor]

    return paths["out"]


def count_paths(
    graph: dict[str, list[str]], order: list[str], start: str, end: str
) -> int:
    paths = defaultdict[str, int](int)
    paths[start] = 1

    for node in order:
        if node not in graph:
            continue

        for neighbor in graph[node]:
            paths[node] += paths[neighbor]

    return paths[end]


def part_2() -> int:
    graph = defaultdict[str, list[str]](list)
    for line in input.read_text().splitlines():
        from_node, *nodes = line.replace(":", "").split()
        for to_node in nodes:
            graph[to_node].append(from_node)

    ts = TopologicalSorter(graph)
    m1, m2 = "dac", "fft"
    order = list(ts.static_order())
    if order.index(m1) > order.index(m2):
        m1, m2 = m2, m1

    paths_m1 = count_paths(graph, order, "svr", m1)
    paths_m2 = count_paths(graph, order, m1, m2)
    paths_out = count_paths(graph, order, m2, "out")

    return paths_m1 * paths_m2 * paths_out


print(part_1())
print(part_2())
