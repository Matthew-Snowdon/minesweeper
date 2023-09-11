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
        self.mine_coordinates = []
        self.game_started = game_started
        self.board = [['-' for _ in range(self.cols)]
                      for _ in range(self.rows)]
        self.flag_count = self.mines
        self.game_over = False
        self.game_active = True
        self.first_click = True
        self.revealed = [[False for _ in range(self.rows)]
                         for _ in range(self.cols)]
        self.flagged = [[False for _ in range(self.rows)]
                        for _ in range(self.cols)]
        self.questioned = [[False for _ in range(self.rows)]
                           for _ in range(self.cols)]
        self.game_over_mine = None
        self.game_state = 'smile'
        self.pressed = None
        self.first_mine_revealed = False
        self.start_ticks = None
        self.cell_clicked = False

    def initialize_board(self):
        self.board = [['-' for _ in range(self.cols)] for _ in
                      range(self.rows)]
        self.initialize_revealed()
        self.initialize_flagged()
        self.initialize_questioned()

    def initialize_revealed(self):
        self.revealed = [[False for _ in range(self.cols)] for _ in
                         range(self.rows)]

    def initialize_flagged(self):
        self.flagged = [[False for _ in range(self.cols)] for _ in
                        range(self.rows)]

    def initialize_questioned(self):
        self.questioned = [[False for _ in range(self.cols)] for _ in
                           range(self.rows)]

    def generate_board_except(self, row, col):
        print(
            f"Generating board with {self.rows} rows and "
            f"{self.cols} columns and {self.mines} mines")
        self.board = [['-' for _ in range(self.cols)]
                      for _ in range(self.rows)]
        self.mine_coordinates = []  # Reset mines
        for i in range(self.mines):
            mine_row, mine_col = random.randint(0, self.rows -
                                                1), \
                random.randint(0, self.cols - 1)
            while (mine_row >= self.rows or mine_col >= self.cols or
                   self.board[mine_row][mine_col] == '#' or
                   (mine_row == row and mine_col == col)):
                mine_row, mine_col = random.randint(0,
                                                    self.rows - 1), random.randint(
                    0, self.cols - 1)
            self.board[mine_row][mine_col] = '#'
            self.mine_coordinates.append((mine_row, mine_col))

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != '#':
                    count = 0
                    for row_offset in range(-1, 2):
                        for col_offset in range(-1, 2):
                            if (0 <= row + row_offset <
                                self.rows) and \
                                    (0 <= col + col_offset <
                                     self.cols):
                                if self.board[row + row_offset][
                                    col + col_offset] == '#':
                                    count += 1
                    self.board[row][col] = str(count)

    def toggle_flag(self, row, col):
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
        for row in range(self.rows):
            for col in range(self.cols):
                rect = self.get_cell_rect(row, col)
                if row >= self.rows or col >= self.cols:
                    print(
                        f"Potential IndexError - Row: {row}, Col: {col}, Self Rows: {self.rows}, Self Cols: {self.cols}")
                    continue

                # Adding an additional check here
                if row < 0 or col < 0 or row >= len(self.board) or col >= len(
                        self.board[0]):
                    print(f"IndexError prevented - Row: {row}, Col: {col}")
                    continue

                cell_content = self.board[row][col]

                if self.game_over and cell_content == '#':
                    if (row, col) == self.game_over_mine:
                        self.display_surface.blit(images['red_mine'], rect)
                    elif self.flagged[row][col]:
                        self.display_surface.blit(images['cross_mine'], rect)
                    else:
                        self.display_surface.blit(images['mine'], rect)
                elif self.revealed[row][col]:
                    if cell_content == '#':
                        self.display_surface.blit(images['mine'], rect)
                    elif cell_content == '0':
                        self.display_surface.blit(images['flat'], rect)
                    else:
                        self.display_surface.blit(images[cell_content], rect)
                elif self.flagged[row][col]:
                    self.display_surface.blit(images['flag'], rect)
                elif self.questioned[row][col]:
                    self.display_surface.blit(images['question'], rect)
                else:
                    self.display_surface.blit(images['tile'], rect)

                # Handling the 'pressed' state
                if self.pressed is not None and self.pressed == (row, col):
                    self.display_surface.blit(images['flat'], rect)

                pygame.draw.rect(self.display_surface, DARK_GRAY, rect, 1)
        pygame.display.update()

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
                        if (0 <= row + row_offset < self.rows) and (
                                0 <= col + col_offset < self.cols):
                            self.reveal_cell(row + row_offset,
                                             col + col_offset)
            self.check_game_won()

    def reset_game(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.mine_coordinates = []
        self.start_ticks = None
        self.banner.timer = 0
        self.game_started = False
        self.flag_count = self.mines
        self.banner.counter = self.flag_count
        self.game_active = True
        self.game_over = False
        self.first_click = True
        self.game_state = 'smile'
        self.pressed = None
        self.initialize_board()

    def check_game_won(self):
        if not self.game_over and self.game_active:
            for row in range(self.rows):
                for col in range(self.cols):
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
