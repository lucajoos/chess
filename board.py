import calculate
import sound
from const import BOARD_ROWS, BOARD_COLS, DEFAULT_FEN
from move import Move
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.squares = [[Square(row, col, None) for col in range(BOARD_COLS)] for row in range(BOARD_ROWS)]
        self.moves = []
        self.pieces = []
        self.active_color = 'w'
        self.en_passant_target_square = None
        self.promotion_square = None

        self.evaluation = {
            'is_check': False,
            'is_stalemate': False,
            'is_checkmate': False,
            'result': None
        }

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

        self.castling = ['K', 'Q', 'k', 'q']

    def reset(self):
        self.squares = [[Square(row, col, None) for col in range(BOARD_COLS)] for row in range(BOARD_ROWS)]
        self.moves = []
        self.pieces = []
        self.active_color = 'w'
        self.en_passant_target_square = None
        self.promotion_square = None

        self.evaluation = {
            'is_check': False,
            'is_stalemate': False,
            'is_checkmate': False,
            'result': None
        }

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

        self.castling = ['K', 'Q', 'k', 'q']

    def evaluate(self):
        is_check = calculate.is_check(self, self.active_color)
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
            'is_checkmate': is_checkmate,
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

            self.moves.append(move)
            piece.moves.append(move)

    def load(self, fen):
        piece_count = {
            'b': {
                'p': 8,
                'n': 2,
                'b': 2,
                'r': 2,
                'q': 1,
                'k': 1
            },
            'w': {
                'p': 8,
                'n': 2,
                'b': 2,
                'r': 2,
                'q': 1,
                'k': 1
            }
        }

        for group_index, group in enumerate(fen.split(' ')):
            if group_index == 0:
                for row_index, row in enumerate(group.split('/')):
                    col_index = 0

                    for position in list(row):
                        if position.isnumeric():
                            col_index += int(position)
                        else:
                            square = self.squares[row_index][col_index]
                            color = 'w' if position.isupper() else 'b'
                            name = position.lower()
                            piece = Piece(square, name, color)
                            piece_count[color][name] -= 1
                            self.pieces.append(piece)
                            square.piece = piece
                            col_index += 1
            elif group_index == 1:
                self.active_color = group
            elif group_index == 2:
                self.castling = '-' if group == '-' else list(group)
            elif group_index == 3:
                self.en_passant_target_square = None if group == '-' else Square.get_square_from_algebraic_notation(self, group)

                if self.en_passant_target_square is not None:
                    en_passant_row = self.en_passant_target_square.row
                    en_passant_col = self.en_passant_target_square.col
                    opposite_color = 'w' if self.active_color == 'b' else 'b'
                    opposite_direction = -1 if opposite_color == 'w' else 1

                    previous_target_square = self.squares[en_passant_row + opposite_direction][en_passant_col]
                    previous_initial_square = self.squares[en_passant_row - opposite_direction][en_passant_col]

                    if not previous_target_square.is_empty():
                        if previous_target_square.piece.name == 'p' and previous_target_square.piece.color == opposite_color:
                            previous_move = Move(
                                previous_initial_square,
                                previous_target_square
                            )

                            previous_target_square.piece.moves.append(previous_move)
                            self.moves.append(previous_move)
        for color in piece_count:
            opposite_color = 'w' if color == 'b' else 'b'
            for piece_name in piece_count[color]:
                piece = Piece(self.squares[0][0], piece_name, color)
                piece.is_visible = True
                piece.is_captured = True

                for _ in range(0, piece_count[color][piece_name]):
                    self.captures[opposite_color][piece_name].append(piece)

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

        row_string += f' {self.active_color} '
        row_string += ' '.join(self.castling) if len(self.castling) > 0 else '-'

        row_string += f' {"-" if self.en_passant_target_square is None else Square.square_to_algebraic_notation(self.en_passant_target_square)}'
        row_string += ' 0 1'
        return row_string
