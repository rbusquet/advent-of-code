from collections import defaultdict

SERIAL_NUMBER = 7803

matrix = defaultdict(int)


def power(x, y):
    x, y = x + 1, y + 1
    rack_id = x + 10
    level = rack_id * y
    level += SERIAL_NUMBER
    level *= rack_id
    hundreds = int(level / 100) % 10
    return hundreds - 5


matrix = defaultdict(int)
for y in range(1, 301):
    for x in range(1, 301):
        p = power(x, y)
        matrix[y, x] = (
            p
            + matrix[y - 1, x]
            + matrix[y, x - 1]
            - matrix[y - 1, x - 1]
        )


best = sum(x for x in matrix.values() if x < 0)
print(best)
best_x = 0
best_y = 0
best_size = 0
for size in range(1, 301):
    for y in range(size, 301):
        for x in range(size, 301):
            A, B, C, D = (
                matrix[y, x],
                matrix[y - size, x],
                matrix[y, x - size],
                matrix[y - size, x - size]
            )
            size_area = A - B - C + D
            if size_area > best:
                best = size_area
                best_x = x
                best_size = size
                best_y = y
                print(f'Found area={best} at {x}x{y} with size {size}')


print(best_x - best_size + 2)
print(best_y - best_size + 2)
print(best_size)
