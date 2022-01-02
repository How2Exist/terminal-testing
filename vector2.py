class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2(x, y)

    def __mult__(self, other):
        if isinstance(other, Vector2):
            x = self.x * other.x
            y = self.y * other.y
        else:
            x = self.x * other
            y = self.y * other

        return Vector2(x, y)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            x = self.x / other.x
            y = self.y / other.y
        else:
            x = self.x / other
            y = self.y / other

        return Vector2(x, y)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))