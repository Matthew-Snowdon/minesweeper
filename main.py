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


# game loop
def game_loop(gameboard, banner):
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # The escape key was pressed
                    game_menu.game_started = False
                    game_menu.run()  # Show the menu

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if banner.button_rect.collidepoint(event.pos):
                        banner.button_state = 'pressed'
                        banner.button_clicked = True
                        if gameboard.game_over:
                            banner.button_img = images['sad_flat']
                            pygame.draw.rect(DISPLAYSURF, BLACK,
                                             banner.button_rect)
                            DISPLAYSURF.blit(banner.button_img,
                                             banner.button_rect.topleft)
                            pygame.display.update()
                    else:
                        banner.button_state = 'normal'
                        banner.button_clicked = False

                if gameboard.game_over:
                    # Don't handle any more mouse presses if the game
                    continue

                col = (event.pos[0] -
                       game_settings["MARGIN_SIZE"]) // game_settings[
                    "CELL_SIZE"]
                row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                        game_settings["MARGIN_SIZE"]) // game_settings[
                           "CELL_SIZE"])

                if row < 0 or row >= game_settings["ROWS"] or col < 0 or \
                        col >= game_settings["COLS"]:
                    gameboard.cell_clicked = True
                elif gameboard.game_active and pygame.mouse.get_pressed()[0]:
                    gameboard.game_state = 'shock'
                    banner.button_img = images[gameboard.game_state]
                    if gameboard.flagged[row][col]:  # The cell is flagged
                        pass  # Do nothing when left-clicking a flagged cell
                    elif not gameboard.revealed[row][
                        col]:  # Cell isn't revealed
                        pressed = (row, col)
                elif event.button == 3 and gameboard.game_active:
                    col = (event.pos[0] - game_settings["MARGIN_SIZE"]) // \
                          game_settings["CELL_SIZE"]
                    row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                            game_settings["MARGIN_SIZE"]) // game_settings[
                               "CELL_SIZE"])

                    if row < 0 or row >= game_settings["ROWS"] or col < 0 or \
                            col >= game_settings["COLS"]:
                        continue
                    if not gameboard.revealed[row][
                        col]:  # Right-click and cell
                        gameboard.toggle_flag(row,
                                              col)  # Handle flag placement

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    banner.button_state = 'normal'
                    if banner.button_rect.collidepoint(
                            event.pos) and banner.button_clicked:
                        gameboard.reset_game()  # Reset the game
                        game_menu.game_started = False  # Don't start the
                        # timer yet
                        gameboard.first_click = False  # Indicate that the
                        # first click hasn't happened
                        gameboard.game_state = 'smile'  # Reset the game state
                        banner.button_img = images[gameboard.game_state]
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(banner.button_img,
                                         banner.button_rect.topleft)
                        pygame.display.update()
                    elif gameboard.game_over:
                        banner.button_img = images['sad']
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(banner.button_img,
                                         banner.button_rect.topleft)
                        pygame.display.update()
                    else:
                        col = (event.pos[0] - game_settings[
                            "MARGIN_SIZE"]) // game_settings["CELL_SIZE"]
                        row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                                game_settings["MARGIN_SIZE"]) // game_settings[
                                   "CELL_SIZE"])

                        if 0 <= row < game_settings["ROWS"] and 0 <= col < \
                                game_settings["COLS"]:
                            if not gameboard.first_click:  # Start the timer
                                # on the first cell click
                                gameboard.first_click = True
                                game_menu.game_started = True
                                gameboard.start_ticks = pygame.time.get_ticks()

                                # Include logic to reveal cell and other
                                # game starting logic if needed
                                gameboard.generate_board_except(row, col)
                                gameboard.reveal_cell(row, col)

                        gameboard.game_state = 'smile'
                        banner.button_img = images[gameboard.game_state]
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(banner.button_img,
                                         banner.button_rect.topleft)
                        pygame.display.update()

                    banner.button_clicked = False

                if gameboard.game_over:  # Don't handle any more mouse
                    # presses if the
                    # game
                    continue

                col = (event.pos[0] - game_settings[
                    "MARGIN_SIZE"]) // game_settings["CELL_SIZE"]
                row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                        game_settings["MARGIN_SIZE"]) // game_settings[
                           "CELL_SIZE"])

                if row < 0 or row >= game_settings["ROWS"] or col < 0 or \
                        col >= game_settings["COLS"]:
                    continue

                if gameboard.game_active and event.button == 1 \
                        and not gameboard.flagged[row][col]:
                    gameboard.game_state = 'smile'
                    banner.button_img = images[gameboard.game_state]
                    if not gameboard.first_click:
                        gameboard.first_click = True
                        gameboard.generate_board_except(row, col)
                    gameboard.reveal_cell(row, col)  # Handle cell revealing

                pressed = None  # Reset the pressed state

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if banner.button_rect.collidepoint(event.pos):
                        if gameboard.game_over:
                            banner.button_img = images['sad_flat']
                        else:
                            if banner.button_state != 'pressed':
                                if gameboard.game_state == 'winner':
                                    banner.button_img = pressed_images[
                                        gameboard.game_state]
                                else:
                                    banner.button_img = images['smile_flat']
                                banner.button_state = 'pressed'
                    else:
                        if gameboard.game_over:
                            banner.button_img = images['sad']
                        else:
                            if banner.button_state == 'pressed':
                                banner.button_state = 'normal'
                                banner.button_img = images[
                                    gameboard.game_state]
                    pygame.draw.rect(DISPLAYSURF, BLACK, banner.button_rect)
                    DISPLAYSURF.blit(banner.button_img,
                                     banner.button_rect.topleft)
                    pygame.display.update()
                    col = (event.pos[0] - game_settings[
                        "MARGIN_SIZE"]) // game_settings["CELL_SIZE"]
                    row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                            game_settings["MARGIN_SIZE"]) // game_settings[
                               "CELL_SIZE"])

                    if 0 <= row < game_settings["ROWS"] and 0 <= col < \
                            game_settings["COLS"] and not \
                            gameboard.flagged[row][col] and not \
                            gameboard.revealed[row][col]:
                        pressed = (row, col)
                    else:
                        pressed = None

        if gameboard.game_started and not gameboard.game_over:
            if gameboard.start_ticks is not None:
                elapsed_time = pygame.time.get_ticks() - gameboard.start_ticks
                seconds = min((elapsed_time // 1000), 999)
                banner.timer = seconds  # Update the banner's timer with the
                # seconds value

                # Check if the timer has reached 999 seconds
                if seconds == 999:
                    gameboard.game_over = True  # Set game_over to True

                # Update the display of the timer
                banner.draw_timer()

        # Check for game over
        if gameboard.game_over:
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

        # Call the draw_timer function to update and render the timer
        banner.draw_timer()

        # draw pressed state
        if gameboard.pressed is not None:
            rect = gameboard.get_cell_rect(*gameboard.pressed)
            DISPLAYSURF.blit(images['flat'], rect)

        # Update the display
        pygame.display.update()


# Create the main display surface
DISPLAYSURF = pygame.display.set_mode((game_settings["SCREEN_WIDTH"],
                                       game_settings["SCREEN_HEIGHT"]))
pygame.display.set_caption('Minesweeper')


# First, create instances of Banner and GameBoard
banner = Banner(DISPLAYSURF, game_state_images, pressed_images)
gameboard = GameBoard(DISPLAYSURF, banner, game_settings["ROWS"],
                      game_settings["COLS"], game_settings["MINES"], False)

# create an instance of your GameMenu with the created instances of
# GameBoard and Banner
game_menu = GameMenu(DISPLAYSURF, game_loop, draw, gameboard, banner)

gameboard.reset_game()
game_menu.run()
