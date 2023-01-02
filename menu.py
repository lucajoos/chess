import pygame.draw

from const import COLORS, BOARD_WIDTH, MENU_HEIGHT, BOARD_HEIGHT, PIECES


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
    def draw(self, surface, board):
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, 0, BOARD_WIDTH, MENU_HEIGHT))
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, BOARD_HEIGHT + MENU_HEIGHT, BOARD_WIDTH, MENU_HEIGHT))
        surface.blit(self.avatars[0], self.avatars[0].get_rect(center=(20 * 2, MENU_HEIGHT // 2)))
        surface.blit(self.avatars[1], self.avatars[1].get_rect(center=(20 * 2, BOARD_HEIGHT + MENU_HEIGHT + MENU_HEIGHT // 2)))
        surface.blit(self.title[0], self.title[0].get_rect(topleft=(70, ((MENU_HEIGHT - 45) // 2 + 3))))
        surface.blit(self.title[1], self.title[1].get_rect(topleft=(70, BOARD_HEIGHT + MENU_HEIGHT + ((MENU_HEIGHT - 45) // 2 + 3))))

        group_count = 0
        piece_count = 0

        for piece_category in PIECES:
            pieces = board.captures.get('b').get(piece_category)
            for (index, piece) in enumerate(pieces):
                img = pygame.transform.smoothscale(piece.img, (25, 25))
                surface.blit(img, img.get_rect(topleft=(65 + (index + piece_count) * 7 + group_count * 13, (MENU_HEIGHT // 2 - 3))))

            piece_count += len(pieces)

            if len(pieces) > 0:
                group_count += 1

        group_count = 0
        piece_count = 0

        for piece_category in PIECES:
            pieces = board.captures.get('w').get(piece_category)
            for (index, piece) in enumerate(pieces):
                img = pygame.transform.smoothscale(piece.img, (25, 25))
                surface.blit(img, img.get_rect(
                    topleft=(65 + (index + piece_count) * 7 + group_count * 13, MENU_HEIGHT + BOARD_HEIGHT + (MENU_HEIGHT // 2 - 3))))

            piece_count += len(pieces)

            if len(pieces) > 0:
                group_count += 1
