from const import COLORS, SQUARE_SIZE, MENU_HEIGHT


class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.is_dark = (self.row + self.col) % 2 == 1
        self.is_accented = False
        self.is_highlighted = False
        self.is_threat = False
        self.has_border = False
        self.center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + MENU_HEIGHT)
        self.bottom_right_corner = (col * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE + MENU_HEIGHT)
        self.top_left_corner = (col * SQUARE_SIZE, row * SQUARE_SIZE + MENU_HEIGHT)
        self.color = self.get_color('DEFAULT')

    def get_color(self, name):
        return COLORS.get(
            f'SQUARE_{"DARK" if self.is_dark else "LIGHT"}{"_HIGHLIGHT" if self.is_highlighted else ""}_{name}'
        )

    def get_inverted_color(self, name):
        return COLORS.get(
            f'SQUARE_{"LIGHT" if self.is_dark else "DARK"}{"_HIGHLIGHT" if self.is_highlighted else ""}_{name}'
        )

    def highlight(self):
        self.is_highlighted = True

    def is_empty(self):
        return self.piece is None

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def square_to_algebraic_notation(board, square):
        return f'{chr(104 - square.col if board.is_inverted else square.col + 97)}{str(square.row + 1 if board.is_inverted else 8 - square.row)}'

    @staticmethod
    def get_square_from_algebraic_notation(board, string):
        split = list(string)
        col = 104 + ord(split[0]) if board.is_inverted else ord(split[0]) - 97
        row = int(split[1]) + 1 if board.is_inverted else 8 - int(split[1])

        return board.squares[row][col]