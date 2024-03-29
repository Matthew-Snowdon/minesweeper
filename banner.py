from utilities import *


class Banner:
    """
    A Banner class used to display and update the game banner.

        Attributes:
            display_surface: The surface on which the banner is drawn.
            game_state_images: A dictionary mapping game states to their
            respective images.
            pressed_images: A dictionary mapping game states to their
            respective images when pressed.
            game_font: The font used for displaying text on the banner.
            counter: The current count of mines or flags (depending on the
            game state).
            timer: The game timer value.
            button_rect: The rectangle defining the area of the button on the
            banner.
            button_state: The current state of the button
            button_clicked: Boolean indicating if the button has been clicked.
            button_img: The image of the button displayed on the banner.
    """
    def __init__(self, display_surface, game_state_image, pressed_image):
        """
        Initializes the Banner with a display surface, game state images,
        and pressed images.

                Args: display_surface: The surface on which the banner will
                be drawn. game_state_image: A dictionary mapping game states
                to images. pressed_image: A dictionary mapping game states
                to images when pressed.
        """
        self.display_surface = display_surface
        self.game_state_images = game_state_image
        self.pressed_images = pressed_image
        self.game_font = pygame.font.Font('assets/digital7.ttf', 70)
        self.counter = game_settings['MINES']
        self.timer = 0
        self.button_rect = None
        self.button_state = 'normal'
        self.button_clicked = False
        self.button_img = images['smile']

    def update_counter(self, new_count):
        """
               Updates the counter with a new value.

               Args:
                   new_count: The new value to set the counter to.
               """
        self.counter = new_count

    def draw_banner(self):
        """
                Draws the banner on the display surface.
                """
        # draw banner
        pygame.draw.rect(self.display_surface, (179, 179, 179),
                         pygame.Rect(game_settings["MARGIN_SIZE"],
                                     game_settings["MARGIN_SIZE"],
                                     game_settings["SCREEN_WIDTH"] - 2 *
                                     game_settings["MARGIN_SIZE"],
                                     game_settings["BANNER_HEIGHT"] -
                                     game_settings["MARGIN_SIZE"]))

    def draw_counter(self):
        """
                Draws the counter on the banner.

                Returns: A rectangle representing the area where the counter
                is drawn.
        """
        counter_text = self.game_font.render(f'{self.counter:03}', True, RED)
        counter_width, counter_height = counter_text.get_size()
        counter_pos_y = (game_settings["MARGIN_SIZE"] +
                         (game_settings["adjusted_banner_height"] // 2) -
                         (counter_height // 2))

        counter_pos = (game_settings["MARGIN_SIZE"] + 14, counter_pos_y)
        counter_rect = counter_text.get_rect(topleft=counter_pos)
        counter_under_text_surface = self.game_font.render('888', True, RED)
        counter_under_text_surface.set_alpha(76)
        counter_under_text_rect = counter_under_text_surface.get_rect(
            topleft=counter_pos)
        pygame.draw.rect(self.display_surface, BLACK, counter_under_text_rect)
        self.display_surface.blit(counter_under_text_surface,
                                  counter_under_text_rect.topleft)
        self.display_surface.blit(counter_text, counter_rect.topleft)
        return counter_rect

    def draw_timer(self):
        """
                Draws the timer on the banner.

                Returns:
                    A rectangle representing the area where the timer is drawn.
                """
        timer_text = self.game_font.render(f'{self.timer:03}', True, RED)
        text_width, text_height = timer_text.get_size()
        timer_pos_y = (game_settings["MARGIN_SIZE"] +
                       (game_settings["adjusted_banner_height"] // 2) -
                       (text_height // 2))

        timer_pos = (game_settings["SCREEN_WIDTH"] - text_width - 14 -
                     game_settings["MARGIN_SIZE"], timer_pos_y)
        timer_rect = timer_text.get_rect(topleft=timer_pos)
        under_text_surface = self.game_font.render('888', True, RED)
        under_text_surface.set_alpha(76)
        under_text_rect = under_text_surface.get_rect(topleft=timer_pos)
        pygame.draw.rect(self.display_surface, BLACK, under_text_rect)
        self.display_surface.blit(under_text_surface, under_text_rect.topleft)
        self.display_surface.blit(timer_text, timer_rect.topleft)
        return timer_rect

    def draw_button(self, game_state, button_state):
        """
        Draws the button on the banner based on the current game state and
        button state.

                Args:
                    game_state: The current state of the game.
                    button_state: The current state of the button.
                """
        timer_rect = self.draw_timer()
        counter_rect = self.draw_counter()

        # Calculate the center position between the timer and the counter
        center_x = (timer_rect.centerx + counter_rect.centerx) // 2
        center_y = (game_settings["MARGIN_SIZE"] +
                    game_settings["BANNER_HEIGHT"] / 2)

        # Calculate the top-left position of the button
        button_pos_y = (game_settings["MARGIN_SIZE"] +
                        (game_settings["adjusted_banner_height"] / 2) -
                        (BUTTON_HEIGHT / 2))
        button_pos_x = center_x - BUTTON_WIDTH // 2

        # Create the button rectangle
        self.button_rect = pygame.Rect(button_pos_x, button_pos_y,
                                       BUTTON_WIDTH, BUTTON_HEIGHT)

        # Create the shadow rectangle
        shadow_pos_x = button_pos_x - SHADOW_OFFSET_X
        shadow_pos_y = button_pos_y - SHADOW_OFFSET_Y
        shadow_rect = pygame.Rect(shadow_pos_x, shadow_pos_y, BUTTON_WIDTH,
                                  BUTTON_HEIGHT)

        # Draw the shadow image behind the button
        self.display_surface.blit(shadow_image, shadow_rect.topleft)

        # Draw the button with the appropriate image based on the game state
        button_img = self.game_state_images[game_state]
        # Determine the correct button image based on the game state and
        # button state
        if button_state == 'pressed':  # Change the image if the button is
            # pressed
            button_img = self.pressed_images[game_state]

        pygame.draw.rect(self.display_surface, BLACK, self.button_rect)
        self.display_surface.blit(button_img, self.button_rect.topleft)
