from collections import Counter
data = []
with open('input2.txt') as f:
    for item in f.readlines():
        data.append(item.strip())

count2 = 0
count3 = 0
for item in data:
    counter = Counter(item.strip())
    rev = {v: k for (k, v) in counter.items()}
    if rev.get(2):
        count2 += 1
    if rev.get(3):
        count3 += 1

print(f'checksum: {count2 * count3}')

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        diffs = []
        for x, letter in enumerate(data[i]):
            if data[j][x] != letter:
                diffs.append(x)
        if len(diffs) == 1:
            print(f'boxes {data[i]} and {data[j]}')
            item = list(data[i])
            item.pop(diffs[0])
            print(f'common letters {"".join(item)}')
            break
