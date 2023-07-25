from unittest import TestCase, main


def memory_game(initial: list[int], turns: int) -> int:
    seen = {}

    for turn, value in enumerate(initial):
        seen[value] = [turn + 1, 1]

    last_spoken = initial[-1]
    for turn in range(len(initial), turns):
        last_turn, count = seen[last_spoken]
        if count == 1:
            say = 0
        else:
            say = turn - last_turn
        seen[last_spoken][0] = turn

        if say in seen:
            seen[say][1] += 1
        else:
            seen[say] = [turn + 1, 1]

        last_spoken = say
    return last_spoken


class TestDay15(TestCase):
    def test_example(self):
        self.assertEqual(memory_game([0, 3, 6], 10), 0)
        self.assertEqual(memory_game([1, 3, 2], 2020), 1)
        self.assertEqual(memory_game([2, 1, 3], 2020), 10)
        self.assertEqual(memory_game([1, 2, 3], 2020), 27)
        self.assertEqual(memory_game([2, 3, 1], 2020), 78)
        self.assertEqual(memory_game([3, 2, 1], 2020), 438)
        self.assertEqual(memory_game([3, 1, 2], 2020), 1836)

        self.assertEqual(memory_game([14, 3, 1, 0, 9, 5], 2020), 614)

        self.assertEqual(memory_game([14, 3, 1, 0, 9, 5], 30_000_000), -1)


main()
