
from collections import defaultdict


PLAYERS = 470
MARBLES = 72170 * 100


class Marble:
    def __init__(self, id: int):
        self.id = id
        self.previous: 'Marble' = self
        self.next: 'Marble' = self

    def replace(self, marble_id: int) -> 'Marble':
        other = Marble(marble_id)
        other.previous = self.previous
        other.next = self
        self.previous.next = other
        self.previous = other
        return other

    def get_next(self, n: int) -> 'Marble':
        ret = self
        for i in range(n):
            ret = ret.next
        return ret

    def get_before(self, n: int) -> 'Marble':
        ret = self
        for i in range(n):
            ret = ret.previous
        return ret

    def remove(self):
        self.previous.next = self.next
        self.next.previous = self.previous
        return self.next


current_marble = Marble(0)
scores = defaultdict(int)

for _round in range(1, MARBLES + 1):
    print(_round)
    if _round % 23 == 0:
        current_player_id = _round % PLAYERS
        scores[current_player_id] += _round
        to_remove = current_marble.get_before(7)
        scores[current_player_id] += to_remove.id
        current_marble = to_remove.remove()
    else:
        to_replace = current_marble.get_next(2)
        current_marble = to_replace.replace(_round)

print(max(scores.values()))
