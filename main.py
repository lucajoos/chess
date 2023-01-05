# Chess von Luca Raúl Joos

import os

import pygame
import sys
import ctypes

from const import ICON, SCREEN_WIDTH, SCREEN_HEIGHT, ENVIRONMENT, ID, ICON_SMALL
from drag import Drag
from draw import Draw
from menu import Menu
from overlay import Overlay
from promotion import Promotion


class Main:
    def __init__(self):
        if hasattr(ctypes, 'windll'):
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(ID)
            pygame.display.set_icon(pygame.image.load(os.path.join(ICON_SMALL)))
        else:
            pygame.display.set_icon(pygame.image.load(os.path.join(ICON)))

        pygame.display.set_caption(f'Chess{" [" + ENVIRONMENT + "]" if ENVIRONMENT != "production" else ""}')

        pygame.init()

        self.font_bold_medium = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Bold.ttf'), 16)
        self.font_bold_small = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Bold.ttf'), 14)
        self.font_regular_small = pygame.font.Font(os.path.join('assets', 'fonts', 'Montserrat-Regular.ttf'), 14)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.draw = Draw()
        self.drag = Drag()
        self.menu = Menu(self.font_bold_small)
        self.promotion = Promotion()
        self.overlay = Overlay()

        while True:
            self.loop()

    def loop(self):
        events = pygame.event.get()
        for event in events:
            self.drag.handle(self.draw.board, event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.menu.draw(self.screen, events, self.font_regular_small, self.draw.board)
        self.draw.squares(self.screen)
        self.draw.board_labels(self.screen, self.font_bold_medium)
        self.draw.square_accents(self.screen)
        self.draw.square_borders(self.screen)
        self.draw.pieces(self.screen)
        self.promotion.draw(self.screen, events, self.draw.board)
        self.drag.draw(self.screen)
        self.overlay.draw(self.screen, events, self.draw.board)

        pygame.display.update()


main = Main()
