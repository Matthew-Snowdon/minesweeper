import pygame_menu
from banner import Banner
from gameboard import GameBoard
from utilities import *

theme = pygame_menu.themes.Theme(
    background_color=(0, 0, 0),  # Background color
    title_font_size=1  # Title font size to minimal value
)


class GameMenu:
    """
    Represents the main menu of the minesweeper game, handling game
    settings, difficulty level selection, and controls instructions. It
    allows players to interact with different parts of the game such as
    starting a new game or adjusting settings.

        Attributes:
            gameboard: Reference to the GameBoard object.
            banner: Reference to the Banner object for displaying game
            information.
            controls_menu: The submenu for showing game controls.
            difficulty: An integer representing the current difficulty level
            of the game.
            surface: The surface on which the menu is drawn.
            game_loop: Function to start the main game loop.
            draw: Function to draw game elements.
            level_menu: The submenu for selecting the difficulty level.
            menu: The main menu object from pygame_menu.
        """
    def __init__(self, surface, game_loop, draw, gameboard=None, banner=None):
        """
        Initializes the GameMenu with the necessary references and settings.

                Args:
                    surface: The surface on which the menu will be drawn.
                    game_loop: Reference to the function that starts the main
                    game loop.
                    draw: Function to draw game elements.
                    gameboard: (Optional) Reference to the GameBoard object.
                    banner: (Optional) Reference to the Banner object.
                """
        self.gameboard = gameboard
        self.banner = banner
        self.controls_menu = None
        self.difficulty = 1
        self.surface = surface
        self.game_loop = game_loop
        self.draw = draw
        self.level_menu = None
        self.menu = None
        self.create_menu(game_settings["SCREEN_WIDTH"],
                         game_settings["SCREEN_HEIGHT"])

    def create_menu(self, width, height):
        """
        Creates the main menu and submenus for the game, including controls
        and difficulty level settings.

                Args:
                    width: The width of the menu screen.
                    height: The height of the menu screen.
                """
        # Create a controls menu
        self.controls_menu = pygame_menu.Menu('Controls', width, height,
                                         theme=theme)
        self.controls_menu.add.label('ESC: Show Menu', max_char=-1)
        self.controls_menu.add.label('Left-Click: Interact with cells',
                                     max_char=-1)
        self.controls_menu.add.label('Right-Click: Toggle flags', max_char=-1)
        self.controls_menu.add.button('Back', pygame_menu.events.BACK)

        self.level_menu = pygame_menu.Menu('Difficulty Level', width,
                                           height, theme=theme)
        difficulty_selector = self.level_menu.add.selector(
            'Difficulty: ', [('Beginner', 1), ('Advanced', 2),
                             ('Expert', 3)], onchange=lambda _, difficulty:
            self.set_difficulty(_, difficulty))

        # Manually trigger the onchange event for the initial selection.
        # difficulty_selector.change(1)

        self.level_menu.add.button('Start Game', self.start_game)
        self.level_menu.add.button('Back', pygame_menu.events.BACK)
        self.menu = pygame_menu.Menu('', width, height, theme=theme)
        self.menu.add.label(
            "Hit ESC to bring up the menu WARNING: game state lost",
            max_char=-1, font_color=(255, 0, 0))
        self.menu.add.button('Play', self.level_menu)
        self.menu.add.button('Controls', self.controls_menu)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def resize_menu(self, width, height):
        """
        Resizes the menu to the given dimensions. This is useful when the
        game window size is adjusted.

                Args:
                    width: New width of the game window.
                    height: New height of the game window.
                """
        self.create_menu(width, height)

    def set_difficulty(self, _, difficulty):
        """
        Sets the difficulty level for the game. This affects the number of
        rows, columns, and mines on the game board.

                Args:
                    difficulty: An integer representing the desired difficulty
                    level.
                """
        self.difficulty = difficulty

    def start_game(self):
        """
        Starts a new game with the selected difficulty level. This method
        sets up the game board with the specified number of rows, columns,
        and mines based on the chosen difficulty. It also handles the
        resizing of the menu and initializes the game board and banner if
        they are not already set.
        """
        # Now update the rows, cols, mines, and window size based on the
        # stored difficulty.
        if self.difficulty == 1:  # Beginner
            self.gameboard.rows = game_settings["ROWS"] = 9
            self.gameboard.cols = game_settings["COLS"] = 9
            self.gameboard.mines = game_settings["MINES"] = 10

        elif self.difficulty == 2:  # Advanced
            self.gameboard.rows = game_settings["ROWS"] = 16
            self.gameboard.cols = game_settings["COLS"] = 16
            self.gameboard.mines = game_settings["MINES"] = 40

        elif self.difficulty == 3:  # Expert
            self.gameboard.rows = game_settings["ROWS"] = 16
            self.gameboard.cols = game_settings["COLS"] = 30
            self.gameboard.mines = game_settings["MINES"] = 99

        print(
            f"Setting up game with {self.gameboard.rows} rows, "
            f"{self.gameboard.cols} cols, "
            f"and {self.gameboard.mines} mines")

        print(f'Resizing menu to width: '
              f'{game_settings["SCREEN_WIDTH"]}, height: '
              f'{game_settings["SCREEN_HEIGHT"]}')
        update_screen_size()

        self.surface = pygame.display.set_mode(
            (game_settings["SCREEN_WIDTH"], game_settings["SCREEN_HEIGHT"]))

        draw_margins_and_corners(self.surface, h_margin_img, v_margin_img,
                                 corners)

        # Call resize_menu after updating the screen size
        self.resize_menu(game_settings["SCREEN_WIDTH"],
                         game_settings["SCREEN_HEIGHT"])
        print(f'Resizing menu to width: '
              f'{game_settings["SCREEN_WIDTH"]}, height: '
              f'{game_settings["SCREEN_HEIGHT"]}')

        pygame.display.flip()

        if not self.banner:
            self.banner = Banner(self.surface, game_state_images,
                                 pressed_images)

        if self.gameboard:
            self.gameboard.reset_game(self.gameboard.rows,
                                      self.gameboard.cols,
                                      self.gameboard.mines)
            self.gameboard.initialize_board()
        else:
            self.gameboard = GameBoard(self.surface, self.banner,
                                       self.gameboard.rows,
                                       self.gameboard.cols,
                                       self.gameboard.mines,
                                       game_started=False)
            self.gameboard.initialize_board()

        self.gameboard.game_started = True

        self.game_loop(self.gameboard, self.banner)

    def run(self):
        """
        Runs the menu loop, handling events and updating the menu display.
        This is the main entry point for the menu system and is called to
        display the menu on the screen.
        """

        events = pygame.event.get()
        self.menu.update(events)
        self.menu.mainloop(self.surface)
