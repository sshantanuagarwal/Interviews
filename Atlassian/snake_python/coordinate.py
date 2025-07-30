class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return isinstance(other, Coordinate) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})" 