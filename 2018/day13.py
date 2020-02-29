from collections import Counter
from copy import deepcopy
from functools import total_ordering


MAP = []
with open("input13.txt") as f:
    MAP = [list(x.strip("\n")) for x in f]

# print(MAP)


TURNS = r"\/"
CARTS = "^>v<"
STRAIGHT = "-|"
INTERSECTIONS = r"+"

LEFT = 0
STRAIGHT = 1
RIGHT = 2

carts = []


@total_ordering
class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn = 0
        self.crashed = False

    def left(self):
        next_index = CARTS.index(self.direction) - 1
        self.direction = CARTS[next_index]

    def right(self):
        next_index = CARTS.index(self.direction) + 1
        next_index = next_index % 4
        self.direction = CARTS[next_index]

    def tick(self):
        current_position = MAP[self.y][self.x]

        if current_position in INTERSECTIONS:
            if self.turn == LEFT:
                self.left()
                self.turn = STRAIGHT
            elif self.turn == STRAIGHT:
                self.turn = RIGHT
            elif self.turn == RIGHT:
                self.right()
                self.turn = LEFT
        elif current_position == "\\":
            if self.direction in "><":
                self.right()
            elif self.direction in "^v":
                self.left()
        elif current_position == "/":
            if self.direction in "><":
                self.left()
            elif self.direction in "^v":
                self.right()

        if self.direction == "^":
            self.y -= 1
        elif self.direction == ">":
            self.x += 1
        elif self.direction == "v":
            self.y += 1
        else:
            self.x -= 1

    def position(self):
        return self.x, self.y

    def __lt__(self, other):
        return self.position() < other.position()

    def __repr__(self):
        return f"Cart {self.direction} at {self.x}x{self.y}"


for Y in range(len(MAP)):
    for X in range(len(MAP[Y])):
        if MAP[Y][X] in CARTS:
            cart = Cart(X, Y, MAP[Y][X])
            if cart.direction in "^v":
                MAP[Y][X] = "|"
            else:
                MAP[Y][X] = "-"
            carts.append(cart)


while True:
    carts = sorted(carts)

    for c in carts:
        if c.crashed:
            continue
        current_positions = {
            (cart.x, cart.y): cart for cart in carts if not cart.crashed
        }
        c.tick()
        if c.position() in current_positions:
            print(f"CRASHED!!!!!!!!! AT {c.x},{c.y}")
            c.crashed = current_positions[c.position()].crashed = True
            print(f"Removing {c} and {current_positions[c.position()]}")
    not_crashed = [c for c in carts if not c.crashed]
    if len(not_crashed) <= 1:
        print(f"LAST POSITION: {not_crashed[0].position()}")
        break
