import re
from collections import defaultdict
from pprint import pprint
from string import ascii_uppercase

regex = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin\.")

instructions = []
with open("input7.txt") as f:
    for line in f:
        matches = regex.match(line).groups()
        instructions.append(matches)


requirements = defaultdict(list)
for step in instructions:
    requirements[step[1]].append(step[0])


steps = list(ascii_uppercase)
ordering = []

while steps:
    for i, step in enumerate(steps):
        requirements[step] = [req for req in requirements[step] if req not in ordering]
        if not requirements[step]:
            ordering.append(step)
            steps.pop(i)
            break

pprint("".join(ordering))


print("--- DAY 07: part 2 ---")

steps = list(ascii_uppercase)
BASE_SECONDS = 60
TOTAL_WORKES = 5
time_to_complete = {step: BASE_SECONDS + i + 1 for i, step in enumerate(steps)}
complete = []

workers = set()

requirements = defaultdict(list)
for step in instructions:
    requirements[step[1]].append(step[0])


def process_requirements(step):
    return [r for r in requirements[step] if r in steps]


total_seconds = 0
while steps:
    complete = {worker for worker in workers if worker[1] == total_seconds}
    complete_steps = {worker[0] for worker in complete}
    steps = [s for s in steps if s not in complete_steps]
    workers -= complete

    being_worked = {worker[0] for worker in workers}
    available_steps = [
        step
        for step in steps
        if step not in being_worked and not process_requirements(step)
    ]

    if available_steps:
        print(available_steps)

    # workers grab tasks
    while len(workers) < TOTAL_WORKES:
        if not available_steps:
            break
        available_step = available_steps.pop(0)
        workers.add((available_step, total_seconds + time_to_complete[available_step]))
    if steps:
        total_seconds += 1


print(total_seconds)
