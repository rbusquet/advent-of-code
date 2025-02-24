import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import TextIO, TypedDict, cast

regex = re.compile(
    r"Valve (?P<valve>[A-Z]{2}) has flow rate=(?P<rate>[0-9]+); "
    r"tunnel[s]{0,1} lead[s]{0,1} to valve[s]{0,1} (?P<leads>.*)"
)


class Node(TypedDict):
    valve: str
    rate: str
    leads: str
    open: bool


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    nodes = dict[str, Node]()
    first: Node | None = None
    for line in args.infile:
        if not (match := regex.match(line)):
            print(line)
            continue
        node = cast(Node, match.groupdict())
        nodes[node["valve"]] = node
        if not first:
            first = node

    def open(cur: Node, rate={}, timer=0, *open_valves):
        next_valves = cur["leads"].split(", ")

        rate = defaultdict(int, rate)
        if timer >= 30:
            return [rate]
        # options: open this one
        open_valves_set = set(open_valves)
        is_open = cur["valve"] in open_valves_set
        rates = []
        if not is_open and (cur_rate := int(cur["rate"])) > 0:
            timer = timer + 1
            rate[timer] += cur_rate
            open_valves_set.add(cur["valve"])
            rates.extend(open(cur, rate, timer, *open_valves_set))
        else:
            for valve in next_valves:
                valve_node = nodes[valve]
                rates.extend(open(valve_node, rate, timer + 1, *open_valves))
        return rates

    if first is None:
        exit()
    result = open(first)
    print(result)
