class Grid:
    def __init__(self):
        self.up = False
        self.left = False
        self.down = False
        self.right = False
        self.food = False

    def __str__(self) -> str:
        return str.format("{0}, {1}, {2}, {3}", self.up, self.left, self.down, self.right)
