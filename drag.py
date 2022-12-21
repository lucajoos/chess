import pygame

from const import SQUARE_SIZE


class Drag:
    def __init__(self):
        self.is_dragging = False
        self.piece = None
        self.pos = (0, 0)

    def draw(self, screen):
        if self.is_dragging:
            screen.blit(self.piece.img, self.piece.img.get_rect(center=self.pos))

    def handle(self, board, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            piece = board.squares[event.pos[1] // SQUARE_SIZE][event.pos[0] // SQUARE_SIZE].piece

            if piece is not None:
                self.pos = event.pos

                self.piece = piece
                self.piece.is_visible = False

                self.is_dragging = True
        if event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
            self.piece.is_visible = True
