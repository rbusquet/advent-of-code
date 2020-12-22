from progress.bar import ChargingBar
from os import environ


def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())

NARRATE = environ.get("NARRATE")

def print_wrapper(string):
    if NARRATE:
        print(string)


player_1 = (
    14,
    6,
    21,
    10,
    1,
    33,
    7,
    13,
    25,
    8,
    17,
    11,
    28,
    27,
    50,
    2,
    35,
    49,
    19,
    46,
    3,
    38,
    23,
    5,
    43,
)
player_2 = (
    18,
    9,
    12,
    39,
    48,
    24,
    32,
    45,
    47,
    41,
    40,
    15,
    22,
    36,
    30,
    26,
    42,
    34,
    20,
    16,
    4,
    31,
    37,
    44,
    29,
)


def combat(player_1, player_2):
    while player_1 and player_2:
        print_wrapper(player_1)
        print_wrapper(player_2)

        card_1, player_1 = player_1[0], player_1[1:]
        card_2, player_2 = player_2[0], player_2[1:]

        if card_1 > card_2:
            player_1 = (*player_1, card_1, card_2)
        else:
            player_2 = (*player_2, card_2, card_1)

    return max(player_1, player_2)


winner = combat(player_1, player_2)
total = 0

for i, x in enumerate(winner):
    total += x * (len(winner) - i)
print("--- part 1 ---")
print(total)


def copy_deck(deck, size):
    s = deck[:size]
    assert len(s) == size
    return s


def recursive_combat(player_1, player_2, level=1, bar: ChargingBar = None):
    print_wrapper(f"=== Game {level} ===")
    visited_games = set()
    round = 0

    while player_1 and player_2:
        round += 1

        if (player_1, player_2) in visited_games:
            return 1, player_1
        visited_games.add((player_1, player_2))

        print_wrapper(f"Player 1's deck: {player_1}")
        print_wrapper(f"Player 2's deck: {player_2}")

        card_1, player_1 = player_1[0], player_1[1:]
        card_2, player_2 = player_2[0], player_2[1:]
        print_wrapper(f"Player 1 plays: {card_1}")
        print_wrapper(f"Player 2 plays: {card_2}")

        # breakpoint()

        if len(player_1) >= card_1 and len(player_2) >= card_2:
            print_wrapper("Playing a sub-game to determine the winner...")
            winner, _ = recursive_combat(
                copy_deck(player_1, card_1),
                copy_deck(player_2, card_2),
                level=level + 1,
            )
            print_wrapper(f"...anyway, back to game 1.")
            if winner == 1:
                print_wrapper(f"Player 1 wins round {round} of game {level}!")
                player_1 = (*player_1, card_1, card_2)
            else:
                print_wrapper(f"Player 2 wins round {round} of game {level}!")
                player_2 = (*player_2, card_2, card_1)
        else:
            if card_1 > card_2:
                print_wrapper(f"Player 1 wins round {round} of game {level}!")
                player_1 = (*player_1, card_1, card_2)
            else:
                print_wrapper(f"Player 2 wins round {round} of game {level}!")
                player_2 = (*player_2, card_2, card_1)
        if bar and max(len(player_1), len(player_2)) > bar.index:
            bar.goto(max(len(player_1), len(player_2)))

    winner = max(player_1, player_2)
    if winner == player_1:
        print_wrapper(f"The winner of game {level} is player 1!")
    else:
        print_wrapper(f"The winner of game {level} is player 2!")

    return (1 if winner == player_1 else 2), winner


player_1 = (
    14,
    6,
    21,
    10,
    1,
    33,
    7,
    13,
    25,
    8,
    17,
    11,
    28,
    27,
    50,
    2,
    35,
    49,
    19,
    46,
    3,
    38,
    23,
    5,
    43,
)
player_2 = (
    18,
    9,
    12,
    39,
    48,
    24,
    32,
    45,
    47,
    41,
    40,
    15,
    22,
    36,
    30,
    26,
    42,
    34,
    20,
    16,
    4,
    31,
    37,
    44,
    29,
)

if not NARRATE:
    with ChargingBar(max=len(player_1) + len(player_2)) as bar:
        winner, deck = recursive_combat(player_1, player_2, bar=bar)
else:
    winner, deck = recursive_combat(player_1, player_2)
total = 0

for i, x in enumerate(deck):
    total += x * (len(deck) - i)
print("--- part 2 ---")
print(total)
