from collections import defaultdict
import re
from functools import reduce
from operator import mul
from typing import List, Tuple, NamedTuple


def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


class Rule(NamedTuple):
    start: str
    end: str

    def within_range(self, value: int) -> bool:
        return self.start <= value <= self.end


class Field(NamedTuple):
    rules: Tuple[Rule]
    field: str

    def within_range(self, value: int) -> bool:
        return any(r.within_range(value) for r in self.rules)


file = read_file()

rules_exp = re.compile(r"(\d+)-(\d+) or (\d+)-(\d+)")

fields: List[Field] = []
for line in file:
    if not line:
        break
    field, rules = line.split(":")
    s1, e1, s2, e2 = rules_exp.match(rules.strip()).groups()
    rules = (
        Rule(int(s1), int(e1)),
        Rule(int(s2), int(e2)),
    )
    fields.append(Field(rules, field))


assert next(file) == "your ticket:"
my_ticket = [*map(int, next(file).split(","))]

next(file)
assert next(file) == "nearby tickets:"

error_rate = 0
valid_tickets = []
for ticket in file:
    ticket = [*map(int, ticket.split(","))]
    ticket_error_rate = 0
    # before, I would check if the rate is 0, it's a valid ticket
    # but there are tickets where the only error was a field with value 0,
    # making the error rate 0 :facepalm:
    is_valid_ticket = True
    for value in ticket:
        is_value_valid = False
        for r in fields:
            if r.within_range(value):
                is_value_valid = True
                break
        if not is_value_valid:
            is_valid_ticket = False
            ticket_error_rate += value
    if is_valid_ticket:
        valid_tickets.append(ticket)
    error_rate += ticket_error_rate


print(error_rate)

indexed_fields = {}

while len(indexed_fields) < len(my_ticket):
    indexes_by_field = defaultdict(list)
    for index in range(len(my_ticket)):
        if index in indexed_fields:
            continue
        for field in fields:
            if all(field.within_range(ticket[index]) for ticket in valid_tickets):
                indexes_by_field[field.field].append(index)

    for field, indexes in indexes_by_field.items():
        if len(indexes) == 1:
            indexed_fields[indexes[0]] = field
            break


departure = []
for index, field in indexed_fields.items():
    if "departure" in field:
        departure.append(my_ticket[index])

print(reduce(mul, departure))
