import pygame.draw

from const import COLORS, BOARD_WIDTH, MENU_HEIGHT, BOARD_HEIGHT


class Menu:
    def draw(self, surface):
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, 0, BOARD_WIDTH, MENU_HEIGHT))
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, BOARD_HEIGHT + MENU_HEIGHT, BOARD_WIDTH, MENU_HEIGHT))
