from const import ROWS, COLS, INITIAL_FEN
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.squares = None
        self.moves = None
        self.active = 'w'
        self.pieces = []
        self.reset()

    def reset(self):
        self.squares = [[Square(row, col, None) for col in range(COLS)] for row in range(ROWS)]
        self.moves = []
        self.load(INITIAL_FEN)

    def load(self, string):
        for group_index, group in enumerate(string.split(' ')):
            if group_index == 0:
                for row_index, row in enumerate(group.split('/')):
                    col_index = 0

                    for position in list(row):
                        if position.isnumeric():
                            col_index += int(position)
                        else:
                            square = self.squares[row_index][col_index]
                            piece = Piece(square, position.lower(), 'w' if position.isupper() else 'b')
                            self.pieces.append(piece)
                            square.piece = piece
                            col_index += 1
            elif group_index == 1:
                self.active = group
