import pygame

import calculate
import sound
from const import SQUARE_SIZE, BOARD_ROWS, BOARD_COLS, ENVIRONMENT, MENU_HEIGHT, SCREEN_HEIGHT
from move import Move


class Drag:
    def __init__(self):
        self.is_dragging = False
        self.possible_positions = []
        self.initial_square = None
        self.hovering_square = None
        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self.pos = (0, 0)

    def reset(self):
        self.is_dragging = False
        self.possible_positions = []
        self.initial_square = None
        self.pos = (0, 0)

    def draw(self, surface):
        if self.is_dragging:
            surface.blit(self.initial_square.piece.img, self.initial_square.piece.img.get_rect(center=self.pos))

    def focus(self, board, target_square, event):
        if ENVIRONMENT == 'development':
            for position in calculate.threat_map(board, 'w' if board.active_color == 'b' else 'b'):
                board.squares[position[0]][position[1]].is_threat = True

        self.pos = event.pos
        self.is_dragging = True
        self.possible_positions = calculate.possible_positions(board, target_square)
        self.initial_square = target_square
        self.hovering_square = target_square

        target_square.highlight()

        for (row, col) in self.possible_positions:
            board.squares[row][col].is_accented = True

    def blur(self, board):
        if ENVIRONMENT == 'development':
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    board.squares[row][col].is_threat = False

        if self.initial_square is not None:
            self.initial_square.is_highlighted = False

        for (row, col) in self.possible_positions:
            board.squares[row][col].is_accented = False

        self.reset()

    def move(self, board, target_square):
        piece = self.initial_square.piece
        piece.is_visible = True
        is_target_square_empty = target_square.is_empty()
        is_en_passant = False
        is_castling = False

        row = self.initial_square.row
        col = self.initial_square.col

        if piece.name == 'p' and abs(self.initial_square.row - target_square.row) == 2:
            board.en_passant_target_square = board.squares[row + piece.direction][col]
        else:
            board.en_passant_target_square = None

        if len(board.moves) > 0:
            previous_move = board.moves[-1]
            previous_move_row_delta = abs(previous_move.initial_square.row - previous_move.target_square.row)
            previous_move_distance = (previous_move.target_square.row - row, previous_move.target_square.col - col)

            if \
                    previous_move_row_delta == 2 and \
                    abs(previous_move_distance[0]) == 0 and \
                    abs(previous_move_distance[1]) == 1 and \
                    previous_move.target_square.piece.name == 'p' and \
                    piece.name == 'p':
                if target_square.row == row + piece.direction and target_square.col == col + previous_move_distance[1]:
                    is_en_passant = True
                    en_passant_square = previous_move.target_square
                    en_passant_piece = en_passant_square.piece

                    board.captures.get(piece.color).get(en_passant_piece.name).append(en_passant_piece)

                    en_passant_piece.is_captured = True
                    en_passant_piece.is_visible = False
                    en_passant_square.piece = None

        if len(piece.moves) < 2 and not board.evaluation.get('is_check'):
            invalid_positions = calculate.threat_map(board, 'w' if board.active_color == 'b' else 'b')

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
                        possibility in board.castling and \
                        target_square.row == row and \
                        target_square.col == 1:
                    board.move(Move(
                        board.squares[row][0],
                        board.squares[row][2]
                    ))
                    board.castling.remove(possibility)
                    is_castling = True

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
                        possibility in board.castling and \
                        target_square.row == row and \
                        target_square.col == 6:
                    board.move(Move(
                        board.squares[row][7],
                        board.squares[row][5]
                    ))
                    board.castling.remove(possibility)
                    is_castling = True

        if len(board.moves) > 0:
            board.moves[-1].target_square.is_highlighted = False

        board.move(Move(
            self.initial_square,
            target_square
        ))

        target_square.is_highlighted = True
        board.active_color = 'b' if board.active_color == 'w' else 'w'

        if \
            (
                (target_square.row == 0 and piece.color == 'w') or
                (target_square.row == 7 and piece.color == 'b')
            ) and \
                piece.name == 'p':
            board.promotion_square = target_square
        else:
            evaluation = board.evaluate()
            board.evaluation = evaluation

            if ENVIRONMENT == 'development':
                print(evaluation)

            if evaluation.get('result') is not None:
                sound.play('game-end')
            elif evaluation.get('is_check'):
                sound.play('move-check')
            elif is_castling:
                sound.play('castle')
            else:
                sound.play(
                    ('move-self' if board.active_color == 'w' else 'move-opponent')
                    if (is_target_square_empty and not is_en_passant) else 'capture'
                )

    def handle(self, board, event):
        if board.evaluation.get('result') is None and board.promotion_square is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > MENU_HEIGHT and SCREEN_HEIGHT - event.pos[1] > MENU_HEIGHT:
                    target_position = ((event.pos[1] - MENU_HEIGHT) // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
                    target_square = board.squares[target_position[0]][target_position[1]]

                    if not target_square.is_empty():
                        if target_square.piece.color == board.active_color:
                            target_square.piece.is_visible = False

                            if self.initial_square is not None:
                                previous_square = self.initial_square

                                self.blur(board)

                                if previous_square != target_square:
                                    self.focus(board, target_square, event)
                                    self.initial_square = target_square
                                else:
                                    target_square.piece.is_visible = True
                            else:
                                self.focus(board, target_square, event)
                    elif self.initial_square is not None:
                        if target_position in self.possible_positions:
                            self.move(board, target_square)

                        self.blur(board)

            if \
                    event.type == pygame.MOUSEMOTION and \
                    event.pos[1] > MENU_HEIGHT and \
                    SCREEN_HEIGHT - event.pos[1] > MENU_HEIGHT:

                self.pos = event.pos
                target_position = ((event.pos[1] - MENU_HEIGHT) // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
                target_square = board.squares[target_position[0]][target_position[1]]

                if target_square.is_empty() and self.cursor == pygame.SYSTEM_CURSOR_HAND and not self.is_dragging:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.cursor = pygame.SYSTEM_CURSOR_ARROW
                elif not target_square.is_empty() and self.cursor == pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self.cursor = pygame.SYSTEM_CURSOR_HAND

                if self.is_dragging:
                    if self.hovering_square is not None:
                        self.hovering_square.has_border = False

                    target_square.has_border = True

                    self.hovering_square = target_square

            if event.type == pygame.MOUSEBUTTONUP:
                if self.hovering_square is not None:
                    self.hovering_square.has_border = False

                self.pos = (0, 0)
                self.is_dragging = False
                self.hovering_square = None

                if self.initial_square is not None:
                    if not self.initial_square.is_empty():
                        self.initial_square.piece.is_visible = True

                if event.pos[1] > MENU_HEIGHT and SCREEN_HEIGHT - event.pos[1] > MENU_HEIGHT:
                    target_position = ((event.pos[1] - MENU_HEIGHT) // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
                    target_square = board.squares[target_position[0]][target_position[1]]

                    if target_square != self.initial_square and target_position in self.possible_positions:
                        self.move(board, target_square)
                        self.blur(board)
