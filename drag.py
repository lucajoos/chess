import pygame

import calculate
from const import SQUARE_SIZE, BOARD_ROWS, BOARD_COLS, ENVIRONMENT, MENU_HEIGHT
from move import Move


class Drag:
    def __init__(self):
        self.is_dragging = False
        self.possible_positions = []
        self.initial_square = None
        self.hovering_square = None
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

        board.move(Move(
            self.initial_square,
            target_square
        ))

        board.active_color = 'b' if board.active_color == 'w' else 'w'
        board.validate()

    def handle(self, board, event):
        if board.result is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > MENU_HEIGHT:
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

            if event.type == pygame.MOUSEMOTION and self.is_dragging:
                if event.pos[1] > MENU_HEIGHT:
                    self.pos = event.pos

                    if self.hovering_square is not None:
                        self.hovering_square.has_border = False

                    target_position = ((event.pos[1] - MENU_HEIGHT) // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
                    target_square = board.squares[target_position[0]][target_position[1]]
                    target_square.has_border = True

                    self.hovering_square = target_square

            if event.type == pygame.MOUSEBUTTONUP:
                target_position = ((event.pos[1] - MENU_HEIGHT) // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
                target_square = board.squares[target_position[0]][target_position[1]]

                if self.hovering_square is not None:
                    self.hovering_square.has_border = False

                self.pos = (0, 0)
                self.is_dragging = False
                self.hovering_square = None

                if self.initial_square is not None:
                    if not self.initial_square.is_empty():
                        self.initial_square.piece.is_visible = True

                if target_square != self.initial_square and target_position in self.possible_positions and event.pos[1] > MENU_HEIGHT:
                    self.move(board, target_square)
                    self.blur(board)
