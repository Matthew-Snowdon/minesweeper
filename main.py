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

# Create instances of Banner and GameBoard
banner = Banner(DISPLAYSURF, game_state_images, pressed_images)
gameboard = GameBoard(DISPLAYSURF, banner, game_settings["ROWS"],
                      game_settings["COLS"], game_settings["MINES"], False)


def draw(gameboard, banner):
    """
        This function handles the drawing of various components on the screen
        including the game board, banner, counter, timer, and the reset button.
        It is called every frame to update the visual elements based on the
        current state of the game.

        Parameters:
        gameboard (object): The gameboard object representing the current state
                            of the game including cells, mines, flags, etc.
        banner (object): The banner object responsible for drawing and updating
                         the banner area which includes the counter, timer, and
                         the reset button.

        """
    gameboard.draw_board()
    banner.draw_banner()
    banner.draw_counter()
    banner.draw_timer()
    banner.draw_button(gameboard.game_state, banner.button_state)


def get_neighbors(row, col):
    """
        This function calculates the coordinates of the neighboring cells
        of a given cell in a grid. It considers all the 8 cells surrounding
        a given cell (row, col) including diagonal neighbors. The function
        ensures that the neighboring cells are within the bounds of the
        gameboard before adding them to the list of neighbors.

        Parameters: row (int): The row index of the cell whose neighbors are
        to be found. col (int): The column index of the cell whose neighbors
        are to be found.

        Returns: list: A list of tuples representing the coordinates of the
        neighboring cells.
    """
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_row, new_col = row + i, col + j
            if 0 <= new_row < gameboard.rows and 0 <= new_col < \
                    gameboard.cols:
                neighbors.append((new_row, new_col))
    return neighbors


def handle_quit():
    """
        This function handles the termination of the game. It first calls
        pygame.quit() to uninitialize all pygame modules, and then calls
        sys.exit() to exit Python and close the game window.
        """
    pygame.quit()
    sys.exit()


def handle_keydown(event, gameboard):
    """
    Handles the keydown events in the game. If the 'ESCAPE' key is pressed,
    it stops the game and flags it to return to the main menu, also resizing
    the game menu to the specified screen width and height.

        Parameters: event (pygame.event.Event): The event object
        representing a key press. gameboard (GameBoard): The gameboard
        object where the game state is managed.

        Global variables: should_return_to_menu (bool): Flag to indicate if
        the game should return to the main menu. game_settings (dict): A
        dictionary holding various game settings, like screen dimensions.
        game_menu (GameMenu): The game menu object to be resized.
    """
    global should_return_to_menu
    if event.key == pygame.K_ESCAPE:
        gameboard.game_started = False
        should_return_to_menu = True


