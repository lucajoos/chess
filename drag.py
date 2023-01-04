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

        if len(board.moves) > 0:
            board.moves[-1].target_square.is_highlighted = False

        board.move(Move(
            self.initial_square,
            target_square
        ))

        evaluation = board.evaluate()

        if ENVIRONMENT == 'development':
            print(evaluation)

        target_square.is_highlighted = True
        board.active_color = 'b' if board.active_color == 'w' else 'w'

        if evaluation.get('result') is not None:
            sound.play('game-end')
        elif evaluation.get('is_check'):
            sound.play('move-check')
        else:
            sound.play(
                ('move-self' if board.active_color == 'w' else 'move-opponent')
                if target_square.is_empty() else 'capture')


    def handle(self, board, event):
        if board.evaluation.get('result') is None:
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

            if event.type == pygame.MOUSEMOTION and self.is_dragging:
                if event.pos[1] > MENU_HEIGHT and SCREEN_HEIGHT - event.pos[1] > MENU_HEIGHT:
                    self.pos = event.pos

                    if self.hovering_square is not None:
                        self.hovering_square.has_border = False

                    target_position = ((event.pos[1] - MENU_HEIGHT) // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
                    target_square = board.squares[target_position[0]][target_position[1]]
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
