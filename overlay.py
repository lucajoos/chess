import math

import pygame

from const import MENU_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, COLORS, DEFAULT_FEN


class Overlay:
    def __init__(self):
        self.icon = pygame.image.load('assets/images/icons/refresh_big.svg')
        self.pos = (0, 0)
        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self.is_sleeping = True

    def draw(self, surface, events, board):
        if board.evaluation.get('result') is None and not self.is_sleeping:
            self.is_sleeping = True
        if board.evaluation.get('result') is not None:
            if self.is_sleeping:
                self.is_sleeping = False
            else:
                for event in events:
                    if event.type == pygame.MOUSEMOTION:
                        self.pos = event.pos

                rect = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
                rect.set_alpha(math.floor(256 * 0.75))
                rect.fill((0, 0, 0))
                surface.blit(rect, (0, MENU_HEIGHT))

                rect = self.icon.get_rect(center=(BOARD_WIDTH // 2, (BOARD_HEIGHT + MENU_HEIGHT * 2) // 2))
                rect_bg = rect.inflate(30, 30)

                is_hovering = rect_bg.collidepoint(self.pos[0], self.pos[1])

                pygame.draw.rect(surface, COLORS.get('FONT_HOVER') if is_hovering else COLORS.get('FONT_SECONDARY'),
                                 rect_bg, 0, 3)
                surface.blit(self.icon, rect)

                if is_hovering and self.cursor == pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self.cursor = pygame.SYSTEM_CURSOR_HAND
                elif not is_hovering and self.cursor == pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.cursor = pygame.SYSTEM_CURSOR_ARROW
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP and is_hovering:
                        board.reset()
                        board.load(DEFAULT_FEN)
                        board.evaluation = board.evaluate()
                        self.pos = (0, 0)
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.cursor = pygame.SYSTEM_CURSOR_ARROW
