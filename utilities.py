import pygame

# Button dimensions
BUTTON_WIDTH = 70
BUTTON_HEIGHT = 70

# Shadow offset
SHADOW_OFFSET_Y = 2
SHADOW_OFFSET_X = 2

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (227, 227, 227)
GRAY = (179, 179, 179)
DARK_GRAY = (127, 127, 127)
RED = (255, 0, 0)

# game settings
game_settings = {
    "ROWS": 16,
    "COLS": 30,
    "MINES": 99,
    "MARGIN_SIZE": 20,
    "CELL_SIZE": 50,
    "BANNER_HEIGHT": 120,
}

game_settings.update({
    "SCREEN_WIDTH": game_settings["COLS"] * game_settings["CELL_SIZE"] +
                    game_settings["MARGIN_SIZE"] * 2,
    "SCREEN_HEIGHT": game_settings["ROWS"] * game_settings["CELL_SIZE"] +
                     game_settings["BANNER_HEIGHT"] + game_settings[
                         "MARGIN_SIZE"] * 2,
    "flag_count": game_settings["MINES"],
    "adjusted_banner_height": game_settings["BANNER_HEIGHT"] - game_settings[
        "MARGIN_SIZE"]
})


def update_screen_size():
    """
    This function updates the game screen size based on the configured
    number of rows and columns. It calculates the new screen width and
    height based on the cell size, margin size, and banner height and
    updates the global game_settings dictionary accordingly. Additionally,
    it loads new margin images with the updated dimensions and adjusts other
    game settings such as flag count and adjusted banner height.

        Global variables modified: - game_settings (dict): A dictionary
        holding various game settings like screen size, margin size, banner
        height, etc. - h_margin_img: The horizontal margin image which gets
        updated with new dimensions. - v_margin_img: The vertical margin
        image which gets updated with new dimensions.
    """
    # Update screen size based on rows and columns
    game_settings["SCREEN_WIDTH"] = \
        game_settings["COLS"] * game_settings["CELL_SIZE"] + \
        game_settings["MARGIN_SIZE"] * 2
    game_settings["SCREEN_HEIGHT"] = \
        game_settings["ROWS"] * game_settings["CELL_SIZE"] + \
        game_settings["BANNER_HEIGHT"] + game_settings["MARGIN_SIZE"] * 2

    # Update margin images
    global h_margin_img, v_margin_img
    h_margin_img = load_image('h_margin',
                              game_settings["SCREEN_WIDTH"],
                              game_settings["MARGIN_SIZE"])
    v_margin_img = load_image('v_margin',
                              game_settings["MARGIN_SIZE"],
                              game_settings["SCREEN_HEIGHT"])

    # Update other settings
    game_settings["flag_count"] = game_settings["MINES"]
    game_settings["adjusted_banner_height"] = \
        game_settings["BANNER_HEIGHT"] - game_settings["MARGIN_SIZE"]


def blit_img(surface, image, pos):
    """
    This function draws the specified image onto the surface at the given
    position.

        Parameters: surface (pygame.Surface): The surface on which the image
        will be drawn. image (pygame.Surface): The image to be drawn onto
        the surface. pos (tuple): A tuple containing the coordinates
        (x, y) at which the image will be drawn.
    """
    surface.blit(image, pos)


# Load images
def load_image(loaded_name, width=game_settings["CELL_SIZE"],
               height=game_settings["CELL_SIZE"]):
    """
    This function loads an image from the assets directory and resizes it to
    the specified dimensions.

        Parameters: loaded_name (str): The name of the image file (without
        extension) to be loaded from the 'assets' directory. width (int):
        The desired width of the loaded image. Defaults to the value of
        "CELL_SIZE" in game_settings. height (int): The desired height of
        the loaded image. Defaults to the value of "CELL_SIZE" in
        game_settings.

        Returns:
        pygame.Surface: The loaded and resized image.
        """
    loaded_img = pygame.image.load(f'assets/{loaded_name}.png')
    return pygame.transform.scale(loaded_img, (width, height))


