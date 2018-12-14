import datetime
import re
from collections import Counter, defaultdict
from typing import NamedTuple
from pprint import pprint


class Entry(NamedTuple):
    date_time: datetime.datetime
    data: str


entries = []
entry_regex = re.compile(r'\[([:\d\s-]+)\] (.*)')
with open('input4.txt') as f:
    for line in f.readlines():
        date_time, info = entry_regex.match(line).groups()
        parsed_datetime = datetime.datetime.strptime(
            date_time, '%Y-%m-%d %H:%M'
        )
        entries.append(Entry(parsed_datetime, info))

entries = sorted(entries, key=lambda e: e.date_time)
pprint(entries)

guard_regex = re.compile(r'Guard #(\d+).*')
guards = defaultdict(list)
for entry in entries:
    guard_match = guard_regex.match(entry.data)
    if guard_match:
        night_timeline = []
        guard_id = guard_match.group(1)
        guards[guard_id].append(night_timeline)
        continue
    night_timeline.append(entry.date_time.minute)


def most_sleep(guard):
    guard_id, nights = guard
    total_sleep = 0
    for night in nights:
        for index in range(0, len(night), 2):
            sleeps_at = night[index]
            wakes_up = night[index + 1]
            slept_for = wakes_up - sleeps_at
            total_sleep += slept_for
    return total_sleep


choosen_guard = max(
    guards.items(),
    key=most_sleep
)

pprint(choosen_guard)

choosen_guard_nights = choosen_guard[1]

minutes_sleeping = []

for night in choosen_guard_nights:
    for index in range(0, len(night), 2):
        sleeps_at = night[index]
        wakes_up = night[index + 1]
        sleeping = list(range(sleeps_at, wakes_up))
        print(f'slept during {sleeping}')
        minutes_sleeping.extend(sleeping)


counter = Counter(minutes_sleeping)
choosen_minute = counter.most_common(1)[0][0]
print(choosen_minute)
print(f'Value = {int(choosen_guard[0])*choosen_minute}')

all_counters = []
for guard_id, nights in guards.items():
    minutes_sleeping = []
    print('for guard', guard_id)
    for night in nights:
        for index in range(0, len(night), 2):
            sleeps_at = night[index]
            wakes_up = night[index + 1]
            sleeping = list(range(sleeps_at, wakes_up))
            print(f'slept during {sleeping}')
            minutes_sleeping.extend(sleeping)

    counter = Counter(minutes_sleeping)
    if counter.most_common(1):
        all_counters.append((counter.most_common(1)[0], guard_id))
print(all_counters)

x = max(all_counters, key=lambda x: x[0][1])

print(x[0][0] * int(x[1]))


