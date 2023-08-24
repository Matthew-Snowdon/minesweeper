# from minesweeper import *
from utilities import *
import random


class GameBoard:
    def __init__(self, display_surface, banner, rows, cols, mines,
                 game_started):
        self.display_surface = display_surface
        self.banner = banner
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.game_started = game_started
        self.board = [['-' for _ in range(cols)] for _ in range(rows)]
        self.flag_count = mines
        self.game_over = False
        self.game_active = True
        self.first_click = False
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.questioned = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over_mine = None
        self.game_state = 'smile'
        self.pressed = None
        self.first_mine_revealed = False
        self.start_ticks = None
        self.cell_clicked = False

    def generate_board_except(self, row, col):
        self.board = [['-' for col in range(game_settings["COLS"])] for row in
                      range(game_settings["ROWS"])]
        self.mines = []  # Reset mines
        for i in range(game_settings["MINES"]):
            mine_row, mine_col = random.randint(0, game_settings["ROWS"] -
                                                1), \
                random.randint(0, game_settings["COLS"] - 1)
            while self.board[mine_row][mine_col] == '#' or (
                    mine_row == row and mine_col == col):
                mine_row, mine_col = random.randint(0, game_settings["ROWS"] -
                                                    1), \
                    random.randint(0, game_settings["COLS"] - 1)
            self.board[mine_row][mine_col] = '#'
            self.mines.append((mine_row, mine_col))  # Store mine coordinates

        for row in range(game_settings["ROWS"]):
            for col in range(game_settings["COLS"]):
                if self.board[row][col] != '#':
                    count = 0
                    for row_offset in range(-1, 2):
                        for col_offset in range(-1, 2):
                            if (0 <= row + row_offset <
                                game_settings["ROWS"]) and \
                                    (0 <= col + col_offset <
                                     game_settings["COLS"]):
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
        return pygame.Rect(game_settings["MARGIN_SIZE"] + col *
                           game_settings["CELL_SIZE"],
                           game_settings["MARGIN_SIZE"] +
                           game_settings["BANNER_HEIGHT"] + row *
                           game_settings["CELL_SIZE"],
                           game_settings["CELL_SIZE"],
                           game_settings["CELL_SIZE"])

    def draw_board(self):
        for row in range(game_settings["ROWS"]):
            for col in range(game_settings["COLS"]):
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

                pygame.draw.rect(self.display_surface, DARK_GRAY, rect,
                                 1)

    def reveal_cell(self, row, col):
        if not self.revealed[row][col] and not self.flagged[row][col]:
            self.revealed[row][col] = True
            if self.board[row][col] == '#':
                self.game_over = True
                self.game_active = False
                self.game_state = 'sad'
                self.game_started = False
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
                        if (0 <= row + row_offset < game_settings[
                            "ROWS"]) and (
                                0 <= col + col_offset < game_settings["COLS"]):
                            self.reveal_cell(row + row_offset,
                                             col + col_offset)
            self.check_game_won()

    def reset_game(self):
        self.start_ticks = pygame.time.get_ticks()
        self.game_started = False
        self.flag_count = game_settings["MINES"]
        self.game_active = True
        self.game_over = False
        self.first_click = False
        self.game_state = 'smile'
        self.pressed = None
        self.revealed = [[False for _ in range(game_settings["ROWS"])] for _ in
                         range(game_settings["COLS"])]
        self.flagged = [[False for _ in range(game_settings["ROWS"])] for _ in
                        range(game_settings["COLS"])]
        self.questioned = [[False for _ in range(game_settings["ROWS"])] for _
                           in range(game_settings["COLS"])]
        self.generate_board_except(-1, -1)

    def check_game_won(self):
        if not self.game_over and self.game_active:
            for row in range(game_settings["ROWS"]):
                for col in range(game_settings["COLS"]):
                    if self.board[row][col] != '#' and not \
                            self.revealed[row][col]:
                        return
            self.game_over = True
            self.game_active = False
            self.game_state = 'winner'
            self.game_started = False
            pygame.draw.rect(self.banner.display_surface, BLACK,
                             self.banner.button_rect)
            self.banner.display_surface.blit(images[self.game_state],
                                             self.banner.button_rect.topleft)
            print("Congratulations! You won!")
            # Draw the game board with revealed cells
            self.draw_board()
            # Update the display
            pygame.display.update()
