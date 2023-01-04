from board import Board
from move import Move
from square import Square


def straight_positions(board, square, is_calculating_threat_map=False):
    piece = square.piece
    row = square.row
    col = square.col

    positions = []

    if row < 7:
        for i in range(row + 1, 8):
            target_piece = board.squares[i][col].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((i, col))

            if not is_empty:
                break
    if row > 0:
        for i in range(row - 1, -1, -1):
            target_piece = board.squares[i][col].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((i, col))

            if not is_empty:
                break
    if col < 7:
        for i in range(col + 1, 8):
            target_piece = board.squares[row][i].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((row, i))

            if not is_empty:
                break
    if col > 0:
        for i in range(col - 1, -1, -1):
            target_piece = board.squares[row][i].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((row, i))

            if not is_empty:
                break
    return positions


def diagonal_positions(board, square, is_calculating_threat_map=False):
    piece = square.piece
    row = square.row
    col = square.col

    positions = []

    if row < 7 and col < 7:
        for i in range(1, 8 - max(row, col)):
            target_piece = board.squares[row + i][col + i].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((row + i, col + i))

            if not is_empty:
                break
    if row > 0 and col > 0:
        for i in range(1, max(row, col) + 1):
            target_piece = board.squares[row - i][col - i].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((row - i, col - i))

            if not is_empty:
                break
    if row > 0 and col < 7:
        for i in range(1, min(row + 1, 8 - col)):
            target_piece = board.squares[row - i][col + i].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((row - i, col + i))

            if not is_empty:
                break
    if row < 7 and col > 0:
        for i in range(1, min(8 - row, col + 1)):
            target_piece = board.squares[row + i][col - i].piece
            is_empty = target_piece is None

            if not is_empty:
                if target_piece.color == piece.color or (target_piece.name == 'k' and not is_calculating_threat_map):
                    break

            positions.append((row + i, col - i))

            if not is_empty:
                break

    return positions


def threat_map(board, color):
    positions = []

    for piece in board.pieces:
        if piece.color == color:
            positions += possible_positions(board, piece.moves[-1].target_square, True)

    return set(positions)


def possible_positions(board, square, is_calculating_threat_map=False):
    piece = square.piece
    row = square.row
    col = square.col

    positions = []

    if piece is not None:
        if piece.name == 'p':
            if not is_calculating_threat_map:
                positions.append((row + piece.direction, col))

            if col > 1 and 8 > row + piece.direction > 0:
                if not board.squares[row + piece.direction][col - 1].is_empty() or is_calculating_threat_map:
                    positions.append((row + piece.direction, col - 1))

            if col < 7 and 8 > row + piece.direction > 0:
                if not board.squares[row + piece.direction][col + 1].is_empty() or is_calculating_threat_map:
                    positions.append((row + piece.direction, col + 1))

            if len(board.moves) > 0:
                previous_move = board.moves[-1]
                previous_move_row_delta = abs(previous_move.initial_square.row - previous_move.target_square.row)
                previous_move_distance = (previous_move.target_square.row - row, previous_move.target_square.col - col)

                if \
                        previous_move_row_delta == 2 and \
                                abs(previous_move_distance[0]) == 0 and \
                                abs(previous_move_distance[1]) == 1 and \
                                previous_move.target_square.piece.name == 'p':
                    positions.append((row + piece.direction, col + previous_move_distance[1]))

            if (row == 1 and piece.color == 'b') or (row == 6 and piece.color == 'w'):
                positions.append((row + piece.direction * 2, col))

        elif piece.name == 'n':
            positions = [
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
            positions = diagonal_positions(board, square, is_calculating_threat_map)

        elif piece.name == 'r':
            positions = straight_positions(board, square, is_calculating_threat_map)

        elif piece.name == 'q':
            positions = \
                diagonal_positions(board, square, is_calculating_threat_map) + \
                straight_positions(board, square, is_calculating_threat_map)

        elif piece.name == 'k':
            positions = [
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
                invalid_positions = threat_map(board, 'w' if board.active_color == 'b' else 'b')

                for possible_position in list(positions):
                    if possible_position in invalid_positions:
                        positions.remove(possible_position)

                if len(piece.moves) < 2 and not board.evaluation.get('is_check'):
                    is_allowed = True

                    possibility = 'q' if col == 4 else 'k'

                    if piece.color == 'w':
                        possibility = possibility.upper()

                    for current_col in range(1, col):
                        if \
                                not board.squares[row][current_col].is_empty() or \
                                (row, current_col) in invalid_positions:
                            is_allowed = False

                    if not board.squares[row][0].is_empty():
                        potential_rook = board.squares[row][0].piece
                        if \
                                is_allowed and \
                                potential_rook.name == 'r' and \
                                len(potential_rook.moves) < 2 and \
                                possibility in board.castling:
                            positions.append((row, 1))

                    is_allowed = True

                    possibility = 'q' if possibility.lower() == 'k' else 'k'

                    if piece.color == 'w':
                        possibility = possibility.upper()

                    for current_col in range(col + 1, 7):
                        if \
                                not board.squares[row][current_col].is_empty() or \
                                (row, current_col) in invalid_positions:
                            is_allowed = False
                    if not board.squares[row][0].is_empty():
                        potential_rook = board.squares[row][0].piece

                        if \
                                is_allowed and \
                                potential_rook.name == 'r' and \
                                len(potential_rook.moves) < 2 and \
                                possibility in board.castling:
                            positions.append((row, 6))

        for position in list(positions):
            if not Square.in_range(position[0], position[1]):
                positions.remove(position)
            else:
                target_square = board.squares[position[0]][position[1]]
                target_piece = target_square.piece

                if target_square == square:
                    positions.remove(position)
                else:
                    if not target_square.is_empty():
                        if target_piece.color == square.piece.color or \
                                (target_piece.name == 'k' and not is_calculating_threat_map) or \
                                (piece.name == 'p' and target_square.col == square.col):
                            positions.remove(position)

        if not is_calculating_threat_map and piece.name == 'k':
            for possible_position in list(positions):
                hypothetical_board = Board()
                hypothetical_board.load(board.save())

                hypothetical_board.move(Move(
                    hypothetical_board.squares[row][col],
                    hypothetical_board.squares[possible_position[0]][possible_position[1]]
                ))

                if is_check(hypothetical_board, hypothetical_board.active_color):
                    positions.remove(possible_position)

    if not is_calculating_threat_map:
        if is_check(board, board.active_color):
            for possible_position in list(positions):
                hypothetical_board = Board()
                hypothetical_board.load(board.save())

                hypothetical_board.move(Move(
                    hypothetical_board.squares[square.row][square.col],
                    hypothetical_board.squares[possible_position[0]][possible_position[1]]
                ))

                if is_check(hypothetical_board, hypothetical_board.active_color):
                    positions.remove(possible_position)

    return positions


def is_check(board, color):
    threats = threat_map(board, 'w' if color == 'b' else 'b')

    for piece in board.pieces:
        if piece.name == 'k' and piece.color == color:
            king_target_square = piece.moves[-1].target_square

            if (king_target_square.row, king_target_square.col) in threats:
                return True

    return False


def is_stalemate(board, color):
    positions = []

    for piece in board.pieces:
        if piece.color == color:
            positions += possible_positions(board, piece.moves[-1].target_square)

    return len(set(positions)) == 0
