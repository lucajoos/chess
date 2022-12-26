from const import ROWS, COLS, DEFAULT_FEN
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.squares = None
        self.moves = None
        self.active_color = 'w'
        self.pieces = []
        self.reset()

    def reset(self):
        self.squares = [[Square(row, col, None) for col in range(COLS)] for row in range(ROWS)]
        self.moves = []

    def move(self, move):
        if not move.initial_square.is_empty():
            piece = move.initial_square.piece

            if not move.target_square.is_empty():
                move.target_square.piece.is_captured = True
                move.target_square.piece.is_visible = False

            move.initial_square.piece = None
            move.target_square.piece = piece

            self.moves.append(move)
            piece.moves.append(move)

            if not piece.was_moved:
                piece.was_moved = True

    def load(self, fen):
        for group_index, group in enumerate(fen.split(' ')):
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
                self.active_color = group
        # TODO: IMPORT COMPLETE FEN

    def save(self):
        row_string = ''

        for row_index, row in enumerate(range(ROWS)):
            col_string = ''
            empty_squares = 0

            for col_index, col in enumerate(range(COLS)):
                square = self.squares[row][col]

                if square.is_empty():
                    empty_squares += 1

                    if col_index == COLS - 1:
                        col_string += str(empty_squares)
                else:
                    if empty_squares > 0:
                        col_string += str(empty_squares)
                        empty_squares = 0
                    col_string += square.piece.name if square.piece.color == 'b' else square.piece.name.upper()

            row_string += col_string

            if row_index < ROWS - 1:
                row_string += '/'

        row_string += f' {self.active_color}'

        # TODO: EXPORT COMPLETE FEN
        row_string += ' KQkq - 0 1'
        return row_string

