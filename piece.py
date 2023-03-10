import os.path

import pygame

from const import PIECE_VALUES
from move import Move


class Piece:
    def __init__(self, initial_square, name, color):
        self.name = name
        self.color = color
        self.direction = -1 if color == 'w' else 1
        self.value = PIECE_VALUES.get(name)
        self.moves = [Move(None, initial_square)]
        self.is_captured = False
        self.img = None
        self.is_visible = True

        self.set_texture()

    def set_texture(self):
        self.img = pygame.transform.smoothscale(pygame.image.load(os.path.join(f'assets/images/pieces/{self.color}_{self.name}.png')), (75, 75))

    def replace_initial_square(self, square):
        self.moves = [Move(None, square)]