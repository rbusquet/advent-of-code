from collections import defaultdict
from pathlib import Path

CORRECT_DISPLAY_MAP = dict(
    zip(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [
            set("abcefg"),
            set("cf"),
            set("acdeg"),
            set("acdfg"),
            set("bcdf"),
            set("abdfg"),
            set("abdefg"),
            set("acf"),
            set("abcdefg"),
            set("abcdfg"),
        ],
    )
)

DISPLAY_TO_NUMBER = {frozenset(v): k for k, v in CORRECT_DISPLAY_MAP.items()}

EASY_DIGITS_LENGTHS = [2, 4, 3, 7]
EASY_DIGITS = [1, 4, 7, 8]
EASY_DECODER = dict(zip(EASY_DIGITS_LENGTHS, EASY_DIGITS))


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        count = 0
        for line in file:
            _, outputs = line.strip().split(" | ")
            for digit in outputs.split(" "):
                count += len(digit) in EASY_DIGITS_LENGTHS

    return count


HARD_DECODER = {5: [2, 3, 5], 6: [0, 6, 9]}


def part_2() -> int:  # noqa: C901
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        final = 0

        for line in file:
            patterns, outputs = line.strip().split(" | ")

            decoder = defaultdict[str, list[str]](set)

            sorted_patterns = sorted(map(set[str], patterns.split()), key=len)

            patterns_by_length = defaultdict[int, list[str]](list)

            for current in sorted_patterns:
                match len(current):
                    case 2:
                        for segment in current:
                            decoder[segment] = ["c", "f"]
                        one = current
                    case 3:
                        # already match 1
                        top_bar = current - one
                        is_a = next(iter(top_bar))
                        decoder[is_a] = ["a"]  # acf - cf
                    case 4:
                        for segment in current:
                            if segment not in decoder:
                                decoder[segment] = ["b", "d"]
                    case 5:
                        patterns_by_length[5].append(current)
                    case 6:
                        patterns_by_length[6].append(current)
                    case 7:
                        for segment in current:
                            if segment not in decoder:
                                decoder[segment] = ["e", "g"]  # abcdefg - cf - bd - a
                        pass
            # at this point, all decoders look like:
            # 'a' -> ['c', 'f']  # meaning a and d want to light up number 1
            # 'd' -> ['c', 'f']
            #
            # 'c' -> ['a']  # c signal means top bar
            #
            # 'b' -> ['b', 'd']  # b and f want to light up the top L
            # 'f' -> ['b', 'd']  # (and will light up on 4, 5 and 6 for example)
            #
            # 'g' -> ['e', 'g']  # g and e want to light up the lower L
            # 'e' -> ['e', 'g']  # (just a coincidence????)
            # solve 5
            for current in patterns_by_length[5]:
                base = set[frozenset[str]]()
                for segment in current:
                    possibles = decoder[segment]
                    children = set[frozenset[str]]()
                    for possible in possibles:
                        if not base:
                            children = set(map(frozenset[str], possibles))
                            break
                        else:
                            children |= {frozenset({*b, possible}) for b in base}
                    base = children
                potential_solution = [a for a in base if a in DISPLAY_TO_NUMBER]
                if len(potential_solution) == 1:
                    for segment in current:
                        decoder[segment] = list(
                            set(decoder[segment]) & set(potential_solution[0])
                        )

            # pprint(decoder)

            for v in decoder.values():
                if len(v) == 1:
                    # solved for k, remove v from everyone else
                    for vv in decoder.values():
                        if v is vv or v[0] not in vv:
                            continue
                        vv.remove(v[0])
            # pprint(decoder)

            # Turns out at this point we're fully solved, no need to play with 6
            # for current in patterns_by_length[6]:
            #     base = set[frozenset[str]]()
            #     for i, segment in enumerate(current):
            #         possibles = decoder[segment]
            #         children = set[frozenset[str]]()
            #         for possible in possibles:
            #             if not base:
            #                 children = set(map(frozenset[str], possibles))
            #                 break
            #             else:
            #                 children |= {frozenset({*b, possible}) for b in base}
            #         base = children
            #     potential_solution = [a for a in base if a in DISPLAY_TO_NUMBER]
            #     if len(potential_solution) == 1:
            #         for segment in current:
            #             decoder[segment] = list(
            #                 set(decoder[segment]) & set(potential_solution[0])
            #             )

            # for k, v in decoder.items():
            #     if len(v) == 1:
            #         # solved for k, remove v from everyone else
            #         for vv in decoder.values():
            #             if v is vv or v[0] not in vv:
            #                 continue
            #             vv.remove(v[0])
            n = ""
            for output in outputs.split():
                match len(output):
                    case 2:
                        n += "1"
                    case 3:
                        n += "7"
                    case 4:
                        n += "4"
                    case 7:
                        n += "8"
                    case 5 | 6:
                        display = set[str]()
                        for segment in output:
                            decoded = decoder[segment]
                            if len(decoded) != 1:
                                print("now we have a problem")
                                raise Exception("break everything")
                            display.add(decoded[0])
                        n += str(DISPLAY_TO_NUMBER[frozenset(display)])
            print(n)
            final += int(n)
    return final


if __name__ == "__main__":
    print(part_1())
    print(part_2())