def handle_mouse_actions(event, gameboard, banner):
    """
    Handles mouse actions (clicks) within the game. Depending on the mouse
    button pressed (left, middle, or right), it performs various actions
    like revealing cells, flattening neighbouring cells, or toggling flags.
    It also updates the banner state and button images accordingly.

        Parameters: event (pygame.event.Event): The event object
        representing a mouse action. gameboard (GameBoard): The gameboard
        object where the game state is managed. banner (Banner): The banner
        object that holds the state and assets for the banner display.

        Global variables: game_settings (dict): A dictionary holding various
        game settings like margin size, banner height, and cell size. images
        (dict): A dictionary holding the various image assets used in the
        game. LEFT_MOUSE_BUTTON (int): The constant representing the left
        mouse button. MIDDLE_MOUSE_BUTTON (int): The constant representing
        the middle mouse button. RIGHT_MOUSE_BUTTON (int): The constant
        representing the right mouse button.
    """
    margin_size = game_settings["MARGIN_SIZE"]
    banner_height = game_settings["BANNER_HEIGHT"]
    cell_size = game_settings["CELL_SIZE"]
    rows = gameboard.rows
    cols = gameboard.cols

    col = (event.pos[0] - margin_size) // cell_size
    row = (event.pos[1] - banner_height - margin_size) // cell_size

    in_bounds = 0 <= row < rows and 0 <= col < cols

    if event.button == LEFT_MOUSE_BUTTON:
        # Handling left mouse button actions, mainly involving revealing cells
        # and updating the banner/button states.
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
                gameboard.pressed = None

    elif event.button == MIDDLE_MOUSE_BUTTON:
        # Handling middle mouse button actions, used for flattening
        # neighbouring cells temporarily.
        if in_bounds and gameboard.game_active:
            neighbors = get_neighbors(row, col)
            for neighbor in neighbors:
                n_row, n_col = neighbor
                if not gameboard.revealed[n_row][
                    n_col] and not gameboard.flagged[n_row][n_col]:
                    gameboard.temp_flattened.add((n_row, n_col))
        gameboard.draw_board()

    elif event.button == RIGHT_MOUSE_BUTTON:
        # Handling right mouse button actions, primarily for toggling cell
        # flags and updating the mine counter.
        if gameboard.game_over:
            return
        if gameboard.game_active and in_bounds and not gameboard.revealed[row][
            col]:
            gameboard.toggle_flag(row, col)
            banner.update_counter(gameboard.flag_count)


def handle_mouse_button_up(event, gameboard, banner):
    """
    This function is triggered when a mouse button is released. Depending on
    the mouse button that was pressed (left or middle), it executes
    different actions like resetting the game, revealing cells, updating the
    game state, etc. It also resets certain attributes like the button state
    and the first click status.

        Parameters: event (pygame.event.Event): The event object
        representing a mouse button release action. gameboard (GameBoard):
        The gameboard object where the game state is managed. banner (
        Banner): The banner object that holds the state and assets for the
        banner display.

        Global variables: game_settings (dict): A dictionary holding various
        game settings like margin size, banner height, and cell size. images
        (dict): A dictionary holding the various image assets used in the
        game. LEFT_MOUSE_BUTTON (int): The constant representing the left
        mouse button. MIDDLE_MOUSE_BUTTON (int): The constant representing
        the middle mouse button.
    """
    # Getting necessary settings and properties
    margin_size = game_settings["MARGIN_SIZE"]
    banner_height = game_settings["BANNER_HEIGHT"]
    cell_size = game_settings["CELL_SIZE"]
    rows = gameboard.rows
    cols = gameboard.cols

    # Calculating the cell coordinates based on the mouse position
    col = (event.pos[0] - margin_size) // cell_size
    row = (event.pos[1] - banner_height - margin_size) // cell_size

    if event.button == LEFT_MOUSE_BUTTON:
        banner.button_state = 'normal'

        # Check if the button in the banner was clicked
        if banner.button_rect.collidepoint(
                event.pos) and banner.button_clicked:
            # Reset the game and update the banner image
            gameboard.reset_game(gameboard.rows, gameboard.cols,
                                 gameboard.mines)
            banner.button_img = images[gameboard.game_state]
        else:
            if gameboard.game_over:
                banner.button_img = images['sad']
                return

            # Check if the click is within the valid game board area
            if 0 <= row < rows and 0 <= col < cols:
                # Handling the first click differently to initialize the game
                if gameboard.first_click and not gameboard.flagged[row][col]:
                    gameboard.first_click = False
                    gameboard.game_started = True
                    gameboard.start_ticks = pygame.time.get_ticks()
                    gameboard.generate_board_except(row, col)
                    gameboard.reveal_cell(row, col)

                # Update the game state and banner image
                gameboard.game_state = 'smile'
                banner.button_img = images[gameboard.game_state]

                # Reveal the cell if it is not flagged and the game is active
                if gameboard.game_active and not gameboard.flagged[row][col]:
                    gameboard.reveal_cell(row, col)

            # Reset the button clicked state
            banner.button_clicked = False
            gameboard.pressed = None  # Reset the pressed cell state

    elif event.button == MIDDLE_MOUSE_BUTTON:
        # Clear the temporary flattened set and redraw the board
        gameboard.temp_flattened.clear()
        gameboard.draw_board()


