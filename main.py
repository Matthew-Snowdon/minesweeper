import sys
from gameboard import GameBoard
from banner import Banner
from menu import GameMenu
from utilities import *

# initialize Pygame
pygame.init()

LEFT_MOUSE_BUTTON = 1
MIDDLE_MOUSE_BUTTON = 2
RIGHT_MOUSE_BUTTON = 3
should_return_to_menu = False

# Create the main display surface
DISPLAYSURF = pygame.display.set_mode((game_settings["SCREEN_WIDTH"],
                                       game_settings["SCREEN_HEIGHT"]))
pygame.display.set_caption('Minesweeper')

# First, create instances of Banner and GameBoard
banner = Banner(DISPLAYSURF, game_state_images, pressed_images)
gameboard = GameBoard(DISPLAYSURF, banner, game_settings["ROWS"],
                      game_settings["COLS"], game_settings["MINES"], False)


def draw(gameboard, banner):
    gameboard.draw_board()
    banner.draw_banner()
    banner.draw_counter()
    banner.draw_timer()
    banner.draw_button(gameboard.game_state, banner.button_state)


def get_neighbors(row, col):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_row, new_col = row + i, col + j
            if 0 <= new_row < gameboard.rows and 0 <= new_col < \
                    gameboard.cols:
                neighbors.append((new_row, new_col))
    return neighbors


def handle_quit():
    pygame.quit()
    sys.exit()


def handle_keydown(event, gameboard):
    global should_return_to_menu
    if event.key == pygame.K_ESCAPE:
        gameboard.game_started = False
        should_return_to_menu = True
        game_menu.resize_menu(game_settings["SCREEN_WIDTH"],
                         game_settings["SCREEN_HEIGHT"])


def handle_mouse_actions(event, gameboard, banner):
    margin_size = game_settings["MARGIN_SIZE"]
    banner_height = game_settings["BANNER_HEIGHT"]
    cell_size = game_settings["CELL_SIZE"]
    rows = gameboard.rows
    cols = gameboard.cols

    col = (event.pos[0] - margin_size) // cell_size
    row = (event.pos[1] - banner_height - margin_size) // cell_size

    in_bounds = 0 <= row < rows and 0 <= col < cols

    if event.button == LEFT_MOUSE_BUTTON:
        if banner.button_rect.collidepoint(event.pos):
            banner.button_state = 'pressed'
            banner.button_clicked = True
            if gameboard.game_over:
                banner.button_img = images['smile_flat']
                return
        else:
            if gameboard.game_over:
                return
            banner.button_state = 'normal'
            banner.button_clicked = False

        if in_bounds and gameboard.game_active:
            if gameboard.flagged[row][col] or gameboard.revealed[row][col]:
                gameboard.game_state = 'smile'
            else:
                gameboard.game_state = 'shock'
            banner.button_img = images[gameboard.game_state]

            if not gameboard.revealed[row][col] and not gameboard.flagged[row][
                col]:
                gameboard.pressed = (row, col)
            else:
                gameboard.pressed = None  # Reset the pressed state

    elif event.button == MIDDLE_MOUSE_BUTTON:
        if in_bounds and gameboard.game_active:
            neighbors = get_neighbors(row, col)
            for neighbor in neighbors:
                n_row, n_col = neighbor
                if not gameboard.revealed[n_row][n_col] and not gameboard.flagged[n_row][n_col]:
                    gameboard.temp_flattened.add((n_row, n_col))
        gameboard.draw_board()

    elif event.button == RIGHT_MOUSE_BUTTON:
        if gameboard.game_over:
            return
        if gameboard.game_active and in_bounds and not gameboard.revealed[row][
            col]:
            gameboard.toggle_flag(row, col)
            banner.update_counter(gameboard.flag_count)


def handle_mouse_button_up(event, gameboard, banner):
    margin_size = game_settings["MARGIN_SIZE"]
    banner_height = game_settings["BANNER_HEIGHT"]
    cell_size = game_settings["CELL_SIZE"]
    rows = gameboard.rows
    cols = gameboard.cols

    col = (event.pos[0] - margin_size) // cell_size
    row = (event.pos[1] - banner_height - margin_size) // cell_size

    if event.button == LEFT_MOUSE_BUTTON:
        banner.button_state = 'normal'

        if banner.button_rect.collidepoint(
                event.pos) and banner.button_clicked:
            gameboard.reset_game(gameboard.rows, gameboard.cols,
                                 gameboard.mines)
            banner.button_img = images[gameboard.game_state]

        else:
            if gameboard.game_over:
                banner.button_img = images['sad']
                return

            if 0 <= row < rows and 0 <= col < cols:
                if gameboard.first_click and not gameboard.flagged[row][col]:
                    gameboard.first_click = False
                    gameboard.game_started = True
                    gameboard.start_ticks = pygame.time.get_ticks()
                    gameboard.generate_board_except(row, col)
                    gameboard.reveal_cell(row, col)

                gameboard.game_state = 'smile'
                banner.button_img = images[gameboard.game_state]

                if gameboard.game_active and not gameboard.flagged[row][col]:
                    gameboard.reveal_cell(row, col)  # Handle cell revealing

            banner.button_clicked = False
            gameboard.pressed = None  # Reset the pressed state

    elif event.button == MIDDLE_MOUSE_BUTTON:
        gameboard.temp_flattened.clear()  # Clear the temp_flattened set
        gameboard.draw_board()


