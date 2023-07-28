import sys
from gameboard import GameBoard
from banner import Banner
from menu import GameMenu
from utilities import *


def draw(gboard, _banner):
    gboard.draw_board()
    _banner.draw_banner()
    _banner.draw_counter()
    _banner.draw_timer()
    _banner.draw_button(gameboard.game_state, banner.button_state)


# initialize Pygame
pygame.init()

# initialize game state
game_started = False
game_state = 'smile'
game_over = False
first_click = True
button_state = 'normal'
button_clicked = False
cell_clicked = False
button_img = images['smile']

# Create the main display surface
DISPLAYSURF = pygame.display.set_mode((game_settings["SCREEN_WIDTH"],
                                       game_settings["SCREEN_HEIGHT"]))
pygame.display.set_caption('Minesweeper')

# Initialize the start time
start_ticks = pygame.time.get_ticks()

# Create an instance of your GameBoard and Banner classes
banner = Banner(DISPLAYSURF, game_state_images, pressed_images)
gameboard = GameBoard(DISPLAYSURF, banner, game_settings["ROWS"],
                      game_settings["COLS"], game_settings["MINES"],
                      game_started)


gameboard.reset_game()


# game loop
def game_loop(gameboard, banner):
    global button_state, button_clicked, cell_clicked, button_img, \
        game_state, game_over, first_click, start_ticks

    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # The escape key was pressed
                    global game_started
                    game_started = False
                    game_menu.run()  # Show the menu

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if banner.button_rect.collidepoint(event.pos):
                        button_state = 'pressed'
                        button_clicked = True
                        if game_over:
                            button_img = images['sad_flat']
                            pygame.draw.rect(DISPLAYSURF, BLACK,
                                             banner.button_rect)
                            DISPLAYSURF.blit(button_img,
                                             banner.button_rect.topleft)
                            pygame.display.update()
                    else:
                        button_state = 'normal'
                        button_clicked = False

                if game_over:  # Don't handle any more mouse presses if the
                    # game
                    continue

                col = event.pos[0] // game_settings["CELL_SIZE"]
                row = ((event.pos[1] - game_settings["BANNER_HEIGHT"]) //
                       game_settings["CELL_SIZE"])

                if row < 0 or row >= game_settings["ROWS"] or col < 0 or \
                        col >= game_settings["COLS"]:
                    cell_clicked = True
                elif gameboard.game_active and pygame.mouse.get_pressed()[0]:
                    game_state = 'shock'
                    button_img = images[game_state]
                    if gameboard.flagged[row][col]:  # The cell is flagged
                        pass  # Do nothing when left-clicking a flagged cell
                    elif not gameboard.revealed[row][
                        col]:  # Cell isn't revealed
                        pressed = (row, col)
                elif event.button == 3 and gameboard.game_active:
                    col = event.pos[0] // game_settings["CELL_SIZE"]
                    row = ((event.pos[1] - game_settings["BANNER_HEIGHT"]) //
                           game_settings["CELL_SIZE"])
                    if row < 0 or row >= game_settings["ROWS"] or col < 0 or \
                            col >= game_settings["COLS"]:
                        continue
                    if not gameboard.revealed[row][
                        col]:  # Right-click and cell
                        gameboard.toggle_flag(row,
                                              col)  # Handle flag placement

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    button_state = 'normal'
                    if banner.button_rect.collidepoint(
                            event.pos) and button_clicked:
                        gameboard.reset_game()  # Reset the game when button is
                        game_state = 'smile'  # Reset the game state
                        button_img = images[game_state]
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(button_img,
                                         banner.button_rect.topleft)
                        pygame.display.update()
                    elif game_over:
                        button_img = images['sad']
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(button_img,
                                         banner.button_rect.topleft)
                        pygame.display.update()
                    else:
                        game_state = 'smile'
                        button_img = images[game_state]
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(button_img,
                                         banner.button_rect.topleft)
                        pygame.display.update()

                    button_clicked = False

                if game_over:  # Don't handle any more mouse presses if the
                    # game
                    continue

                col = event.pos[0] // game_settings["CELL_SIZE"]
                row = ((event.pos[1] - game_settings["BANNER_HEIGHT"]) //
                       game_settings["CELL_SIZE"])
                if row < 0 or row >= game_settings["ROWS"] or col < 0 or \
                        col >= game_settings["COLS"]:
                    continue

                if gameboard.game_active and event.button == 1 \
                        and not gameboard.flagged[row][col]:
                    game_state = 'smile'
                    button_img = images[game_state]
                    if first_click:
                        first_click = False
                        gameboard.generate_board_except(row, col)
                    gameboard.reveal_cell(row, col)  # Handle cell revealing

                pressed = None  # Reset the pressed state

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if banner.button_rect.collidepoint(event.pos):
                        if game_over:
                            button_img = images['sad_flat']
                        else:
                            if button_state != 'pressed':
                                if game_state == 'winner':
                                    button_img = pressed_images[game_state]
                                else:
                                    button_img = images['smile_flat']
                                button_state = 'pressed'
                    else:
                        if game_over:
                            button_img = images['sad']
                        else:
                            if button_state == 'pressed':
                                button_state = 'normal'
                                button_img = images[game_state]
                    pygame.draw.rect(DISPLAYSURF, BLACK, banner.button_rect)
                    DISPLAYSURF.blit(button_img, banner.button_rect.topleft)
                    pygame.display.update()
                    col = event.pos[0] // game_settings["CELL_SIZE"]
                    row = ((event.pos[1] - game_settings["BANNER_HEIGHT"]) //
                           game_settings["CELL_SIZE"])
                    if 0 <= row < game_settings["ROWS"] and 0 <= col < \
                            game_settings["COLS"] and not \
                            gameboard.flagged[row][col] and not \
                            gameboard.revealed[row][col]:
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
            for (mine_row, mine_col) in gameboard.mines:
                mine_rect = gameboard.get_cell_rect(mine_row, mine_col)
                if (mine_row, mine_col) == gameboard.game_over_mine:
                    DISPLAYSURF.blit(images['red_mine'], mine_rect)
                elif gameboard.flagged[mine_row][mine_col]:  # the mines that
                    DISPLAYSURF.blit(images['cross_mine'], mine_rect)
                else:  # all other mines
                    DISPLAYSURF.blit(images['mine'], mine_rect)
            pygame.display.update()  # Update the game board after revealing
            # all
            continue  # Don't handle any more game logic after game over

        # Call the draw function
        draw(gameboard, banner)

        # draw pressed state
        if gameboard.pressed is not None:
            rect = gameboard.get_cell_rect(*gameboard.pressed)
            DISPLAYSURF.blit(images['flat'], rect)

        # Update the display
        pygame.display.update()


# game_loop(gameboard, banner)
game_menu = GameMenu(DISPLAYSURF, game_loop, draw)
game_menu.run()
