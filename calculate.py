import copy

from board import Board
from const import ROWS, COLS
from move import Move
from square import Square


class Calculate:
    @staticmethod
    def straight_positions(board, square, is_calculating_threat_map=False):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if row < 7:
            for i in range(row + 1, 8):
                target_piece = board.squares[i][col].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((i, col))

                if not is_empty:
                    break
        if row > 0:
            for i in range(row - 1, -1, -1):
                target_piece = board.squares[i][col].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((i, col))

                if not is_empty:
                    break
        if col < 7:
            for i in range(col + 1, 8):
                target_piece = board.squares[row][i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((row, i))

                if not is_empty:
                    break
        if col > 0:
            for i in range(col - 1, -1, -1):
                target_piece = board.squares[row][i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((row, i))

                if not is_empty:
                    break
        return possible_positions

    @staticmethod
    def diagonal_positions(board, square, is_calculating_threat_map=False):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if row < 7 and col < 7:
            for i in range(1, 8 - max(row, col)):
                target_piece = board.squares[row + i][col + i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((row + i, col + i))

                if not is_empty:
                    break
        if row > 0 and col > 0:
            for i in range(1, max(row, col) + 1):
                target_piece = board.squares[row - i][col - i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((row - i, col - i))

                if not is_empty:
                    break
        if row > 0 and col < 7:
            for i in range(1, min(row + 1, 8 - col)):
                target_piece = board.squares[row - i][col + i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((row - i, col + i))

                if not is_empty:
                    break
        if row < 7 and col > 0:
            for i in range(1, min(8 - row, col + 1)):
                target_piece = board.squares[row + i][col - i].piece
                is_empty = target_piece is None

                if not is_empty:
                    if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                        break

                possible_positions.append((row + i, col - i))

                if not is_empty:
                    break

        return possible_positions

    @staticmethod
    def threat_map(board, color):
        possible_positions = []

        for piece in board.pieces:
            if piece.color == color:
                possible_positions += Calculate.possible_positions(board, piece.moves[-1].target_square, True)

        return set(possible_positions)

    @staticmethod
    def possible_positions(board, square, is_calculating_threat_map=False):
        piece = square.piece
        row = square.row
        col = square.col

        possible_positions = []

        if piece is not None:
            if piece.name == 'p':
                if not is_calculating_threat_map:
                    possible_positions.append((row + piece.direction, col))

                if col > 1:
                    if not board.squares[row + piece.direction][col - 1].is_empty() or is_calculating_threat_map:
                        possible_positions.append((row + piece.direction, col - 1))

                if col < 7:
                    if not board.squares[row + piece.direction][col + 1].is_empty() or is_calculating_threat_map:
                        possible_positions.append((row + piece.direction, col + 1))

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
                possible_positions = Calculate.diagonal_positions(board, square, is_calculating_threat_map)

            elif piece.name == 'r':
                possible_positions = Calculate.straight_positions(board, square, is_calculating_threat_map)

            elif piece.name == 'q':
                possible_positions = \
                    Calculate.diagonal_positions(board, square, is_calculating_threat_map) + \
                    Calculate.straight_positions(board, square, is_calculating_threat_map)

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

                if not is_calculating_threat_map:
                    invalid_positions = Calculate.threat_map(board, 'w' if board.active_color == 'b' else 'b')

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
                                    (target_piece.name == 'k' and not is_calculating_threat_map) or \
                                    (piece.name == 'p' and target_square.col == square.col):
                                possible_positions.remove(position)

            if not is_calculating_threat_map and piece.name == 'k':
                for possible_position in list(possible_positions):
                    hypothetical_board = Board()
                    hypothetical_board.load(board.save())

                    hypothetical_board.move(Move(
                        hypothetical_board.squares[row][col],
                        hypothetical_board.squares[possible_position[0]][possible_position[1]]
                    ))

                    if possible_position in Calculate.threat_map(hypothetical_board, board.active_color):
                        possible_positions.remove(possible_position)

        if not is_calculating_threat_map:
            if Calculate.is_check(board, board.active_color):
                for possible_position in list(possible_positions):
                    hypothetical_board = Board()
                    hypothetical_board.load(board.save())

                    hypothetical_board.move(Move(
                        hypothetical_board.squares[square.row][square.col],
                        hypothetical_board.squares[possible_position[0]][possible_position[1]]
                    ))

                    if Calculate.is_check(hypothetical_board, hypothetical_board.active_color):
                        possible_positions.remove(possible_position)

        return possible_positions

    @staticmethod
    def is_check(board, color):
        threat_map = Calculate.threat_map(board, 'w' if color == 'b' else 'b')

        for piece in board.pieces:
            if piece.name == 'k' and piece.color == color:
                king_target_square = piece.moves[-1].target_square

                if (king_target_square.row, king_target_square.col) in threat_map:
                    return True

        return False
