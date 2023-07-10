import pygame
import random
import sys

# game settings
SCREEN_WIDTH = 600
BANNER_HEIGHT = 100
SCREEN_HEIGHT = 600 + BANNER_HEIGHT
ROWS = 10
COLS = 10
MINES = 15
CELL_SIZE = SCREEN_WIDTH // COLS
# Button dimensions
BUTTON_WIDTH = CELL_SIZE * 1.2
BUTTON_HEIGHT = CELL_SIZE * 1.2

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (227, 227, 227)
GRAY = (179, 179, 179)
DARK_GRAY = (127, 127, 127)
RED = (255, 0, 0)

# initialize Pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minesweeper')

# Initialize the start time
start_ticks = pygame.time.get_ticks()

# load game assets
game_font = pygame.font.Font('digital7.ttf', 70)

tile_image = pygame.image.load('tile.png')
tile_image = pygame.transform.scale(tile_image, (CELL_SIZE, CELL_SIZE))

mine_image = pygame.image.load('mine.png')
mine_image = pygame.transform.scale(mine_image, (CELL_SIZE, CELL_SIZE))

red_mine_image = pygame.image.load('red_mine.png')
red_mine_image = pygame.transform.scale(red_mine_image, (CELL_SIZE, CELL_SIZE))

cross_mine_image = pygame.image.load('cross_mine.png')
cross_mine_image = pygame.transform.scale(cross_mine_image,
                                          (CELL_SIZE, CELL_SIZE))

question_image = pygame.image.load('question.png')
question_image = pygame.transform.scale(question_image, (CELL_SIZE, CELL_SIZE))

flag_image = pygame.image.load('flag.png')
flag_image = pygame.transform.scale(flag_image, (CELL_SIZE, CELL_SIZE))

flat_image = pygame.image.load('flat.png')
flat_image = pygame.transform.scale(flat_image, (CELL_SIZE, CELL_SIZE))

pressed_image = pygame.image.load('flat.png')
pressed_image = pygame.transform.scale(pressed_image, (CELL_SIZE, CELL_SIZE))

one_image = pygame.image.load('1.png')
one_image = pygame.transform.scale(one_image, (CELL_SIZE, CELL_SIZE))

two_image = pygame.image.load('2.png')
two_image = pygame.transform.scale(two_image, (CELL_SIZE, CELL_SIZE))

three_image = pygame.image.load('3.png')
three_image = pygame.transform.scale(three_image, (CELL_SIZE, CELL_SIZE))

four_image = pygame.image.load('4.png')
four_image = pygame.transform.scale(four_image, (CELL_SIZE, CELL_SIZE))

five_image = pygame.image.load('5.png')
five_image = pygame.transform.scale(five_image, (CELL_SIZE, CELL_SIZE))

