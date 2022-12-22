from const import ROWS, COLS, INITIAL_FEN
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.squares = None
        self.moves = None
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
                            self.squares[row_index][col_index].piece = Piece(position.lower(),
                                                                             'w' if position.isupper() else 'b')
                            col_index += 1

    def calculate_straight_positions(self, square):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if row < 7:
            for i in range(row + 1, 8):
                target_piece = self.squares[i][col].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((i, col))

                if not is_empty:
                    break
        if row > 0:
            for i in range(row - 1, -1, -1):
                target_piece = self.squares[i][col].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((i, col))

                if not is_empty:
                    break
        if col < 7:
            for i in range(col + 1, 8):
                target_piece = self.squares[row][i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row, i))

                if not is_empty:
                    break
        if col > 0:
            for i in range(col - 1, -1, -1):
                target_piece = self.squares[row][i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row, i))

                if not is_empty:
                    break
        return possible_positions

    def calculate_diagonal_positions(self, square):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if row < 7 and col < 7:
            for i in range(1, 8 - max(row, col)):
                target_piece = self.squares[row + i][col + i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row + i, col + i))
                
                if not is_empty:
                    break
        if row > 0 and col > 0:
            for i in range(1, max(row, col) + 1):
                target_piece = self.squares[row - i][col - i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row - i, col - i))

                if not is_empty:
                    break
        if row > 0 and col < 7:
            for i in range(1, min(row + 1, 8 - col)):
                target_piece = self.squares[row - i][col + i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row - i, col + i))

                if not is_empty:
                    break
        if row < 7 and col > 0:
            for i in range(1, min(8 - row, col + 1)):
                target_piece = self.squares[row + i][col - i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row + i, col - i))

                if not is_empty:
                    break

        return possible_positions

    def calculate_possible_moves(self, square):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []
        possible_moves = []

        if piece is not None:
            if piece.name == 'p':
                possible_positions.append((row + piece.direction, col))

                if not piece.was_moved:
                    possible_positions.append((row + piece.direction * 2, col))

            elif piece.name == 'n':
                possible_positions = [
                    (row + 1, col + 2),
                    (row + 2, col + 1),
                    (row - 1, col + 2),
                    (row - 2, col + 1),
                    (row + 1, col - 2),
                    (row + 2, col - 1),
                    (row - 1, col - 2),
                    (row - 2, col - 1),
                ]

            elif piece.name == 'b':
                possible_positions = self.calculate_diagonal_positions(square)

            elif piece.name == 'r':
                possible_positions = self.calculate_straight_positions(square)

            elif piece.name == 'q':
                possible_positions = self.calculate_diagonal_positions(square) + self.calculate_straight_positions(square)

            for index, position in enumerate(list(possible_positions)):
                if not Square.in_range(position[0], position[1]):
                    possible_positions.remove(position)
                else:
                    target_square = self.squares[position[0]][position[1]]
                    target_piece = target_square.piece

                    if target_square == square:
                        possible_positions.remove(position)
                    else:
                        if target_piece is not None:
                            if target_piece.color == square.piece.color or target_piece.name == 'k':
                                possible_positions.remove(position)

        return possible_positions
