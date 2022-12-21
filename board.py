from const import ROWS, COLS
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.squares = [[Square(row, col, None) for col in range(COLS)] for row in range(ROWS)]
        self.load('pppppppp/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def load(self, string):
        for group_index, group in enumerate(string.split(' ')):
            if group_index == 0:
                for row_index, row in enumerate(group.split('/')):
                    col_index = 0

                    for position in list(row):
                        if position.isnumeric():
                            col_index += int(position)
                        else:
                            self.squares[row_index][col_index].piece = Piece(position.lower(),
                                                                             'w' if position.isupper() else 'b')
                            col_index += 1

    def calculate_possible_moves(self, square):
        piece = square.piece
        row = square.row
        col = square.col

        possible_moves = []

        if piece is not None:
            if piece.name == 'p':
                possible_moves.append((row + piece.direction, col))

                if not piece.was_moved:
                    possible_moves.append((row + piece.direction * 2, col))

            if piece.name == 'n':
                possible_moves = [
                    (row + 1, col + 2),
                    (row + 2, col + 1),
                    (row - 1, col + 2),
                    (row - 2, col + 1),
                    (row + 1, col - 2),
                    (row + 2, col - 1),
                    (row - 1, col - 2),
                    (row - 2, col - 1),
                ]

            for index, move in enumerate(list(possible_moves)):
                row, col = move
                if not Square.in_range(row, col):
                    possible_moves.remove(move)
                else:
                    target_square = self.squares[row][col]

                    if target_square.piece is not None:
                        if target_square.piece.color == square.piece.color:
                            possible_moves.remove(move)

        return possible_moves
