import os.path

import pygame

from const import PIECE_VALUES


class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.value = (1 if color == 'w' else -1) * PIECE_VALUES.get(name)
        self.moves = []
        self.was_moved = False
        self.dir = -1 if color == 'w' else 1
        self.img = None
        self.is_visible = True

        self.set_texture()

    def set_texture(self, size=80):
        self.img = pygame.image.load(os.path.join(f'assets/images/{size}px/{self.color}_{self.name}.png'))

    def move(self, move):
        self.moves.append(move)

        if not self.was_moved:
            self.was_moved = True
