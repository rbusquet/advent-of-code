def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


f = read_file()
earliest = int(next(f))
service = [*map(int, filter(lambda i: i != 'x', next(f).split(',')))]

times = {}
for bus in service:
    mod = earliest % bus
    times[bus] = earliest - mod + bus


bus, timestamp = min(times.items(), key=lambda x: x[1])
print("--- part 1 ---")
print(bus * (timestamp - earliest))

f = read_file()
next(f)
service = enumerate(next(f).split(','))

valid = [*filter(lambda x: x[1] != 'x', service)]
print(valid)

for i, bus in valid:
    print(f"(t + {i}) mod {bus} = 0;")
# :eyes: https://www.wolframalpha.com/input/?i=solve+%28t+%2B+0%29+mod+29+%3D+0%3B+%28t+%2B+23%29+mod+37+%3D+0%3B+%28t+%2B+29%29+mod+631+%3D+0%3B+%28t+%2B+47%29+mod+13+%3D+0%3B+%28t+%2B+48%29+mod+19+%3D+0%3B+%28t+%2B+52%29+mod+23+%3D+0%3B+%28t+%2B+60%29+mod+383+%3D+0%3B+%28t+%2B+70%29+mod+41+%3D+0%3B+%28t+%2B+77%29+mod+17+%3D+0%3B
print(894954360381385)