def handle_mouse_motion(event, gameboard, banner):
    """
    This function is triggered when a mouse motion event occurs. It manages
    changes in the game state and updates the images and states of elements
    based on the mouse position and button states.

        Parameters: - event (pygame.event.Event): The event object
        representing a mouse motion action. - gameboard (GameBoard): The
        gameboard object managing the game state. - banner (Banner): The
        banner object holding the state and assets for the banner display.

        Global Variables: - game_settings (dict): A dictionary holding
        various game settings like margin size, banner height, and cell
        size. - images (dict): A dictionary holding the various image assets
        used in the game.
    """
    # Getting necessary settings and properties
    margin_size = game_settings["MARGIN_SIZE"]
    banner_height = game_settings["BANNER_HEIGHT"]
    cell_size = game_settings["CELL_SIZE"]
    rows = gameboard.rows
    cols = gameboard.cols

    # Calculating the cell coordinates based on the mouse position
    col = (event.pos[0] - margin_size) // cell_size
    row = (event.pos[1] - banner_height - margin_size) // cell_size

    # Check if the mouse is within bounds or outside the grid or over the grid
    in_bounds = 0 <= row < rows and 0 <= col < cols
    outside_grid = row < 0 or row >= rows or col < 0 or col >= cols
    over_grid = 0 <= row < rows and 0 <= col < cols
    left_button_pressed = pygame.mouse.get_pressed()[0]

    def update_state_and_image(new_state):
        """Updates the game state and banner image based on the new state."""
        if gameboard.game_state != new_state:
            gameboard.game_state = new_state
            banner.button_img = images[new_state]

    # Handle the game over state
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

    # Handling the left button pressed state
    if left_button_pressed:
        if banner.button_rect.collidepoint(event.pos):
            banner.button_state = 'pressed'
            banner.button_img = images['smile_flat']
        else:
            if banner.button_state == 'pressed':
                banner.button_state = 'normal'
                banner.button_img = images[gameboard.game_state]

        if over_grid and not gameboard.flagged[row][
            col] and not gameboard.revealed[row][col]:
            gameboard.pressed = (row, col)
        else:
            gameboard.pressed = None

    # Handling the middle button pressed state
    middle_button_pressed = pygame.mouse.get_pressed()[1]

    if middle_button_pressed:
        gameboard.temp_flattened.clear()

        if in_bounds:
            neighbors = get_neighbors(row, col)
            for neighbor in neighbors:
                n_row, n_col = neighbor
                if not gameboard.revealed[n_row][
                    n_col] and not gameboard.flagged[n_row][n_col]:
                    gameboard.temp_flattened.add((n_row, n_col))
        gameboard.draw_board()


def handle_events(gameboard, banner):
    """
    This function is the main event handler in the game. It retrieves all
    pending events from the pygame event queue and handles them accordingly,
    calling the appropriate functions to deal with quit events, key presses,
    and mouse actions (button down, button up, and motion).

        Parameters: gameboard (GameBoard): The gameboard object where the
        game state is managed. banner (Banner): The banner object that holds
        the state and assets for the banner display.
    """
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
    """
    This is the main loop of the game that keeps running infinitely to
    manage the game flow. It handles game events, updates the timer on the
    banner, checks if the time limit is reached, and updates the game and
    banner displays accordingly. If the global flag `should_return_to_menu`
    is set to True, it resets the flag and breaks the loop, effectively
    returning to the menu.

        Parameters: gameboard (GameBoard): The gameboard object where the
        game state is managed. banner (Banner): The banner object that holds
        the state and assets for the banner display.

        Global variables: should_return_to_menu (bool): A flag that
        indicates whether the game should return to the menu.
    """
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
