import pygame

import sound
from const import SQUARE_SIZE, COLORS, MENU_HEIGHT, ENVIRONMENT
from piece import Piece


class Promotion:
    def __init__(self):
        self.pos = (0, 0)
        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self.has_skipped_event = False

    def draw(self, surface, events, board):
        if board.promotion_square is not None:
            hovering_piece = None

            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.pos = event.pos

            row = board.promotion_square.row
            col = board.promotion_square.col
            color = board.promotion_square.piece.color
            pieces = ['q', 'b', 'n', 'r']
            offset = 0

            if board.promotion_square.piece.direction == 1:
                offset = SQUARE_SIZE * 3

            pygame.draw.rect(
                surface,
                COLORS.get('FONT_PRIMARY'),
                (col * SQUARE_SIZE, row * SQUARE_SIZE + MENU_HEIGHT - offset, SQUARE_SIZE, SQUARE_SIZE * 4)
            )

            for (index, piece_name) in enumerate(pieces if color == 'w' else list(reversed(pieces))):
                square = board.squares[row - index if color == 'b' else index][col]
                piece = Piece(square, piece_name, color)
                img_rect = piece.img.get_rect(center=square.center)

                surface.blit(
                    piece.img,
                    img_rect
                )

                is_hovering = img_rect.collidepoint(self.pos[0], self.pos[1])

                if is_hovering:
                    hovering_piece = piece

            if hovering_piece is not None and self.cursor == pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.cursor = pygame.SYSTEM_CURSOR_HAND
            elif hovering_piece is None and self.cursor == pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.cursor = pygame.SYSTEM_CURSOR_ARROW

            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and hovering_piece is not None:
                    if not self.has_skipped_event:
                        self.has_skipped_event = True
                    else:
                        hovering_piece.replace_initial_square(
                            board.squares[row][col]
                        )

                        board.promotion_square.piece.is_visible = False
                        board.promotion_square.piece = hovering_piece
                        board.promotion_square = None
                        board.pieces.append(hovering_piece)

                        sound.play('promote')
                        self.has_skipped_event = False

                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.cursor = pygame.SYSTEM_CURSOR_ARROW

                        evaluation = board.evaluate()
                        board.evaluation = evaluation

                        if ENVIRONMENT == 'development':
                            print(evaluation)

                        self.pos = (0, 0)
