from const import COLORS


class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.is_dark = (self.row + self.col) % 2 == 0

        self.color = None
        self.reset()

    def reset(self):
        self.color = COLORS.get('TILE_DARK_DEFAULT' if self.is_dark else 'TILE_LIGHT_DEFAULT')

    def highlight(self):
        self.color = COLORS.get(
            'TILE_DARK_HIGHLIGHT' if self.is_dark else 'TILE_LIGHT_HIGHLIGHT'
        )

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
