import pygame
import sys

from const import BOARD_HEIGHT, BOARD_WIDTH, SQUARE_SIZE, MENU_HEIGHT
from drag import Drag
from game import Game


class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT + MENU_HEIGHT))
        self.game = Game()
        self.drag = Drag()

        pygame.display.set_caption('Chess')
        while True:
            self.loop()

    def loop(self):
        for event in pygame.event.get():
            self.drag.handle(self.game.board, event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.game.draw_squares(self.screen)
        self.game.draw_pieces(self.screen)
        self.game.draw_square_accents(self.screen)
        self.drag.draw(self.screen)

        if self.game.board.active_color is not None:
            # TODO: draw result
            pass

        pygame.display.update()


main = Main()
