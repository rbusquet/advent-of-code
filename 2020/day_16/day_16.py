from collections import defaultdict
import re
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import List, Tuple, Dict

def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


@dataclass
class Rule:
    start: str
    end: str

    def within_range(self, value: int) -> bool:
        return self.start <= value <= self.end

@dataclass
class Field:
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


assert next(file) == 'your ticket:'
my_ticket = [*map(int, next(file).split(","))]

next(file)
assert next(file) == 'nearby tickets:'

error_rate = 0
valid_tickets = []
for ticket in file:
    ticket = [*map(int, ticket.split(","))]
    ticket_error_rate = 0
    for value in ticket:
        is_value_valid = False
        for r in fields:
            if r.within_range(value):
                is_value_valid = True
                break
        if not is_value_valid:
            ticket_error_rate += value
    if ticket_error_rate == 0:
        valid_tickets.append(ticket)
    error_rate += ticket_error_rate


print(error_rate)


checked_fields = set()
checked_indexes = set()
fields_to_index = {}

while len(fields_to_index) < len(my_ticket):
    indexes_by_field = defaultdict(list)
    for index in range(len(my_ticket)):
        if index in checked_indexes:
            continue
        for field in fields:
            if field.field in checked_fields:
                continue
            if all(field.within_range(ticket[index]) for ticket in valid_tickets):
                indexes_by_field[field.field].append(index)

    for field, indexes in indexes_by_field.items():
        if len(indexes) == 1:
            checked_fields.add(field)
            checked_indexes.add(indexes[0])
            fields_to_index[field] = indexes[0]
    print(indexes_by_field)


departure = []
for field, index in fields_to_index.items():
    if 'departure' in field:
        departure.append(my_ticket[index])
print(departure)

print(reduce(mul, departure))
