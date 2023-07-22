# from minesweeper import *
from utilities import *
import random


class GameBoard:
    def __init__(self, display_surface, banner):
        self.display_surface = display_surface
        self.banner = banner
        self.board = [['-' for _ in range(COLS)] for _ in range(ROWS)]
        self.mines = []
        self.flag_count = MINES
        self.game_over = False
        self.game_active = True
        self.first_click = True
        self.revealed = [[False for _ in range(ROWS)] for _ in range(COLS)]
        self.flagged = [[False for _ in range(ROWS)] for _ in range(COLS)]
        self.questioned = [[False for _ in range(ROWS)] for _ in range(COLS)]
        self.game_over_mine = None
        self.game_state = 'smile'
        self.pressed = None
        self.first_mine_revealed = False

    def generate_board_except(self, row, col):
        self.board = [['-' for col in range(COLS)] for row in range(ROWS)]
        self.mines = []  # Reset mines
        for i in range(MINES):
            mine_row, mine_col = random.randint(0, ROWS - 1), \
                random.randint(0, COLS - 1)
            while self.board[mine_row][mine_col] == '#' or (
                    mine_row == row and mine_col == col):
                mine_row, mine_col = random.randint(0,
                                                    ROWS - 1), random.randint(
                    0, COLS - 1)
            self.board[mine_row][mine_col] = '#'
            self.mines.append((mine_row, mine_col))  # Store mine coordinates

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != '#':
                    count = 0
                    for row_offset in range(-1, 2):
                        for col_offset in range(-1, 2):
                            if (0 <= row + row_offset < ROWS) and (
                                    0 <= col + col_offset < COLS):
                                if self.board[row + row_offset][
                                    col + col_offset] == '#':
                                    count += 1
                    self.board[row][col] = str(count)

    def toggle_flag(self, row, col):
        if self.flag_count == 0 and not self.flagged[row][col]:
            return
        # If it's not flagged or questioned, flag it
        if not self.flagged[row][col] and not self.questioned[row][col]:
            self.flagged[row][col] = True
            self.flag_count -= 1  # Decrease the flag count
        # If it's flagged, question it and unflag
        elif self.flagged[row][col] and not self.questioned[row][col]:
            self.flagged[row][col] = False
            self.questioned[row][col] = True
            self.flag_count += 1  # Increase the flag count
        # If it's questioned, reset it
        elif not self.flagged[row][col] and self.questioned[row][col]:
            self.questioned[row][col] = False
        # Ensure flag_count doesn't go into negative
        self.flag_count = max(0, self.flag_count)

    @staticmethod
    def get_cell_rect(row, col):
        return pygame.Rect(MARGIN_SIZE + col * CELL_SIZE,
                           MARGIN_SIZE + BANNER_HEIGHT + row * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                rect = self.get_cell_rect(row, col)
                if self.revealed[row][col]:
                    cell_content = self.board[row][col]
                    if cell_content == '#':
                        if self.game_over and (
                                row, col) == self.game_over_mine:
                            self.display_surface.blit(images['red_mine'], rect)
                        else:
                            self.display_surface.blit(images['mine'], rect)
                    elif cell_content == '0':
                        self.display_surface.blit(images['flat'], rect)
                    elif cell_content == '1':
                        self.display_surface.blit(images['1'], rect)
                    elif cell_content == '2':
                        self.display_surface.blit(images['2'], rect)
                    elif cell_content == '3':
                        self.display_surface.blit(images['3'], rect)
                    elif cell_content == '4':
                        self.display_surface.blit(images['4'], rect)
                    elif cell_content == '5':
                        self.display_surface.blit(images['5'], rect)
                elif self.flagged[row][col]:
                    self.display_surface.blit(images['flag'], rect)
                elif self.questioned[row][col]:
                    self.display_surface.blit(images['question'], rect)
                else:
                    self.display_surface.blit(images['tile'], rect)

                pygame.draw.rect(self.display_surface, DARK_GRAY, rect, 1)

    def reveal_cell(self, row, col):
        if not self.revealed[row][col] and not self.flagged[row][col]:
            self.revealed[row][col] = True
            if self.board[row][col] == '#':
                self.game_over = True
                self.game_active = False
                self.game_state = 'sad'
                pygame.draw.rect(self.banner.display_surface, BLACK,
                                 self.banner.button_rect)
                self.banner.display_surface.blit(images[self.game_state],
                                                 self.banner.button_rect.
                                                 topleft)
                pygame.display.update()  # Update the display
                self.game_over_mine = (row, col)
                print("Game Over!")
            elif self.board[row][col] == '0':
                for row_offset in range(-1, 2):
                    for col_offset in range(-1, 2):
                        if (0 <= row + row_offset < ROWS) and (
                                0 <= col + col_offset < COLS):
                            self.reveal_cell(row + row_offset,
                                             col + col_offset)
            self.check_game_won()

    def reset_game(self):
        pygame.time.get_ticks()
        self.flag_count = MINES
        self.game_active = True
        self.game_over = False
        self.first_click = True
        self.game_state = 'smile'
        self.pressed = None
        self.revealed = [[False for _ in range(ROWS)] for _ in range(COLS)]
        self.flagged = [[False for _ in range(ROWS)] for _ in range(COLS)]
        self.questioned = [[False for _ in range(ROWS)] for _ in range(COLS)]
        self.generate_board_except(-1, -1)

    def check_game_won(self):
        if not self.game_over and self.game_active:
            for row in range(ROWS):
                for col in range(COLS):
                    if self.board[row][col] != '#' and not \
                            self.revealed[row][col]:
                        return
            self.game_over = True
            self.game_active = False
            self.game_state = 'winner'
            pygame.draw.rect(self.banner.display_surface, BLACK,
                             self.banner.button_rect)
            self.banner.display_surface.blit(images[self.game_state],
                                             self.banner.button_rect.topleft)
            print("Congratulations! You won!")
            # Draw the game board with revealed cells
            self.draw_board()
            # Update the display
            pygame.display.update()
