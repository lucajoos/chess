from const import ROWS, COLS
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.squares = [[Square(row, col) for row in range(ROWS)] for col in range(COLS)]
        self.load('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def load(self, string):
        for group_index, group in enumerate(string.split(' ')):
            if group_index == 0:
                for row_index, row in enumerate(group.split('/')):
                    col_index = 0

                    for position in list(row):
                        if position.isnumeric():
                            col_index += int(position)
                        else:
                            self.squares[row_index][col_index].piece = Piece(position.lower(), 'w' if position.isupper() else 'b')
                            col_index += 1


