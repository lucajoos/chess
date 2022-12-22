from const import ROWS, COLS
from square import Square


class Calculate:
    @staticmethod
    def straight_positions(board, square):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if row < 7:
            for i in range(row + 1, 8):
                target_piece = board.squares[i][col].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((i, col))

                if not is_empty:
                    break
        if row > 0:
            for i in range(row - 1, -1, -1):
                target_piece = board.squares[i][col].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((i, col))

                if not is_empty:
                    break
        if col < 7:
            for i in range(col + 1, 8):
                target_piece = board.squares[row][i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row, i))

                if not is_empty:
                    break
        if col > 0:
            for i in range(col - 1, -1, -1):
                target_piece = board.squares[row][i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row, i))

                if not is_empty:
                    break
        return possible_positions

    @staticmethod
    def diagonal_positions(board, square):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if row < 7 and col < 7:
            for i in range(1, 8 - max(row, col)):
                target_piece = board.squares[row + i][col + i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row + i, col + i))

                if not is_empty:
                    break
        if row > 0 and col > 0:
            for i in range(1, max(row, col) + 1):
                target_piece = board.squares[row - i][col - i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row - i, col - i))

                if not is_empty:
                    break
        if row > 0 and col < 7:
            for i in range(1, min(row + 1, 8 - col)):
                target_piece = board.squares[row - i][col + i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row - i, col + i))

                if not is_empty:
                    break
        if row < 7 and col > 0:
            for i in range(1, min(8 - row, col + 1)):
                target_piece = board.squares[row + i][col - i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or target_piece.name == 'k':
                        break

                possible_positions.append((row + i, col - i))

                if not is_empty:
                    break

        return possible_positions

    @staticmethod
    def possible_positions(board, square):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if piece is not None:
            if piece.name == 'p':
                possible_positions.append((row + piece.direction, col))

                if col > 1:
                    if not board.squares[row + piece.direction][col - 1].is_empty():
                        possible_positions.append((row + piece.direction, col - 1))

                if col < 7:
                    if not board.squares[row + piece.direction][col + 1].is_empty():
                        possible_positions.append((row + piece.direction, col + 1))

                if not piece.was_moved:
                    possible_positions.append((row + piece.direction * 2, col))
                print(possible_positions)

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
                possible_positions = Calculate.diagonal_positions(board, square)

            elif piece.name == 'r':
                possible_positions = Calculate.straight_positions(board, square)

            elif piece.name == 'q':
                possible_positions = \
                    Calculate.diagonal_positions(board, square) + \
                    Calculate.straight_positions(board, square)

            elif piece.name == 'k':
                possible_positions = [
                    (row + 1, col + 1),
                    (row + 1, col),
                    (row + 1, col - 1),
                    (row, col + 1),
                    (row, col - 1),
                    (row - 1, col + 1),
                    (row - 1, col),
                    (row - 1, col - 1),
                ]

                invalid_positions = []

                # calculate invalid positions

                for possible_position in list(possible_positions):
                    if possible_position in invalid_positions:
                        possible_positions.remove(possible_position)

            for position in list(possible_positions):
                if not Square.in_range(position[0], position[1]):
                    possible_positions.remove(position)
                else:
                    target_square = board.squares[position[0]][position[1]]
                    target_piece = target_square.piece

                    if target_square == square:
                        possible_positions.remove(position)
                    else:
                        if not target_square.is_empty():
                            if target_piece.color == square.piece.color or \
                                    (target_piece.name == 'k') or \
                                    (piece.name == 'p' and target_square.col == square.col):
                                possible_positions.remove(position)
        return possible_positions
