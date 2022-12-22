import pygame

from const import SQUARE_SIZE
from move import Move


class Drag:
    def __init__(self):
        self.is_dragging = False
        self.possible_positions = []
        self.initial_square = None
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
        self.pos = event.pos
        self.is_dragging = True
        self.possible_positions = board.calculate_possible_moves(target_square)
        self.initial_square = target_square

        target_square.color_highlight()

        for (row, col) in self.possible_positions:
            board.squares[row][col].is_accented = True

    def blur(self, board):
        if self.initial_square is not None:
            self.initial_square.color_reset()

        for (row, col) in self.possible_positions:
            board.squares[row][col].is_accented = False

        self.reset()

    def move(self, board, target_square):
        piece = self.initial_square.piece
        piece.is_visible = True

        move = Move(
            self.initial_square,
            target_square
        )

        self.initial_square.piece = None
        target_square.piece = piece

        piece.move(move)
        board.moves.append(move)

        board.active = 'b' if board.active == 'w' else 'w'

    def handle(self, board, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            target_position = (event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
            target_square = board.squares[target_position[0]][target_position[1]]

            if not target_square.is_empty():
                if target_square.piece.color == board.active:
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
            self.pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            target_position = (event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE)
            target_square = board.squares[target_position[0]][target_position[1]]

            self.pos = (0, 0)
            self.is_dragging = False

            if self.initial_square is not None:
                if not self.initial_square.is_empty():
                    self.initial_square.piece.is_visible = True

            if target_square != self.initial_square and target_position in self.possible_positions:
                self.move(board, target_square)
                self.blur(board)
