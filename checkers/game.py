import pygame
from checkers.board import Board
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, GREY, BLACK
from .piece import Piece
pygame.font.init()

FONT_1 = pygame.font.SysFont("comicsans", 19)
FONT_2 = pygame.font.SysFont("comicsans", 15)

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.turn_count= 0

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self .valid_moves)
        self.draw_menu(self.win)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self,row,col):
        if self.selected:
            result = self._move(row,col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row,col)
        if piece !=0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self,row,col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col*SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn ==RED:
            self.turn = WHITE
        else:
            self.turn = RED
        self.turn_count +=1
        return self.turn_count

    def draw_menu(self, win):

        pygame.draw.rect(win, GREY, (8 * SQUARE_SIZE, 0 * SQUARE_SIZE, SQUARE_SIZE * 2, SQUARE_SIZE * 8))
        pygame.draw.rect(win, WHITE, (8.1 * SQUARE_SIZE, 0.1 * SQUARE_SIZE, SQUARE_SIZE * 1.8, SQUARE_SIZE * 7.5))

        pygame.draw.rect(win, BLACK, (8.3 * SQUARE_SIZE, 0.3 * SQUARE_SIZE, SQUARE_SIZE * 1.4, SQUARE_SIZE * 0.6))
        level_text = FONT_1.render(f"Turn:{self.turn_count}", 1, (255, 0, 255))
        win.blit(level_text, (SQUARE_SIZE * 8.4, SQUARE_SIZE / 4))

        pygame.draw.rect(win, (255,180,0), (8.3 * SQUARE_SIZE,  SQUARE_SIZE, SQUARE_SIZE * 1.4, SQUARE_SIZE * 5))
        if self.turn_count>0:
            turn_info_text = FONT_2.render("{self.turn_count}", 1, (255, 0, 255))
            win.blit(turn_info_text, (SQUARE_SIZE * 8.4, SQUARE_SIZE ))

