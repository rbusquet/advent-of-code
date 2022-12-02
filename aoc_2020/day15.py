from progress.bar import PixelBar


def memory_game(initial, stop):
    seen = {}
    last_index = index  # noqa: F821

    for index, value in enumerate(initial):
        seen[value] = index
        last_index = index

    last_spoken = initial[-1]
    # print(f"last spoken: {last_spoken}")
    with PixelBar() as bar:
        for index in range(last_index - 1, stop - 1):
            next_spoken = index - seen.get(last_spoken, index)
            seen[last_spoken] = index
            last_spoken = next_spoken
            if index % ((stop - 1) // 100) == 0:
                bar.next()

    return last_spoken


print("--- part 1 ---")
print(memory_game([14, 3, 1, 0, 9, 5], 2020))
print("--- part 2 ---")
print(memory_game([14, 3, 1, 0, 9, 5], 30_000_000))
