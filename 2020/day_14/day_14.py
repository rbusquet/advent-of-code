import re
from collections import defaultdict


def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


def apply_mask(mask: str, value: int) -> int:
    binary = f"{value:036b}"
    result = ""
    for i, digit in enumerate(binary):
        result += digit if mask[i] == "X" else mask[i]
    return int(result, base=2)


mask = None
memory = defaultdict(int)
mask_exp = re.compile(r"mask = ([01X]{36})")
mem_exp = re.compile(r"mem\[(\d+)\] = (\d+)")

for line in read_file():
    if match := mask_exp.match(line):
        mask = match.groups()[0]
        continue
    elif match := mem_exp.match(line):
        index, value = match.groups()
        memory[int(index)] = apply_mask(mask, int(value))

print("--- part 1 ---")
print(sum(memory.values()))


def memory_address_decoder(mask: str, value: int):
    binary = f"{value:036b}"
    result = []
    x_indexes = []
    # save a temporary "mask" in result with the 0 and 1
    # rules applied
    for i, bit in enumerate(mask):
        if bit == "X":
            x_indexes.append(i)
        result.append(binary[i] if bit == "0" else mask[i])
    # pow(2, len(x_indexes)) is the amount of addresses written
    # in this instruction
    x_format = f"{{0:0{len(x_indexes)}b}}"
    addresses = []
    for i in range(pow(2, len(x_indexes))):
        floats = x_format.format(i)
        for float_index, index in enumerate(x_indexes):
            result[index] = floats[float_index]
        addresses.append(int("".join(result), 2))
    return addresses


mask = None
memory = defaultdict(int)
mask_exp = re.compile(r"mask = ([01X]{36})")
mem_exp = re.compile(r"mem\[(\d+)\] = (\d+)")

for line in read_file():
    if match := mask_exp.match(line):
        mask = match.groups()[0]
        continue
    elif match := mem_exp.match(line):
        index, value = match.groups()
        addresses = memory_address_decoder(mask, int(index))
        for address in addresses:
            memory[address] = int(value)

print("--- part 2 ---")
print(sum(memory.values()))