smile_img = pygame.image.load('smile.png')
smile_img = pygame.transform.scale(smile_img,
                                   (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
smile_flat = pygame.image.load('smile_flat.png')
smile_flat = pygame.transform.scale(smile_flat,
                                    (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
shock_img = pygame.image.load('shock.png')
shock_img = pygame.transform.scale(shock_img,
                                   (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
sad_img = pygame.image.load('sad.png')
sad_img = pygame.transform.scale(sad_img,
                                 (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
sad_flat = pygame.image.load('sad_flat.png')
sad_flat = pygame.transform.scale(sad_flat,
                                  (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
winner_img = pygame.image.load('winner.png')
winner_img = pygame.transform.scale(winner_img,
                                    (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
winner_flat = pygame.image.load('winner_flat.png')
winner_flat = pygame.transform.scale(winner_flat,
                                     (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))

# initialize game state
game_state = 'smile'  # This would be updated based on the state of the game
revealed = [[False for row in range(ROWS)] for col in range(COLS)]
flagged = [[False for row in range(ROWS)] for col in range(COLS)]
questioned = [[False for row in range(ROWS)] for col in range(COLS)]
first_mine_revealed = False  # Flag to track the first mine revealed
game_over = False
game_over_mine = None  # The location of the mine that ended the game
game_active = True  # The game is active and the board can be changed
pressed = None  # Cell which is pressed but not released yet
first_click = True
board = []  # This initializes board as an empty list
mines = []  # Store the coordinates of mines
flag_count = MINES
button_state = 'normal'
button_clicked = False
cell_clicked = False

# Create a dictionary to map game state to images
images = {'smile': smile_img, 'shock': shock_img, 'sad': sad_img,
          'winner': winner_img}

pressed_images = {'smile': smile_flat, 'winner': winner_flat,
                  'sad': sad_flat, 'shock': shock_img}


# define game functions
def generate_board_except(row, col):
    global board, mines  # Access to the global variables
    board = [['-' for col in range(COLS)] for row in range(ROWS)]
    mines = []  # Reset mines
    for i in range(MINES):
        mine_row, mine_col = random.randint(0, ROWS - 1), \
                             random.randint(0, COLS - 1)
        while board[mine_row][mine_col] == '#' or \
                (mine_row == row and mine_col == col):
            mine_row, mine_col = random.randint(0, ROWS - 1), \
                                 random.randint(0, COLS - 1)
        board[mine_row][mine_col] = '#'
        mines.append((mine_row, mine_col))  # Store mine coordinates

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != '#':
                count = 0
                for row_offset in range(-1, 2):
                    for col_offset in range(-1, 2):
                        if (0 <= row + row_offset < ROWS) and \
                                (0 <= col + col_offset < COLS):
                            if board[row + row_offset][col + col_offset] \
                                    == '#':
                                count += 1
                board[row][col] = str(count)


def toggle_flag(row, col):
    global flag_count
    if flag_count == 0 and not flagged[row][col]:
        return
    # If it's not flagged or questioned, flag it
    if not flagged[row][col] and not questioned[row][col]:
        flagged[row][col] = True
        flag_count -= 1  # Decrease the flag count
    # If it's flagged, question it and unflag
    elif flagged[row][col] and not questioned[row][col]:
        flagged[row][col] = False
        questioned[row][col] = True
        flag_count += 1  # Increase the flag count
    # If it's questioned, reset it
    elif not flagged[row][col] and questioned[row][col]:
        questioned[row][col] = False
    # Ensure flag_count doesn't go into negative
    flag_count = max(0, flag_count)


def get_cell_rect(row, col):
    return pygame.Rect(col * CELL_SIZE, BANNER_HEIGHT + row *
                       CELL_SIZE, CELL_SIZE, CELL_SIZE)


def draw_board(game_board):
    for row in range(ROWS):
        for col in range(COLS):
            rect = get_cell_rect(row, col)
            if revealed[row][col]:
                cell_content = board[row][col]
                if cell_content == '#':
                    if game_over and (row, col) == game_over_mine:
                        DISPLAYSURF.blit(red_mine_image, rect)
                    else:
                        DISPLAYSURF.blit(mine_image, rect)
                elif cell_content == '0':
                    DISPLAYSURF.blit(flat_image, rect)
                elif cell_content == '1':
                    DISPLAYSURF.blit(one_image, rect)
                elif cell_content == '2':
                    DISPLAYSURF.blit(two_image, rect)
                elif cell_content == '3':
                    DISPLAYSURF.blit(three_image, rect)
                elif cell_content == '4':
                    DISPLAYSURF.blit(four_image, rect)
                elif cell_content == '5':
                    DISPLAYSURF.blit(five_image, rect)
            elif flagged[row][col]:
                DISPLAYSURF.blit(flag_image, rect)
            elif questioned[row][col]:
                DISPLAYSURF.blit(question_image, rect)
            else:
                DISPLAYSURF.blit(tile_image, rect)

            pygame.draw.rect(DISPLAYSURF, DARK_GRAY, rect, 1)


def reveal_cell(row, col):
    global game_over, game_over_mine, game_active, game_state, button_img
    if not revealed[row][col] and not flagged[row][col]:
        revealed[row][col] = True
        if board[row][col] == '#':
            game_over = True
            game_active = False
            game_state = 'sad'
            button_img = images[game_state]
            pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
            DISPLAYSURF.blit(button_img, button_rect.topleft)
            pygame.display.update()  # Update the display
            game_over_mine = (row, col)
            print("Game Over!")
        elif board[row][col] == '0':
            for row_offset in range(-1, 2):
                for col_offset in range(-1, 2):
                    if (0 <= row + row_offset < ROWS) and (
                            0 <= col + col_offset < COLS):
                        reveal_cell(row + row_offset, col + col_offset)
        check_game_won()  # Check if the game is won after revealing a cell


def reset_game():
    global start_ticks, flag_count, game_active, game_over, first_click, \
        revealed, flagged, questioned, game_state, button_img, pressed
    start_ticks = pygame.time.get_ticks()
    flag_count = MINES
    game_active = True
    game_over = False
    first_click = True
    game_state = 'smile'
    button_img = images[game_state]
    pressed = None
    revealed = [[False for _ in range(ROWS)] for _ in range(COLS)]
    flagged = [[False for _ in range(ROWS)] for _ in range(COLS)]
    questioned = [[False for _ in range(ROWS)] for _ in range(COLS)]
    generate_board_except(-1, -1)  # Pass invalid row and col to generate
    # the board


def check_game_won():
    global game_over, game_active, game_state, button_img
    if not game_over and game_active:
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] != '#' and not revealed[row][col]:
                    return
        game_over = True
        game_active = False
        game_state = 'winner'
        button_img = images[game_state]
        pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
        DISPLAYSURF.blit(button_img, button_rect.topleft)
        print("Congratulations! You won!")
        # Draw the game board with revealed cells
        draw_board(board)
        # Update the display
        pygame.display.update()


reset_game()

# game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_rect.collidepoint(event.pos):
                    button_state = 'pressed'
                    button_clicked = True
                    if game_over:
                        button_img = sad_flat
                        pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
                        DISPLAYSURF.blit(button_img, button_rect.topleft)
                        pygame.display.update()
                else:
                    button_state = 'normal'
                    button_clicked = False

            if game_over:  # Don't handle any more mouse presses if the game
                # is over
                continue

            col = event.pos[0] // CELL_SIZE
            row = (event.pos[1] - BANNER_HEIGHT) // CELL_SIZE

            if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                cell_clicked = True
            elif game_active and pygame.mouse.get_pressed()[0]:
                game_state = 'shock'
                button_img = images[game_state]
                if flagged[row][col]:  # The cell is flagged
                    pass  # Do nothing when left-clicking a flagged cell
                elif not revealed[row][col]:  # The cell isn't revealed
                    pressed = (row, col)
            elif event.button == 3 and game_active:
                col = event.pos[0] // CELL_SIZE
                row = (event.pos[1] - BANNER_HEIGHT) // CELL_SIZE
                if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                    continue
                if not revealed[row][col]:  # Right-click and cell not revealed
                    toggle_flag(row, col)  # Handle flag placement

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_state = 'normal'
                if button_rect.collidepoint(event.pos) and button_clicked:
                    reset_game()  # Reset the game when button is released
                    game_state = 'smile'  # Reset the game state
                    button_img = images[game_state]
                    pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
                    DISPLAYSURF.blit(button_img, button_rect.topleft)
                    pygame.display.update()
                elif game_over:
                    button_img = sad_img
                    pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
                    DISPLAYSURF.blit(button_img, button_rect.topleft)
                    pygame.display.update()
                else:
                    game_state = 'smile'
                    button_img = images[game_state]
                    pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
                    DISPLAYSURF.blit(button_img, button_rect.topleft)
                    pygame.display.update()

                button_clicked = False

            if game_over:  # Don't handle any more mouse presses if the game
                # is over
                continue

            col = event.pos[0] // CELL_SIZE
            row = (event.pos[1] - BANNER_HEIGHT) // CELL_SIZE
            if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                continue

            if game_active and event.button == 1 and not flagged[row][col]:
                game_state = 'smile'
                button_img = images[game_state]
                if first_click:
                    first_click = False
                    generate_board_except(row, col)
                reveal_cell(row, col)  # Handle cell revealing

            pressed = None  # Reset the pressed state

        elif event.type == pygame.MOUSEMOTION:
            # Check if left mouse button is still down
            if pygame.mouse.get_pressed()[0]:
                if button_rect.collidepoint(event.pos):
                    # Mouse is inside the button area
                    if game_over:
                        button_img = sad_flat
                    else:
                        # Your existing logic when the game isn't over
                        if button_state != 'pressed':
                            if game_state == 'winner':
                                button_img = pressed_images[game_state]
                            else:
                                button_img = smile_flat
                            button_state = 'pressed'
                else:
                    # Mouse moved out of the button area
                    if game_over:
                        button_img = sad_img
                    else:
                        # Your existing logic when the game isn't over
                        if button_state == 'pressed':
                            button_state = 'normal'
                            button_img = images[game_state]
                pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
                DISPLAYSURF.blit(button_img, button_rect.topleft)
                pygame.display.update()
                col = event.pos[0] // CELL_SIZE
                row = (event.pos[1] - BANNER_HEIGHT) // CELL_SIZE
                # Add a boundary check to avoid going off the grid
                if 0 <= row < ROWS and 0 <= col < COLS and not \
                        flagged[row][col] and not revealed[row][col]:
                    pressed = (row, col)
                else:
                    pressed = None

    elapsed_time = pygame.time.get_ticks() - start_ticks
    seconds = min((elapsed_time // 1000), 999)

    # Check if the timer has reached 999 seconds
    if seconds == 999:
        game_over = True  # Set game_over to True

    # Check for game over
    if game_over:
        # if game over, draw all mines
        for (mine_row, mine_col) in mines:
            mine_rect = get_cell_rect(mine_row, mine_col)
            # the mine that was clicked
            if (mine_row, mine_col) == game_over_mine:
                DISPLAYSURF.blit(red_mine_image, mine_rect)
            elif flagged[mine_row][mine_col]:  # the mines that were flagged
                DISPLAYSURF.blit(cross_mine_image, mine_rect)
            else:  # all other mines
                DISPLAYSURF.blit(mine_image, mine_rect)
        pygame.display.update()  # Update the game board after revealing all
        # mines
        continue  # Don't handle any more game logic after game over

    # draw banner
    pygame.draw.rect(DISPLAYSURF, (179, 179, 179),
                     pygame.Rect(0, 0, SCREEN_WIDTH, BANNER_HEIGHT))

    # draw the game board with revealed cells
    draw_board(board)

    # draw pressed state
    if pressed is not None:
        rect = get_cell_rect(*pressed)
        DISPLAYSURF.blit(pressed_image, rect)

    # create timer text
    timer_text = game_font.render(f'{seconds:03}', True, RED)

    # get the width and height of the timer text
    text_width, text_height = timer_text.get_size()

    # calculate the top left position of the timer
    # Subtract 10 for a small right margin
    timer_pos = (SCREEN_WIDTH - text_width - 10,
                 BANNER_HEIGHT / 2 - text_height / 2)

    # get the rectangle of the timer text
    timer_rect = timer_text.get_rect(topleft=timer_pos)

    # create "888" text with 30% opacity
    under_text_surface = game_font.render('888', True, RED)
    under_text_surface.set_alpha(76)  # 30% opacity

    # get the rectangle of the "888" text
    under_text_rect = under_text_surface.get_rect(topleft=timer_pos)

    # create a background rectangle for the timer with the dimensions of "888"
    pygame.draw.rect(DISPLAYSURF, BLACK, under_text_rect)

    # blit the "888" text
    DISPLAYSURF.blit(under_text_surface, under_text_rect.topleft)

    # blit the timer text
    DISPLAYSURF.blit(timer_text, timer_rect.topleft)

    # create counter text
    counter = flag_count
    counter_text = game_font.render(f'{counter:03}', True, RED)

    # get the width and height of the counter text
    counter_width, counter_height = counter_text.get_size()

    # calculate the top left position of the counter
    counter_pos = (10,
                   BANNER_HEIGHT / 2 - counter_height / 2)  # Add 10 for a
    # small left margin

    # get the rectangle of the counter text
    counter_rect = counter_text.get_rect(topleft=counter_pos)

    # create "888" text for counter with 30% opacity
    counter_under_text_surface = game_font.render('888', True, RED)
    counter_under_text_surface.set_alpha(76)  # 30% opacity

    # get the rectangle of the "888" counter text
    counter_under_text_rect = counter_under_text_surface.get_rect(
        topleft=counter_pos)

    # create a background rectangle for the counter with the dimensions of
    # "888"
    pygame.draw.rect(DISPLAYSURF, BLACK, counter_under_text_rect)

    # blit the "888" text for counter
    DISPLAYSURF.blit(counter_under_text_surface,
                     counter_under_text_rect.topleft)

    # blit the counter text
    DISPLAYSURF.blit(counter_text, counter_rect.topleft)

    # Calculate the center position between the timer and the counter
    center_x = (timer_rect.centerx + counter_rect.centerx) // 2
    center_y = (timer_rect.centery + counter_rect.centery) // 2

    # Calculate the top-left position of the button
    button_pos_x = center_x - BUTTON_WIDTH // 2
    button_pos_y = center_y - BUTTON_HEIGHT // 2

    # Create the button rectangle
    button_rect = pygame.Rect(button_pos_x, button_pos_y, BUTTON_WIDTH,
                              BUTTON_HEIGHT)

    # Draw the button with the appropriate image based on the game state
    button_img = images[game_state]
    # Determine the correct button image based on the game state
    if button_state == 'pressed':  # Change the image if the button is pressed
        button_img = pressed_images[game_state]

    pygame.draw.rect(DISPLAYSURF, BLACK, button_rect)
    DISPLAYSURF.blit(button_img, button_rect.topleft)

    # Update the display
    pygame.display.update()
