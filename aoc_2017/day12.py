from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    matrix = dict[int, list[int]]()
    for line in input.read_text().splitlines():
        root_str, children = line.split(" <-> ")
        root = int(root_str)
        if root not in matrix:
            matrix[root] = list()
        for child in map(int, children.split(", ")):
            matrix[root].append(child)
            if child not in matrix:
                matrix[child] = list()
            matrix[child].append(root)

    visited = set()
    queue = [0]
    while queue:
        node = queue.pop()
        visited.add(node)
        for child in matrix[node]:
            if child not in visited:
                queue.append(child)
    return len(visited)


def part_2() -> int:
    matrix = dict[int, list[int]]()
    for line in input.read_text().splitlines():
        root_str, children = line.split(" <-> ")
        root = int(root_str)
        if root not in matrix:
            matrix[root] = list()
        for child in map(int, children.split(", ")):
            matrix[root].append(child)
            if child not in matrix:
                matrix[child] = list()
            matrix[child].append(root)

    groups = 0
    visited = set()
    for node in matrix:
        if node not in visited:
            groups += 1
            queue = [node]
            while queue:
                node = queue.pop()
                visited.add(node)
                for child in matrix[node]:
                    if child not in visited:
                        queue.append(child)
    return groups


print(part_1())
print(part_2())
