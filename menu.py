import pygame_menu
from banner import Banner
from gameboard import GameBoard
from utilities import *

theme = pygame_menu.themes.Theme(
    background_color=(0, 0, 0),  # Background color
    title_background_color=(0, 0, 0),  # Title background color (same as
    # background)
    title_font_color=(1, 1, 1),  # Set title font color to a nearly similar
    # color
    title_font_size=1  # Title font size to minimal value
)


class GameMenu:
    def __init__(self, surface, game_loop, draw):
        self.difficulty = 1
        self.surface = surface
        self.game_loop = game_loop
        self.draw = draw
        self.game_started = False
        self.level_menu = None
        self.menu = None
        self.create_menu(game_settings["SCREEN_WIDTH"],
                         game_settings["SCREEN_HEIGHT"])

    def create_menu(self, width, height):
        self.level_menu = pygame_menu.Menu('Difficulty Level', width,
                                           height, theme=theme)
        difficulty_selector = self.level_menu.add.selector(
            'Difficulty: ', [('Beginner', 1), ('Advanced', 2),
                             ('Expert', 3)], onchange=lambda _, difficulty:
            self.set_difficulty(_, difficulty))

        # Manually trigger the onchange event for the initial selection.
        difficulty_selector.change(1)

        self.level_menu.add.button('Start Game', self.start_game)
        self.level_menu.add.button('Back', pygame_menu.events.BACK)

        self.menu = pygame_menu.Menu('', width, height, theme=theme)
        self.menu.add.button('Play', self.level_menu)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def resize_menu(self, width, height):
        self.create_menu(width, height)

    def set_difficulty(self, _, difficulty):
        self.difficulty = difficulty

    def start_game(self):
        # Now update the rows, cols, mines, and window size based on the
        # stored difficulty.
        if self.difficulty == 1:  # Beginner
            game_settings["ROWS"] = 9
            game_settings["COLS"] = 9
            game_settings["MINES"] = 10
        elif self.difficulty == 2:  # Advanced
            game_settings["ROWS"] = 16
            game_settings["COLS"] = 16
            game_settings["MINES"] = 40
        else:  # Expert
            game_settings["ROWS"] = 16
            game_settings["COLS"] = 30
            game_settings["MINES"] = 99

        update_screen_size()

        self.surface = pygame.display.set_mode(
            (game_settings["SCREEN_WIDTH"], game_settings["SCREEN_HEIGHT"]))

        draw_margins_and_corners(self.surface, h_margin_img, v_margin_img,
                                 corners)

        # Call resize_menu after updating the screen size
        self.resize_menu(game_settings["SCREEN_WIDTH"],
                         game_settings["SCREEN_HEIGHT"])

        banner = Banner(self.surface, game_state_images, pressed_images)
        gameboard = GameBoard(self.surface, banner, game_settings["ROWS"],
                              game_settings["COLS"], game_settings["MINES"],
                              self.game_started)

        self.game_started = True

        self.game_loop(gameboard, banner)

    def run(self):
        self.menu.mainloop(self.surface)
