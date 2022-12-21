class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

        self.color = None
        self.reset_color()

    def reset_color(self):
        self.color = (234, 235, 200) if (self.row + self.col) % 2 == 0 else (119, 154, 88)
