from const import COLORS, SQUARE_SIZE


class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.is_dark = (self.row + self.col) % 2 == 0
        self.is_accented = False
        self.is_highlighted = False
        self.center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)

        self.color = None
        self.color_reset()

    def get_color(self, name):
        return COLORS.get(
            f'SQUARE_DARK_{name}' if self.is_dark else f'SQUARE_LIGHT_{name}'
        )

    def color_reset(self):
        self.is_accented = False
        self.is_highlighted = False
        self.color = self.get_color('DEFAULT')

    def highlight(self):
        self.is_highlighted = True
        self.color = self.get_color('HIGHLIGHT')

    def is_empty(self):
        return self.piece is None

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
