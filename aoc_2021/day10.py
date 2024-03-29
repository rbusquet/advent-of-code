import logging
from collections import deque
from pathlib import Path
from statistics import median

CHUNK_DELIMITERS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

OPEN_DELIMITER = list(CHUNK_DELIMITERS.keys())
CLOSE_DELIMITER = list(CHUNK_DELIMITERS.values())

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
                if ch in OPEN_DELIMITER:
                    queue.append((i, ch))
                else:
                    last_index, last_delimiter = queue.pop()
                    expected_delimiter = CHUNK_DELIMITERS[last_delimiter]
                    if ch != expected_delimiter:
                        line_score += CORRUPT_POINTS[ch]
                        logger.debug(
                            f"{lineno}:{i} Expected {expected_delimiter}, "
                            f"but found {ch} instead."
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
                    score = score * 5 + INCOMPLETE_POINTS[CHUNK_DELIMITERS[ch]]
                logger.debug(f"{lineno}: Incomplete line. Score is {score}.")
                incomplete_scores.append(score)

    incomplete_score = int(median(sorted(incomplete_scores)))
    return corrupt_score, incomplete_score


if __name__ == "__main__":
    print(part_1_and_2())
