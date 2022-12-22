import pygame
import sys

from const import HEIGHT, WIDTH, TILE_SIZE
from drag import Drag
from game import Game


class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
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

        self.game.draw_tiles(self.screen)
        self.game.draw_pieces(self.screen)
        self.drag.draw(self.screen)

        pygame.display.update()


main = Main()
