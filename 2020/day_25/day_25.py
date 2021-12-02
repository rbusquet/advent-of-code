card_public_key = 1526110
door_public_key = 20175123


def infer_loop_size(key: int, subject: int) -> int:
    loop_size = 0
    value = 1
    while value != key:
        loop_size += 1
        value *= subject
        value %= 20201227
    return loop_size


def transform_subject(loop_size: int, subject: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    return value


card_loop_size = infer_loop_size(card_public_key, 7)
door_loop_size = infer_loop_size(door_public_key, 7)
print(card_loop_size, door_loop_size)

encryption_key_card = transform_subject(card_loop_size, door_public_key)
encryption_key_door = transform_subject(door_loop_size, card_public_key)

assert encryption_key_card == encryption_key_door

# TIL:
assert encryption_key_card == pow(door_public_key, card_loop_size, 20201227)
print(encryption_key_card)
