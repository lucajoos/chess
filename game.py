import pygame.draw

from board import Board
from const import ROWS, COLS, SQUARE_SIZE, COLORS, DEFAULT_FEN
from square import Square


class Game:
    def __init__(self):
        self.board = Board()
        self.board.load(DEFAULT_FEN)

    def draw_squares(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]

                pygame.draw.rect(
                    surface,
                    square.get_color('THREAT' if square.is_threat else 'DEFAULT'),
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

                if square.has_border:
                    pygame.draw.rect(
                        surface,
                        square.get_color('BORDER'),
                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        5
                    )

                if len(self.board.moves) > 1:
                    previous_move = self.board.moves[-2]
                    previous_move.initial_square.is_highlighted = False
                    previous_move.initial_square.is_highlighted = False

                if len(self.board.moves) > 0:
                    last_move = self.board.moves[-1]
                    last_move.initial_square.is_highlighted = True
                    last_move.initial_square.is_highlighted = True

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                piece = square.piece

                if piece is not None and piece.is_visible:
                    surface.blit(
                        piece.img,
                        piece.img.get_rect(center=square.center)
                    )

    def draw_square_accents(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]

                if square.is_accented:
                    if square.is_empty():
                        pygame.draw.circle(surface, square.get_color('ACCENT'), square.center, 20)
                    else:
                        pygame.draw.circle(surface, square.get_color('ACCENT'), square.center, SQUARE_SIZE // 2, 10)
