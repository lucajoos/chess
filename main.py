import os

import pygame
import sys

from const import BOARD_HEIGHT, BOARD_WIDTH, SQUARE_SIZE, MENU_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
from drag import Drag
from game import Game
from menu import Menu


class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game = Game()
        self.drag = Drag()
        self.menu = Menu()
        self.font_bold = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Bold.ttf'), 16)
        self.font_regular = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Regular.ttf'), 16)

        pygame.display.set_caption('Chess')
        while True:
            self.loop()

    def loop(self):
        for event in pygame.event.get():
            self.drag.handle(self.game.board, event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.menu.draw(self.screen)
        self.game.draw_squares(self.screen)
        self.game.draw_board_labels(self.screen, self.font_bold)
        self.game.draw_square_accents(self.screen)
        self.game.draw_square_borders(self.screen)
        self.game.draw_pieces(self.screen)
        self.drag.draw(self.screen)

        if self.game.board.active_color is not None:
            # TODO: draw result
            pass

        pygame.display.update()


main = Main()
