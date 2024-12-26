from enum import Enum


class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f'(x: {self.x}, y: {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False


class Direction(Enum):
    UP = ('^', Position(0, -1))
    RIGHT = ('>', Position(1, 0))
    DOWN = ('v', Position(0, 1))
    LEFT = ('<', Position(-1, 0))

    @classmethod
    def from_symbol(cls, symbol):
        for direction in cls:
            if direction.value[0] == symbol:
                return direction
        raise ValueError(f"Invalid direction symbol: {symbol}")

    def move(self):
        return self.value[1]  # Returns the Position

    def get_symbol(self):
        return self.value[0]

    @classmethod
    def get_all_symbols(cls):
        return [direction.value[0] for direction in cls]
