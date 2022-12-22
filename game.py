import pygame.draw

from board import Board
from const import ROWS, COLS, TILE_SIZE, COLORS


class Game:
    def __init__(self):
        self.board = Board()

    def draw_tiles(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(
                    surface,
                    self.board.squares[row][col].color,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

                if len(self.board.moves) > 1:
                    previous_move = self.board.moves[-2]
                    previous_move.initial_square.reset()
                    previous_move.target_square.reset()

                if len(self.board.moves) > 0:
                    last_move = self.board.moves[-1]
                    last_move.initial_square.highlight()
                    last_move.target_square.highlight()

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.squares[row][col].piece

                if piece is not None and piece.is_visible:
                    surface.blit(
                        piece.img,
                        piece.img.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                    )
