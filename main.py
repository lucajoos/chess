import pygame
import sys

from const import HEIGHT, WIDTH
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        pygame.display.set_caption('Chess')
        while True:
            self.loop()


    def loop(self):
        self.game.draw_bg(self.screen)
        self.game.draw_pieces(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main = Main()
