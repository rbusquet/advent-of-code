from string import ascii_lowercase

print('--- DAY 5: part 1 ---')


def destroy(letter, next_letter):
    same_letter = letter.lower() == next_letter.lower()
    opposite_sign = letter != next_letter
    return opposite_sign and same_letter


def break_array(array, index):
    return array[:index], array[index], array[index + 1], array[index + 2:]


buffer = ''
with open('input5.txt') as f:
    buffer = f.read(1)
    while True:
        letter = buffer[-1:]
        next_letter = f.read(1)
        if not next_letter:
            break
        should_destroy = destroy(letter, next_letter)
        if should_destroy:
            buffer = buffer[:-1]
        else:
            buffer += next_letter
        # print(buffer[:50])

print(f'Processed polymer has length={len(buffer)}')

print('--- DAY 5: part 2 ---')
for unit in ascii_lowercase:
    with open('input5.txt') as f:
        buffer = f.read(1)
        while buffer.lower() == unit:
            buffer = f.read(1)
        while True:
            letter = buffer[-1:]
            next_letter = f.read(1)
            if next_letter.lower() == unit:
                continue
            if not next_letter:
                break
            should_destroy = destroy(letter, next_letter)
            if should_destroy:
                buffer = buffer[:-1]
            else:
                buffer += next_letter
            # print(buffer[:50])

    print(f'Removing units {unit} length of polymer is {len(buffer)}')
