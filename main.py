import pygame
import sys

from const import HEIGHT, WIDTH, SQUARE_SIZE
from game import Game


class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

        self.is_dragging = False
        self.dragging_piece = None
        self.dragging_pos = (0, 0)
        self.dragging_square = None

        pygame.display.set_caption('Chess')
        while True:
            self.loop()


    def loop(self):
        self.game.draw_bg(self.screen)
        self.game.draw_pieces(self.screen)

        if self.is_dragging:
            self.screen.blit(self.dragging_piece.img, self.dragging_piece.img.get_rect(center=self.dragging_pos))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                piece = self.game.board.squares[event.pos[1] // SQUARE_SIZE][event.pos[0] // SQUARE_SIZE].piece

                if piece is not None:
                    piece.is_visible = False
                    self.dragging_pos = event.pos
                    self.dragging_piece = piece
                    self.is_dragging = True
            if event.type == pygame.MOUSEMOTION and self.is_dragging:
                self.dragging_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_dragging = False
                self.dragging_piece.is_visible = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main = Main()
