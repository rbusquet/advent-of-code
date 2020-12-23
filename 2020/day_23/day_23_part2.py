from progress.bar import ShadyBar

cups = list(map(int, "712643589"))
linked = {cup: cups[i + 1] for i, cup in enumerate(cups) if i < 8}

rest_linked = {i: i+1 for i in range(10, 1_000_000)}
linked = {**linked, **rest_linked}
linked[9] = 10
linked[1_000_000] = 7

print(len(linked))

moves = 0
head = 1_000_000
with ShadyBar(max=10_000_000) as bar:
    bar.suffix = 'ETA: %(eta)ds'
    while moves < 10_000_000:

        current_cup = linked[head]
        n1 = linked[current_cup]
        n2 = linked[n1]
        n3 = linked[n2]
        next_cups = (n1, n2, n3)

        # print("pick up:", next_cups)
        destination_cup = max(0, current_cup - 1) or 1_000_000
        while destination_cup in next_cups:
            destination_cup -= 1
            if destination_cup < 1:
                destination_cup = 1_000_000
        # print("destination:", destination_cup)
        # the cup after the destination cup closes the move
        next_to_destination = linked[destination_cup]
        # n1 moved after destination cup
        new_next_to_destination = n1
        # the one next to n3 will move to after the current
        new_next_to_current = linked[n3]
        # n3 is now before the one that used to be next to destination
        new_next_to_n3 = next_to_destination

        linked[destination_cup] = new_next_to_destination
        linked[n3] = new_next_to_n3
        linked[current_cup] = new_next_to_current

        # head is now current_cup
        head = current_cup
        moves += 1
        if moves % 10_000 == 0:
            bar.goto(moves)

p1 = linked[1]
p2 = linked[p1]
print(p1, '*', p2, '=', p1 * p2)