def draw_margins_and_corners(DISPLAYSURF, h_margin_img, v_margin_img, corners):
    """
    This function draws the margins and corners of the gameboard on the
    given display surface.

        Parameters: DISPLAYSURF (pygame.Surface): The display surface where
        the margins and corners will be drawn. h_margin_img (
        pygame.Surface): The horizontal margin image to be used.
        v_margin_img (pygame.Surface): The vertical margin image to be used.
        corners (dict): A dictionary containing corner images keyed by their
        respective positions (top_L, top_R, bottom_L, bottom_R, banner_L,
        banner_R).

        Returns:
        None: The function directly modifies the DISPLAYSURF object.
        """
    blit_img(DISPLAYSURF, h_margin_img, (0, 0))
    blit_img(DISPLAYSURF, h_margin_img, (
        0, game_settings["SCREEN_HEIGHT"] - game_settings["MARGIN_SIZE"]))
    blit_img(DISPLAYSURF, h_margin_img, (0,
                                         game_settings["BANNER_HEIGHT"]))
    blit_img(DISPLAYSURF, v_margin_img, (0, 0))
    blit_img(DISPLAYSURF, v_margin_img, (game_settings["SCREEN_WIDTH"] -
                                         game_settings["MARGIN_SIZE"], 0))

    corner_names = ['top_L', 'top_R', 'bottom_L', 'bottom_R', 'banner_L',
                    'banner_R']
    corner_positions = [(0, 0), (
        game_settings["SCREEN_WIDTH"] - game_settings["MARGIN_SIZE"], 0),
                        (0, game_settings["SCREEN_HEIGHT"] - game_settings[
                            "MARGIN_SIZE"]),
                        (game_settings["SCREEN_WIDTH"] - game_settings[
                            "MARGIN_SIZE"],
                         game_settings["SCREEN_HEIGHT"] - game_settings[
                             "MARGIN_SIZE"]),
                        (0, game_settings["BANNER_HEIGHT"]),
                        (game_settings["SCREEN_WIDTH"] - game_settings[
                            "MARGIN_SIZE"], game_settings["BANNER_HEIGHT"])]

    for corner, position in zip(corner_names, corner_positions):
        blit_img(DISPLAYSURF, corners[corner], position)


# Load and scale images
image_dict = {}
for name in ['top_L_corner', 'top_R_corner', 'bottom_L_corner',
             'bottom_R_corner', 'banner_margin_L', 'banner_margin_R']:
    img = pygame.image.load(f'assets/{name}.png')
    img = pygame.transform.scale(img, (
        game_settings["MARGIN_SIZE"], game_settings["MARGIN_SIZE"]))
    image_dict[name] = img

# Load and scale margin images
h_margin_img = load_image('h_margin', game_settings["SCREEN_WIDTH"],
                          game_settings["MARGIN_SIZE"])
v_margin_img = load_image('v_margin', game_settings["MARGIN_SIZE"],
                          game_settings["SCREEN_HEIGHT"])

# Adjust the settings to 'Beginner' difficulty
game_settings["ROWS"] = 9
game_settings["COLS"] = 9
game_settings["MINES"] = 10
game_settings["SCREEN_WIDTH"] = 9 * game_settings["CELL_SIZE"] + 2 * \
                                game_settings["MARGIN_SIZE"]
game_settings["SCREEN_HEIGHT"] = 9 * game_settings["CELL_SIZE"] + \
                                 game_settings["BANNER_HEIGHT"] + 2 * \
                                 game_settings["MARGIN_SIZE"]

# Create a dictionary for the corner images
corners = {
    'top_L': image_dict['top_L_corner'],
    'top_R': image_dict['top_R_corner'],
    'bottom_L': image_dict['bottom_L_corner'],
    'bottom_R': image_dict['bottom_R_corner'],
    'banner_L': image_dict['banner_margin_L'],
    'banner_R': image_dict['banner_margin_R']
}

image_names = ["tile", "mine", "red_mine", "cross_mine", "question", "flag",
               "flat", "1", "2", "3", "4", "5", "6", "7", "8", "h_margin",
               "v_margin", "shadow"]

# Button images need different dimensions, so we handle them separately
button_image_names = ["smile", "smile_flat", "shock", "sad", "sad_flat",
                      "winner", "winner_flat"]

images = {}
for name in image_names:
    images[name] = load_image(name)

for name in button_image_names:
    images[name] = load_image(name, BUTTON_WIDTH, BUTTON_HEIGHT)

# Create a dictionary to map game state to images
game_state_images = {
    'smile': images['smile'],
    'shock': images['shock'],
    'sad': images['sad'],
    'winner': images['winner']
}

# Create a dictionary to map game state to pressed images
pressed_images = {
    'smile': images['smile_flat'],
    'shock': images['shock'],
    'sad': images['sad_flat'],
    'winner': images['winner_flat']
}

shadow_image = pygame.transform.scale(images['shadow'], (BUTTON_WIDTH,
                                                         BUTTON_HEIGHT))
