from pathlib import Path


def part_1() -> int:
    """
    ROCK: A and X
    PAPER: B and Y
    SCISSORS: C and Z
    """
    match = {
        "X": "A",
        "Y": "B",
        "Z": "C",
    }
    wins = {
        "X": "C",  # rock beats scissors
        "Y": "A",  # paper beats rock
        "Z": "B",  # scissors beats paper
    }

    base_score = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    with open(Path(__file__).parent / "input.txt") as file:
        total_score = 0
        for line in file:
            line = line.strip()
            p1, p2 = line.split(" ")
            if match[p2] == p1:
                total_score += 3 + base_score[p2]
                print("draw")
            elif wins[p2] == p1:
                total_score += 6 + base_score[p2]
                print("win")
            else:
                total_score += base_score[p2]
                print("loss")
        return total_score


def part_2() -> int:
    """
    ROCK: A and X
    PAPER: B and Y
    SCISSORS: C and Z
    """
    loser_hands = {
        "A": "C",  # rock beats scissors
        "B": "A",  # paper beats rock
        "C": "B",  # scissors beats paper
    }
    winner_hands = {
        "C": "A",  # rock beats scissors
        "A": "B",  # paper beats rock
        "B": "C",  # scissors beats paper
    }

    base_score = {
        "A": 1,
        "B": 2,
        "C": 3,
    }
    translate = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
    }
    with open(Path(__file__).parent / "input.txt") as file:
        total_score = 0
        for line in file:
            line = line.strip()
            p1, p2 = line.split(" ")
            if p2 == "Z":  # win
                winner_hand = winner_hands[p1]
                total_score += 6 + base_score[winner_hand]
                print(
                    f"must win, pick {translate[winner_hand]} against {translate[p1]}"
                )
            elif p2 == "X":  # lose
                loser_hand = loser_hands[p1]
                total_score += 0 + base_score[loser_hand]
                print(
                    f"must lose, pick {translate[loser_hand]} against {translate[p1]}"
                )
            else:  # draw
                total_score += 3 + base_score[p1]
                print(f"must draw, pick {translate[p1]} against {translate[p1]}")
        return total_score


if __name__ == "__main__":
    print(part_1())
    print(part_2())
