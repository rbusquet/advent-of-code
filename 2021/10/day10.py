import logging
from collections import deque
from pathlib import Path

CHUNK_DELIMTERS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

OPEN_DELIMETER = list(CHUNK_DELIMTERS.keys())
CLOSE_DELIMETER = list(CHUNK_DELIMTERS.values())

CORRUPT_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}

INCOMPLETE_POINTS = {")": 1, "]": 2, "}": 3, ">": 4}
logger = logging.getLogger(__name__)


def part_1_and_2() -> tuple[int, int]:
    with open(Path(__file__).parent / "input.txt") as file:
        corrupt_score = 0
        incomplete_scores = list[int]()
        for lineno, line in enumerate(file):
            line = line.strip()
            queue = deque[tuple[int, str]]()

            chunks = []
            line_score = 0
            for i, ch in enumerate(line):
                if ch in OPEN_DELIMETER:
                    queue.append((i, ch))
                else:
                    last_index, last_delimeter = queue.pop()
                    expected_delimeter = CHUNK_DELIMTERS[last_delimeter]
                    if ch != expected_delimeter:
                        line_score += CORRUPT_POINTS[ch]
                        logger.debug(
                            f"{lineno}:{i} Expected {expected_delimeter}, but found {ch} instead."
                        )
                        break
                    else:
                        chunks.append(line[last_index : i + 1])
                        logger.info(f"found chunk {chunks[-1]}")
            if line_score:
                corrupt_score += line_score
            else:
                score = 0

                while queue:
                    _, ch = queue.pop()
                    score = score * 5 + INCOMPLETE_POINTS[CHUNK_DELIMTERS[ch]]
                logger.debug(f"{lineno}: Incomplete line. Score is {score}.")
                incomplete_scores.append(score)

    incomplete_score = sorted(incomplete_scores)[len(incomplete_scores) // 2]
    return corrupt_score, incomplete_score


if __name__ == "__main__":
    print(part_1_and_2())
