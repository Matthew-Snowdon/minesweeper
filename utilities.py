import pygame

# game settings
game_settings = {
    "ROWS": 9,  # initial setting, will change based on difficulty
    "COLS": 9,  # initial setting, will change based on difficulty
    "MINES": 10,  # initial setting, will change based on difficulty
    "MARGIN_SIZE": 20,  # This is static
    "CELL_SIZE": 50,  # This is static now
    "BANNER_HEIGHT": 120,  # This is static
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


def blit_img(surface, image, pos):
    surface.blit(image, pos)


# Load images
def load_image(loaded_name, width=game_settings["CELL_SIZE"],
               height=game_settings["CELL_SIZE"]):
    loaded_img = pygame.image.load(f'assets/{loaded_name}.png')
    return pygame.transform.scale(loaded_img, (width, height))


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


def draw_margins_and_corners(DISPLAYSURF, h_margin_img, v_margin_img, corners):
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


image_names = ["tile", "mine", "red_mine", "cross_mine", "question", "flag",
               "flat", "1", "2", "3", "4", "5", "h_margin", "v_margin",
               "shadow"]

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
