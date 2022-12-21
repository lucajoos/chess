import pygame.draw

from board import Board
from const import ROWS, COLS, SQUARE_SIZE

class Game:
    def __init__(self):
        self.board = Board()

    def draw_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(surface, self.board.squares[row][col].color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.squares[row][col].piece

                if piece is not None and piece.is_visible:
                    surface.blit(piece.img, piece.img.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)))
