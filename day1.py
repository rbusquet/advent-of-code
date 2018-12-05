data = []
with open('input1.txt') as f:
    for line in f.readlines():
        data.append(int(line))

frequency = 0
for delta in data:
    frequency += delta
print(f'part 1: {frequency}')

all_frequencies = {0}
frequency = 0
index = 0

while True:
    frequency += data[index]
    if frequency in all_frequencies:
        break
    all_frequencies.add(frequency)
    index = (index + 1) % len(data)

print(f'part 2: {frequency}')
