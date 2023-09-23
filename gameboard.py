# from minesweeper import *
from utilities import *
import random


class GameBoard:
    """
    Represents the game board of a minesweeper game, handling game logic,
    cell state management, and rendering of the game board.

    Attributes:
        display_surface: Surface object where the game board is rendered.
        banner: Banner object to display game-related information such as timer
        and mine count.
        rows, cols: Dimensions of the game board in terms of number of rows and
        columns.
        mines: Total number of mines on the game board.
        mine_coordinates: List of coordinates where mines are located.
        game_started: Boolean flag indicating if the game has started.
        board: 2D array representing the current state of each cell (mine,
        number, or unrevealed).
        flag_count: Counter for the number of flags placed by the player.
        game_over: Boolean flag indicating if the game has ended (either win
        or lose).
        game_active: Boolean flag indicating if the game is currently active.
        first_click: Boolean flag indicating if the first click on the board
        has been made.
        revealed: 2D boolean array indicating if a cell has been revealed.
        flagged: 2D boolean array indicating if a cell is flagged.
        questioned: 2D boolean array indicating if a cell is marked with a
        question.
        game_over_mine: Coordinates of the mine that caused the game to end,
        if applicable.
        game_state: String representing the current state of the game ('smile',
        'sad', 'winner').
        pressed: Coordinates of the currently pressed cell, if any.
        first_mine_revealed: Boolean flag indicating if the first mine has been
        revealed.
        start_ticks: Timestamp marking the start of the game timer.
        cell_clicked: Boolean flag indicating if a cell has been clicked during
        the current update.
        temp_flattened: Set of cells that are temporarily displayed as
        flattened.
    """
    def __init__(self, display_surface, banner, rows, cols, mines,
                 game_started):
        """
                Initializes the GameBoard with the given parameters.

                Args: display_surface: The surface on which the game board
                will be drawn. banner: The banner object associated with the
                game. rows: Number of rows in the game board. cols: Number
                of columns in the game board. mines: Number of mines to be
                placed on the game board. game_started: Boolean indicating
                whether the game has started.
        """
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
        self.temp_flattened = set()

    def initialize_board(self):
        """
                Initializes the game board and related attributes.
                """
        self.board = [['-' for _ in range(self.cols)] for _ in
                      range(self.rows)]
        self.initialize_revealed()
        self.initialize_flagged()
        self.initialize_questioned()

    def initialize_revealed(self):
        """
                Initializes the 'revealed' attribute to False for all cells.
                """
        self.revealed = [[False for _ in range(self.cols)] for _ in
                         range(self.rows)]

    def initialize_flagged(self):
        """
                Initializes the 'flagged' attribute to False for all cells.
                """
        self.flagged = [[False for _ in range(self.cols)] for _ in
                        range(self.rows)]

    def initialize_questioned(self):
        """
                Initializes the 'questioned' attribute to False for all cells.
                """
        self.questioned = [[False for _ in range(self.cols)] for _ in
                           range(self.rows)]

    def generate_board_except(self, row, col):
        """
        Generates the game board with mines, except at the specified row and
        column.

                Args:
                    row: The row number where a mine should not be placed.
                    col: The column number where a mine should not be placed.
                """
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
                mine_row, mine_col = (random.randint(0,
                                                    self.rows - 1),
                                      random.randint(
                    0, self.cols - 1))
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
        """
        Toggles a flag or question mark on a cell at the specified row and
        column.

                Args:
                    row: The row number of the cell.
                    col: The column number of the cell.
                """
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
        """
                Gets the rectangle for a cell at the specified row and column.

                Args:
                    row: The row number of the cell.
                    col: The column number of the cell.

                Returns: A pygame.Rect object representing the area of the
                specified cell.
        """
        return pygame.Rect(game_settings["MARGIN_SIZE"] + col *
                           game_settings["CELL_SIZE"],
                           game_settings["MARGIN_SIZE"] +
                           game_settings["BANNER_HEIGHT"] + row *
                           game_settings["CELL_SIZE"],
                           game_settings["CELL_SIZE"],
                           game_settings["CELL_SIZE"])

    def draw_board(self):
        """
        Renders the entire game board on the display surface. This method
        iterates through each cell in the game board, drawing the
        appropriate image based on the cell's state. It handles different
        scenarios such as revealed cells, flagged cells, cells with mines,
        and special cases like the cell that caused the game to end. The
        method also updates the visual representation of cells when they are
        pressed, and draws borders around each cell for a grid-like appearance.

    The method considers the following states for each cell:
    - If the cell is in the 'temp_flattened' set, it's displayed as flat.
    - If the game is over and the cell contains a mine, different images are
    used based on whether the mine caused the game over or if it was flagged
    incorrectly.
    - For revealed cells, the method displays either a mine, a flat image, or a
    number based on the cell content.
    - Flagged and questioned cells are drawn with their respective images.
    - Unrevealed cells are drawn with the default tile image.
    - If a cell is currently pressed, it's shown as flat.

    The method concludes by updating the display to reflect the new state of
    the game board.
    """
        for row in range(self.rows):
            for col in range(self.cols):
                rect = self.get_cell_rect(row, col)
                if row >= self.rows or col >= self.cols:
                    print(
                        f"Potential IndexError - Row: {row}, Col: {col}, "
                        f"Self Rows: {self.rows}, Self Cols: {self.cols}")
                    continue

                # Adding a check here
                if row < 0 or col < 0 or row >= len(self.board) or col >= len(
                        self.board[0]):
                    print(f"IndexError prevented - Row: {row}, Col: {col}")
                    continue

                cell_content = self.board[row][col]

                if (row, col) in self.temp_flattened:
                    self.display_surface.blit(images['flat'], rect)
                else:
                    if self.game_over and cell_content == '#':
                        if (row, col) == self.game_over_mine:
                            self.display_surface.blit(images['red_mine'], rect)
                        elif self.flagged[row][col]:
                            self.display_surface.blit(images['cross_mine'],
                                                      rect)
                        else:
                            self.display_surface.blit(images['mine'], rect)
                    elif self.revealed[row][col]:
                        if cell_content == '#':
                            self.display_surface.blit(images['mine'], rect)
                        elif cell_content == '0':
                            self.display_surface.blit(images['flat'], rect)
                        else:
                            self.display_surface.blit(images[cell_content],
                                                      rect)
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
        """
                Reveals the cell at the specified row and column.

                Args:
                    row: The row number of the cell to reveal.
                    col: The column number of the cell to reveal.
                """
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
        """
                Resets the game with new dimensions and number of mines.

                Args:
                    rows: New number of rows for the game board.
                    cols: New number of columns for the game board.
                    mines: New number of mines for the game board.
                """
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
        """
        Evaluates the game board to determine if the player has won. Winning
        is achieved when all non-mine cells have been revealed. If the
        player has won, updates the game state to reflect the victory,
        updating the banner and drawing the final state of the game board.
        """
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
