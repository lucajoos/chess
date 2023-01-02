import pygame.draw

from const import COLORS, BOARD_WIDTH, MENU_HEIGHT, BOARD_HEIGHT


class Menu:
    def __init__(self, font):
        self.avatars = (
            pygame.transform.scale(pygame.image.load('assets/images/black_400.png'), (45, 45)),
            pygame.transform.scale(pygame.image.load('assets/images/white_400.png'), (45, 45)),
        )

        self.title = (
            font.render('Black', True, '#FFFFFF'),
            font.render('White', True, '#FFFFFF'),
        )
    def draw(self, surface):
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, 0, BOARD_WIDTH, MENU_HEIGHT))
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, BOARD_HEIGHT + MENU_HEIGHT, BOARD_WIDTH, MENU_HEIGHT))
        surface.blit(self.avatars[0], self.avatars[0].get_rect(center=(20 * 2, MENU_HEIGHT // 2)))
        surface.blit(self.avatars[1], self.avatars[1].get_rect(center=(20 * 2, BOARD_HEIGHT + MENU_HEIGHT + MENU_HEIGHT // 2)))
        surface.blit(self.title[0], self.title[0].get_rect(topleft=(70, 15)))
        surface.blit(self.title[1], self.title[1].get_rect(topleft=(70, BOARD_HEIGHT + MENU_HEIGHT + 15)))
