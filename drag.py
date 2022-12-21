import pygame

from const import SQUARE_SIZE


class Drag:
    def __init__(self):
        self.is_dragging = False
        self.possible_moves = []
        self.initial_square = None
        self.pos = (0, 0)

    def draw(self, screen):
        if self.is_dragging:
            screen.blit(self.initial_square.piece.img, self.initial_square.piece.img.get_rect(center=self.pos))

    def handle(self, board, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            square = board.squares[event.pos[1] // SQUARE_SIZE][event.pos[0] // SQUARE_SIZE]

            if square.piece is not None:
                self.possible_moves = board.calculate_possible_moves(square)
                self.pos = event.pos

                self.initial_square = square
                self.initial_square.piece.is_visible = False

                self.is_dragging = True

                for (row, col) in self.possible_moves:
                    board.squares[row][col].color = '#C84646'
        if event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and self.is_dragging:
            self.is_dragging = False
            self.initial_square.piece.is_visible = True

            for (row, col) in self.possible_moves:
                board.squares[row][col].reset_color()

            target_square = board.squares[event.pos[1] // SQUARE_SIZE][event.pos[0] // SQUARE_SIZE]
            target_row = target_square.row
            target_col = target_square.col

            if target_square is not self.initial_square:
                if (target_row, target_col) in self.possible_moves:
                    piece = self.initial_square.piece
                    piece.move((target_row, target_col))

                    target_square.piece = piece
                    self.initial_square.piece = None
