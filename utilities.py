import pygame

# game settings
MARGIN_SIZE = 20  # Set margin size
SCREEN_WIDTH = 600 + MARGIN_SIZE * 2
BANNER_HEIGHT = 120 - MARGIN_SIZE
adjusted_banner_height = BANNER_HEIGHT - MARGIN_SIZE
SCREEN_HEIGHT = 600 + BANNER_HEIGHT + MARGIN_SIZE * 2
ROWS = 10
COLS = 10
MINES = 15
CELL_SIZE = (SCREEN_WIDTH - 2 * MARGIN_SIZE) // COLS
flag_count = MINES

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
def load_image(loaded_name, width=CELL_SIZE, height=CELL_SIZE):
    loaded_img = pygame.image.load(f'assets/{loaded_name}.png')
    return pygame.transform.scale(loaded_img, (width, height))


# Load and scale images
image_dict = {}
for name in ['top_L_corner', 'top_R_corner', 'bottom_L_corner',
             'bottom_R_corner', 'banner_margin_L', 'banner_margin_R']:
    img = pygame.image.load(f'assets/{name}.png')
    img = pygame.transform.scale(img, (MARGIN_SIZE, MARGIN_SIZE))
    image_dict[name] = img

# Load and scale margin images
h_margin_img = load_image('h_margin', SCREEN_WIDTH, MARGIN_SIZE)
v_margin_img = load_image('v_margin', MARGIN_SIZE, SCREEN_HEIGHT)

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
    blit_img(DISPLAYSURF, h_margin_img, (0, SCREEN_HEIGHT - MARGIN_SIZE))
    blit_img(DISPLAYSURF, h_margin_img, (0, BANNER_HEIGHT))
    blit_img(DISPLAYSURF, v_margin_img, (0, 0))
    blit_img(DISPLAYSURF, v_margin_img, (SCREEN_WIDTH - MARGIN_SIZE, 0))

    corner_names = ['top_L', 'top_R', 'bottom_L', 'bottom_R', 'banner_L',
                    'banner_R']
    corner_positions = [(0, 0), (SCREEN_WIDTH - MARGIN_SIZE, 0),
                        (0, SCREEN_HEIGHT - MARGIN_SIZE),
                        (SCREEN_WIDTH - MARGIN_SIZE,
                         SCREEN_HEIGHT - MARGIN_SIZE),
                        (0, BANNER_HEIGHT),
                        (SCREEN_WIDTH - MARGIN_SIZE, BANNER_HEIGHT)]

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
