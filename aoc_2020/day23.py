cups = list(map(int, "712643589"))

moves = 0
while moves < 100:
    current_cup = cups[0]
    next_cups = cups[1:4]
    print("cups:", cups)
    print("pick up:", next_cups)
    destination_cup = max(0, current_cup - 1) or 9
    while destination_cup in next_cups:
        destination_cup -= 1
        if destination_cup < 1:
            destination_cup = 9
    print("destination:", destination_cup)
    dest_index = cups.index(destination_cup)
    cups[:] = [*cups[4 : dest_index + 1], *next_cups, *cups[dest_index + 1 :], cups[0]]
    moves += 1
print("final:", cups)

one = cups.index(1)
print("".join(map(str, [*cups[one + 1 :], *cups[:one]])))
