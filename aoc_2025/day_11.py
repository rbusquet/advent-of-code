import enum
from collections import defaultdict
from graphlib import TopologicalSorter
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    graph = defaultdict[str, list[str]](list)
    inverted_graph = defaultdict[str, list[str]](list)
    for line in input.read_text().splitlines():
        from_node, *nodes = line.replace(":", "").split()
        for to_node in nodes:
            graph[to_node].append(from_node)
        inverted_graph[from_node] += nodes

    ts = TopologicalSorter(graph)
    paths = defaultdict[str, int](int)
    paths["you"] = 1

    for node in ts.static_order():
        if node not in graph:
            continue

        for neighbor in graph[node]:
            paths[node] += paths[neighbor]

    return paths["out"]


class State(enum.Flag):
    seen_svr = enum.auto()
    seen_dac = enum.auto()
    seen_fft = enum.auto()


def part_2() -> int:
    return 0


print(part_1())
print(part_2())
