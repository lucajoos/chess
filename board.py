import calculate
import sound
from const import BOARD_ROWS, BOARD_COLS, DEFAULT_FEN
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.squares = None
        self.moves = None
        self.pieces = []

        self.captures = {
            'b': {
                'p': [],
                'n': [],
                'b': [],
                'r': [],
                'q': [],
                'k': []
            },
            'w': {
                'p': [],
                'n': [],
                'b': [],
                'r': [],
                'q': [],
                'k': []
            }
        }

        self.active_color = 'w'
        self.is_inverted = False
        self.evaluation = None
        self.reset()

    def reset(self):
        self.evaluation = None
        self.squares = [[Square(row, col, None) for col in range(BOARD_COLS)] for row in range(BOARD_ROWS)]
        self.moves = []

        self.captures = {
            'b': {
                'p': [],
                'n': [],
                'b': [],
                'r': [],
                'q': [],
                'k': []
            },
            'w': {
                'p': [],
                'n': [],
                'b': [],
                'r': [],
                'q': [],
                'k': []
            }
        }

    def evaluate(self):
        is_check = calculate.is_check(self, 'w' if self.active_color == 'b' else 'b')
        is_stalemate = calculate.is_stalemate(self, self.active_color)
        is_checkmate = is_check and is_stalemate
        result = None

        if is_checkmate:
            result = self.active_color

        elif is_stalemate:
            result = 'n'

        return {
            'is_check': is_check,
            'is_stalemate': is_stalemate,
            'is_checkmate': is_check and is_stalemate,
            'result': result
        }

    def move(self, move):
        if not move.initial_square.is_empty():
            piece = move.initial_square.piece

            if not move.target_square.is_empty():
                target_piece = move.target_square.piece
                self.captures.get(piece.color).get(target_piece.name).append(target_piece)

                move.target_square.piece.is_captured = True
                move.target_square.piece.is_visible = False

            move.initial_square.piece = None
            move.target_square.piece = piece

            if \
                    (move.target_square.row == 0 and piece.color == 'w') or \
                    (move.target_square.row == 7 and piece.color == 'b'):
                # TODO: promotion
                pass

            self.moves.append(move)
            piece.moves.append(move)

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

        for row_index, row in enumerate(range(BOARD_ROWS)):
            col_string = ''
            empty_squares = 0

            for col_index, col in enumerate(range(BOARD_COLS)):
                square = self.squares[row][col]

                if square.is_empty():
                    empty_squares += 1

                    if col_index == BOARD_COLS - 1:
                        col_string += str(empty_squares)
                else:
                    if empty_squares > 0:
                        col_string += str(empty_squares)
                        empty_squares = 0
                    col_string += square.piece.name if square.piece.color == 'b' else square.piece.name.upper()

            row_string += col_string

            if row_index < BOARD_ROWS - 1:
                row_string += '/'

        row_string += f' {self.active_color}'

        # TODO: EXPORT COMPLETE FEN
        row_string += ' KQkq - 0 1'
        return row_string
