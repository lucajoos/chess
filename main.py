import os

import pygame
import sys
import ctypes

from const import ICON, SCREEN_WIDTH, SCREEN_HEIGHT, ENVIRONMENT
from drag import Drag
from game import Game
from menu import Menu
from overlay import Overlay
from promotion import Promotion


class Main:
    def __init__(self):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('lucajoos.chess.1.0.0')
        pygame.display.set_caption(f'Chess{" [" + ENVIRONMENT + "]" if ENVIRONMENT != "production" else ""}')
        pygame.display.set_icon(pygame.image.load(os.path.join(ICON)))

        pygame.init()

        self.font_bold_medium = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Bold.ttf'), 16)
        self.font_bold_small = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Bold.ttf'), 14)
        self.font_regular_small = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Regular.ttf'), 14)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game = Game()
        self.drag = Drag()
        self.menu = Menu(self.font_bold_small)
        self.promotion = Promotion()
        self.overlay = Overlay()

        while True:
            self.loop()

    def loop(self):
        events = pygame.event.get()
        for event in events:
            self.drag.handle(self.game.board, event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.menu.draw(self.screen, events, self.font_regular_small, self.game.board)
        self.game.draw_squares(self.screen)
        self.game.draw_board_labels(self.screen, self.font_bold_medium)
        self.game.draw_square_accents(self.screen)
        self.game.draw_square_borders(self.screen)
        self.game.draw_pieces(self.screen)
        self.promotion.draw(self.screen, events, self.game.board)
        self.drag.draw(self.screen)
        self.overlay.draw(self.screen, events, self.game.board)

        pygame.display.update()


main = Main()
