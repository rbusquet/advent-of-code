from dataclasses import dataclass, field

with open("input13.txt") as f:
    MAP = [list(x.strip("\n")) for x in f]

# print(MAP)


TURNS = r"\/"
CARTS = "^>v<"
INTERSECTIONS = r"+"

LEFT = 0
STRAIGHT = 1
RIGHT = 2

carts = []


@dataclass(order=True)
class Cart:
    x: int
    y: int
    direction: str = field(compare=False)
    turn: int = field(compare=False, default=0)
    crashed: bool = False

    def left(self) -> None:
        next_index = CARTS.index(self.direction) - 1
        self.direction = CARTS[next_index]

    def right(self) -> None:
        next_index = CARTS.index(self.direction) + 1
        next_index = next_index % 4
        self.direction = CARTS[next_index]

    def tick(self) -> None:
        current_position = MAP[self.y][self.x]

        if current_position in INTERSECTIONS:
            self.intersection()
        elif current_position == "\\":
            self.backslash()
        elif current_position == "/":
            self.slash()

        if self.direction == "^":
            self.y -= 1
        elif self.direction == ">":
            self.x += 1
        elif self.direction == "v":
            self.y += 1
        else:
            self.x -= 1

    def slash(self) -> None:
        if self.direction in "><":
            self.left()
        elif self.direction in "^v":
            self.right()

    def backslash(self) -> None:
        if self.direction in "><":
            self.right()
        elif self.direction in "^v":
            self.left()

    def intersection(self) -> None:
        if self.turn == LEFT:
            self.left()
            self.turn = STRAIGHT
        elif self.turn == STRAIGHT:
            self.turn = RIGHT
        elif self.turn == RIGHT:
            self.right()
            self.turn = LEFT

    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def __repr__(self) -> str:
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
