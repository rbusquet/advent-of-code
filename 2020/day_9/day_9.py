
def read_file():
    with open('./input.txt') as f:
        yield from map(lambda c: c.strip(), f.readlines())

preamble = []

invalid = None

PREAMBLE = 25

message = [*map(int, read_file())]
for number in message:
    if len(preamble) == PREAMBLE:
        found_sum = False
        for diff in preamble:
            if diff == number:
                continue
            if number - diff in preamble:
                found_sum = True
                break
        if not found_sum:
            invalid = number
            break
        preamble = preamble[1:]
    preamble.append(number)

print("--- part 1 ---")
print(invalid)

print("--- part 2 ---")
index = 0
while True:
    base_index = index
    total = message[base_index]
    contiguous = [message[base_index]]
    while total < invalid:
        base_index += 1
        total += message[base_index]
        contiguous.append(message[base_index])
    if total == invalid:
        print(min(contiguous) + max(contiguous))
        break
    else:
        index += 1
