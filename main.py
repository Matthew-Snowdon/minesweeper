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


# def get_neighbors(row, col):
#     neighbors = []
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             if i == 0 and j == 0:  # Skip the cell itself
#                 continue
#             new_row, new_col = row + i, col + j
#             if 0 <= new_row < game_settings["ROWS"] and 0 <= new_col < \
#                     game_settings["COLS"]:
#                 neighbors.append((new_row, new_col))
#     return neighbors


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
                    gameboard.game_started = False
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
                            #pygame.display.update()
                    else:
                        banner.button_state = 'normal'
                        banner.button_clicked = False

                if gameboard.game_over:
                    # Don't handle any more mouse presses if the game
                    continue

                col = ((event.pos[0] - game_settings["MARGIN_SIZE"])
                       // game_settings["CELL_SIZE"])
                row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                        game_settings["MARGIN_SIZE"]) // game_settings[
                           "CELL_SIZE"])

                # Check if the click is outside the grid
                if (row < 0 or row >= game_settings["ROWS"] or col < 0 or
                        col >= game_settings["COLS"]):
                    gameboard.cell_clicked = True
                    continue

                # At this point, we're sure the click is inside the grid
                if gameboard.game_active and pygame.mouse.get_pressed()[0]:
                    if gameboard.flagged[row][col] or gameboard.revealed[row][
                        col]:
                        gameboard.game_state = 'smile'
                    else:
                        gameboard.game_state = 'shock'
                    banner.button_img = images[gameboard.game_state]

                    if gameboard.flagged[row][col]:  # The cell is flagged
                        pass  # Do nothing when left-clicking a flagged cell

                    elif not gameboard.revealed[row][col]:
                        gameboard.pressed = (row, col)

                # if gameboard.game_active and event.button == 1 and \
                #         gameboard.revealed[row][col]:
                #     neighbors = get_neighbors(row, col)
                #     for nr, nc in neighbors:
                #         if not gameboard.revealed[nr][nc] and not gameboard.flagged[nr][nc]:
                #             rect = gameboard.get_cell_rect(nr, nc)
                #             DISPLAYSURF.blit(images['flat'], rect)
                #
                #     pygame.display.update()

                elif event.button == 3 and gameboard.game_active:
                    if not gameboard.revealed[row][col]:
                        gameboard.toggle_flag(row, col)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    banner.button_state = 'normal'
                    if banner.button_rect.collidepoint(
                            event.pos) and banner.button_clicked:
                        gameboard.reset_game()  # Reset the game
                        gameboard.game_started = False  # Don't start the
                        # timer yet
                        gameboard.first_click = False  # Indicate that the
                        # first click hasn't happened
                        gameboard.game_state = 'smile'  # Reset the game state
                        banner.button_img = images[gameboard.game_state]
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(banner.button_img,
                                         banner.button_rect.topleft)
                        #pygame.display.update()
                    elif gameboard.game_over:
                        banner.button_img = images['sad']
                        pygame.draw.rect(DISPLAYSURF, BLACK,
                                         banner.button_rect)
                        DISPLAYSURF.blit(banner.button_img,
                                         banner.button_rect.topleft)
                        #pygame.display.update()
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
                                gameboard.game_started = True
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
                        #pygame.display.update()

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

                gameboard.pressed = None  # Reset the pressed state

                # if event.button == 1 and gameboard.revealed[row][col]:
                #     neighbors = get_neighbors(row, col)
                #     for nr, nc in neighbors:
                #         rect = gameboard.get_cell_rect(nr, nc)
                #         if gameboard.flagged[nr][nc]:
                #             gameboard.display_surface.blit(images['flag'],
                #                                            rect)
                #         elif gameboard.questioned[nr][nc]:
                #             gameboard.display_surface.blit(images['question'],
                #                                            rect)
                #         else:
                #             gameboard.display_surface.blit(images['tile'],
                #                                            rect)
                #
                #         pygame.draw.rect(gameboard.display_surface, DARK_GRAY,
                #                          rect, 1)

            elif event.type == pygame.MOUSEMOTION:
                col = (event.pos[0] - game_settings["MARGIN_SIZE"]) // \
                      game_settings["CELL_SIZE"]
                row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                        game_settings["MARGIN_SIZE"]) // game_settings[
                           "CELL_SIZE"])

                # Check if the mouse is outside the grid
                if (row < 0 or row >= game_settings[
                    "ROWS"] or col < 0 or col >= game_settings[
                        "COLS"]) and gameboard.game_state != 'smile':
                    gameboard.game_state = 'smile'
                    banner.button_img = images[gameboard.game_state]
                    pygame.draw.rect(DISPLAYSURF, BLACK,
                                     banner.button_rect)  # Redraw the button area
                    DISPLAYSURF.blit(banner.button_img,
                                     banner.button_rect.topleft)  # Update the button image
                    #pygame.display.update()

                # Check if the mouse is over the grid and the left button is pressed
                if 0 <= row < game_settings["ROWS"] and 0 <= col < \
                        game_settings["COLS"] and pygame.mouse.get_pressed()[
                    0]:
                    if gameboard.flagged[row][col] or gameboard.revealed[row][
                        col]:
                        if gameboard.game_state != 'smile':
                            gameboard.game_state = 'smile'
                            banner.button_img = images[gameboard.game_state]
                            pygame.draw.rect(DISPLAYSURF, BLACK,
                                             banner.button_rect)  # Redraw the button area
                            DISPLAYSURF.blit(banner.button_img,
                                             banner.button_rect.topleft)  # Update the button image
                            #pygame.display.update()

                        # Condition for unrevealed cell
                    elif not gameboard.revealed[row][col]:
                        if gameboard.game_state != 'shock':
                            gameboard.game_state = 'shock'
                            banner.button_img = images[gameboard.game_state]
                            pygame.draw.rect(DISPLAYSURF, BLACK,
                                             banner.button_rect)  # Redraw the button area
                            DISPLAYSURF.blit(banner.button_img,
                                             banner.button_rect.topleft)  # Update the button image
                            #pygame.display.update()

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
                    #pygame.display.update()
                    col = (event.pos[0] - game_settings[
                        "MARGIN_SIZE"]) // game_settings["CELL_SIZE"]
                    row = ((event.pos[1] - game_settings["BANNER_HEIGHT"] -
                            game_settings["MARGIN_SIZE"]) // game_settings[
                               "CELL_SIZE"])

                    if 0 <= row < game_settings["ROWS"] and 0 <= col < \
                            game_settings["COLS"] and not \
                            gameboard.flagged[row][col] and not \
                            gameboard.revealed[row][col]:
                        gameboard.pressed = (row, col)
                    else:
                        gameboard.pressed = None

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

# gameboard.reset_game()
game_menu.run()
