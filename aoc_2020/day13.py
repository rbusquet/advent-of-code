def read_file():
    with open("./input.txt") as f:
        yield from (c.strip() for c in f.readlines())


def part_1() -> None:
    f = read_file()
    earliest = int(next(f))
    service = [*map(int, filter(lambda i: i != "x", next(f).split(",")))]

    times = {}
    for bus in service:
        mod = earliest % bus
        times[bus] = earliest - mod + bus

    bus, timestamp = min(times.items(), key=lambda x: x[1])
    print("--- part 1 ---")
    print(bus * (timestamp - earliest))


def part_2() -> None:
    f = read_file()
    next(f)
    service = enumerate(next(f).split(","))

    valid = [*filter(lambda x: x[1] != "x", service)]
    print(valid)

    # this is cheating
    for i, bus in valid:
        print(f"(t + {i}) mod {bus} = 0;")
    print(894954360381385)

    # for real now
    ts = 0
    step = int(valid[0][1])

    for offset, time in valid[1:]:
        time = int(time)
        while True:
            ts += step
            if (ts + offset) % time == 0:
                # found the first match
                break
        step *= time
    print(ts)
