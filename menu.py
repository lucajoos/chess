import math

import pygame.draw

import dialog
import sound
from const import COLORS, BOARD_WIDTH, MENU_HEIGHT, BOARD_HEIGHT, PIECES, DEFAULT_FEN, ENVIRONMENT


class Menu:
    def __init__(self, font):
        self.pos = (0, 0)
        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self.avatars = (
            pygame.transform.scale(pygame.image.load('assets/images/black_400.png'), (45, 45)),
            pygame.transform.scale(pygame.image.load('assets/images/white_400.png'), (45, 45)),
        )

        self.title = (
            font.render('Black', True, COLORS.get('FONT_PRIMARY')),
            font.render('White', True, COLORS.get('FONT_PRIMARY')),
        )

        self.icons = {
            'download': pygame.image.load('assets/images/icons/download.svg'),
            'upload': pygame.image.load('assets/images/icons/upload.svg'),
            'refresh': pygame.image.load('assets/images/icons/refresh.svg')
        }
    def draw(self, surface, events, font, board):
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, 0, BOARD_WIDTH, MENU_HEIGHT))
        pygame.draw.rect(surface, COLORS.get('MENU'), (0, BOARD_HEIGHT + MENU_HEIGHT, BOARD_WIDTH, MENU_HEIGHT))
        surface.blit(self.avatars[0], self.avatars[0].get_rect(center=(20 * 2, MENU_HEIGHT // 2)))
        surface.blit(self.avatars[1], self.avatars[1].get_rect(center=(20 * 2, BOARD_HEIGHT + MENU_HEIGHT + MENU_HEIGHT // 2)))
        surface.blit(self.title[0], self.title[0].get_rect(topleft=(70, ((MENU_HEIGHT - 45) // 2 + 3))))
        surface.blit(self.title[1], self.title[1].get_rect(topleft=(70, BOARD_HEIGHT + MENU_HEIGHT + ((MENU_HEIGHT - 45) // 2 + 3))))

        black_group_count = 0
        black_piece_count = 0
        black_score = 0

        for piece_category in PIECES:
            pieces = board.captures.get('b').get(piece_category)
            for (index, piece) in enumerate(pieces):
                black_score += piece.value
                img = pygame.transform.smoothscale(piece.img, (25, 25))
                surface.blit(img, img.get_rect(
                    topleft=(65 + (index + black_piece_count) * 7 + black_group_count * 13, (MENU_HEIGHT // 2 - 3))))

            black_piece_count += len(pieces)

            if len(pieces) > 0:
                black_group_count += 1

        white_group_count = 0
        white_piece_count = 0
        white_score = 0

        for piece_category in PIECES:
            pieces = board.captures.get('w').get(piece_category)
            for (index, piece) in enumerate(pieces):
                white_score += piece.value
                img = pygame.transform.smoothscale(piece.img, (25, 25))
                surface.blit(img, img.get_rect(
                    topleft=(65 + (index + white_piece_count) * 7 + white_group_count * 13, MENU_HEIGHT + BOARD_HEIGHT + (MENU_HEIGHT // 2 - 3))))

            white_piece_count += len(pieces)

            if len(pieces) > 0:
                white_group_count += 1

        if black_score > white_score:
            img = font.render(f'+{abs(math.floor(black_score - white_score))}', True, COLORS.get('FONT_LIGHT'))
            surface.blit(img, img.get_rect(
                topleft=(70 + black_piece_count * 7 + black_group_count * 13, MENU_HEIGHT // 2 + 3)))
        elif white_score > black_score:
            img = font.render(f'+{abs(math.floor(black_score - white_score))}', True, COLORS.get('FONT_LIGHT'))
            surface.blit(img, img.get_rect(
                topleft=(70 + white_piece_count * 7 + white_group_count * 13, MENU_HEIGHT + BOARD_HEIGHT + MENU_HEIGHT // 2 + 3)))

        hovering = None

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.pos = event.pos

        for (index, option) in enumerate(['download', 'upload', 'refresh']):
            img = self.icons.get(option)
            rect = img.get_rect(center=(BOARD_WIDTH - (3 - index) * 40, MENU_HEIGHT // 2))
            rect_bg = rect.inflate(15, 15)

            is_hovering = rect_bg.collidepoint(self.pos[0], self.pos[1])

            if is_hovering:
                hovering = option

            pygame.draw.rect(surface, COLORS.get('FONT_LIGHT') if is_hovering else COLORS.get('FONT_SECONDARY'), rect_bg, 0, 3)
            surface.blit(img, rect)

        if hovering is not None and self.cursor == pygame.SYSTEM_CURSOR_ARROW:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.cursor = pygame.SYSTEM_CURSOR_HAND
        elif hovering is None and self.cursor == pygame.SYSTEM_CURSOR_HAND:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.cursor = pygame.SYSTEM_CURSOR_ARROW

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and hovering is not None:
                if hovering == 'download':
                    fen = board.save()

                    if ENVIRONMENT == 'development':
                        print(fen)
                    else:
                        dialog.save(fen)
                if hovering == 'upload':
                    filename = dialog.load()

                    if filename is not None:
                        file = open(filename, 'r')
                        fen = file.read()
                        board.load(fen)
                        board.evaluation = board.evaluate()
                        sound.play('game-start')
                if hovering == 'refresh':
                    board.reset()
                    board.load(DEFAULT_FEN)
                    board.evaluation = board.evaluate()
                    sound.play('game-start')