def handle_mouse_motion(event, gameboard, banner):
    margin_size = game_settings["MARGIN_SIZE"]
    banner_height = game_settings["BANNER_HEIGHT"]
    cell_size = game_settings["CELL_SIZE"]
    rows = gameboard.rows
    cols = gameboard.cols

    col = (event.pos[0] - margin_size) // cell_size
    row = (event.pos[1] - banner_height - margin_size) // cell_size

    in_bounds = 0 <= row < rows and 0 <= col < cols
    outside_grid = row < 0 or row >= rows or col < 0 or col >= cols
    over_grid = 0 <= row < rows and 0 <= col < cols
    left_button_pressed = pygame.mouse.get_pressed()[0]

    def update_state_and_image(new_state):
        if gameboard.game_state != new_state:
            gameboard.game_state = new_state
            banner.button_img = images[new_state]

    if gameboard.game_over:
        if banner.button_rect.collidepoint(event.pos):
            if left_button_pressed:
                if banner.button_state == 'pressed':
                    banner.button_img = images['smile']
                else:
                    banner.button_state = 'pressed'
                    banner.button_img = images['smile_flat']
            else:
                banner.button_state = 'normal'
                banner.button_img = images['sad']
        else:
            if left_button_pressed and banner.button_state == 'pressed':
                banner.button_state = 'normal'
                banner.button_img = images['sad']
        return

    if outside_grid and gameboard.game_state != 'smile':
        update_state_and_image('smile')

    elif over_grid and left_button_pressed:
        if gameboard.flagged[row][col] or gameboard.revealed[row][col]:
            update_state_and_image('smile')
        elif not gameboard.revealed[row][col]:
            update_state_and_image('shock')

    if left_button_pressed:
        if banner.button_rect.collidepoint(event.pos):
            banner.button_state = 'pressed'
            banner.button_img = images['smile_flat']
        else:
            if banner.button_state == 'pressed':
                banner.button_state = 'normal'
                banner.button_img = images[gameboard.game_state]

        if over_grid and not gameboard.flagged[row][col] and not gameboard.revealed[row][col]:
            gameboard.pressed = (row, col)
        else:
            gameboard.pressed = None

    middle_button_pressed = pygame.mouse.get_pressed()[1]

    if middle_button_pressed:
        gameboard.temp_flattened.clear()

        if in_bounds:
            neighbors = get_neighbors(row, col)
            for neighbor in neighbors:
                n_row, n_col = neighbor
                if not gameboard.revealed[n_row][n_col] and not gameboard.flagged[n_row][n_col]:
                    gameboard.temp_flattened.add((n_row, n_col))
        gameboard.draw_board()


def handle_events(gameboard, banner):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            handle_quit()

        elif event.type == pygame.KEYDOWN:
            handle_keydown(event, gameboard)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_actions(event, gameboard, banner)

        elif event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_button_up(event, gameboard, banner)

        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(event, gameboard, banner)


# game loop
def game_loop(gameboard, banner):
    global should_return_to_menu
    while True:
        # handle events
        handle_events(gameboard, banner)

        if gameboard.game_started and not gameboard.game_over:
            if gameboard.start_ticks is not None:
                elapsed_time = pygame.time.get_ticks() - gameboard.start_ticks
                seconds = min((elapsed_time // 1000), 999)
                banner.timer = seconds

                # Check if the timer has reached 999 seconds
                if seconds == 999:
                    gameboard.game_over = True  # Set game_over to True
                    gameboard.game_state = 'sad'

                # Update the display of the timer
                banner.draw_timer()

        if should_return_to_menu:
            should_return_to_menu = False  # reset the flag for future calls
            break

        draw(gameboard, banner)


# create an instance of your GameMenu with the created instances of
# GameBoard and Banner
game_menu = GameMenu(DISPLAYSURF, game_loop, draw, gameboard, banner)

game_menu.run()
