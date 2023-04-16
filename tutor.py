import pygame
import os
import time
import random
import string

# Constants
MAX_LINES = 5
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
TEXT_INPUT_HEIGHT = int(HEIGHT * 0.1)
CURSOR_BLINK_RATE = 500
PADDING = 10
LINE_SPACING = 4
#TEXT_INPUT_X = (WIDTH - TEXT_INPUT_WIDTH) // 2
#@TEXT_INPUT_Y = HEIGHT - TEXT_INPUT_HEIGHT
TEXT_INPUT_WIDTH = int(WIDTH * 0.9)
TEXT_INPUT_HEIGHT = int(HEIGHT * 0.1)
FLOATING_LETTERS = 5
LETTER_SPAWN_INTERVAL = 1.5
DEFAULT_COLOR = (153, 255, 153)
INPUT_BACKGROUND_COLOR = (0, 100, 0)
INPUT_TEXT_COLOR = (153, 255, 153)
MIN_SPEED = 20.0
MAX_SPEED = 20.0
KEYBOARD_IMAGE = "keyboard.png"
HANDS_IMAGE = "hands.png"


def init_pygame():
    pygame.init()
    pygame.font.init()

def load_image(filename, width, height, alpha=None):
    image = pygame.image.load(os.path.join("assets", filename))
    image = image.convert_alpha()
    if alpha is not None:
        image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    image = pygame.transform.scale(image, (width, height))
    return image

def handle_cursor_blinking(current_time, last_blink_time, cursor_visible, cursor_blink_rate):
    if current_time - last_blink_time >= cursor_blink_rate / 1000:
        cursor_visible = not cursor_visible
        last_blink_time = current_time
    return cursor_visible, last_blink_time

def create_floating_letter(font, screen_width, screen_height):
    letter = random.choice(string.ascii_letters)
    #x = screen_width // 2 - font.size(letter)[0] // 2
    x = random.randint(TEXT_INPUT_HEIGHT, screen_width - font.size(letter)[0])
    y = random.randint(TEXT_INPUT_HEIGHT, screen_height - font.size(letter)[1])
    speed = MAX_SPEED
    return FloatingLetter(letter, font, x, y, speed, color=DEFAULT_COLOR)

# Create the FloatingLetter class
class FloatingLetter:
    def __init__(self, letter, font, x, y, speed, color=(0, 0, 0), highlight_colors=((255, 0, 0), (255, 255, 0), (255, 0, 0))):
        self.letter = letter
        self.font = font
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.highlight_colors = highlight_colors
        self.flash_duration = 0.25
        self.highlighted = False
        self.highlight_start_time = None
        self.flash_index = 0

    def draw(self, surface):
        if self.highlighted:
            elapsed_time = time.time() - self.highlight_start_time
            self.flash_index = int(elapsed_time // self.flash_duration) % len(self.highlight_colors)
            color = self.highlight_colors[self.flash_index]
        else:
            color = self.color

        rendered_letter = self.font.render(self.letter, True, color)
        surface.blit(rendered_letter, (self.x, self.y))

    def update(self, dt):
        self.y -= self.speed * dt

    def is_offscreen(self, screen_height):
        return self.y < -self.font.get_height()

    def highlight(self):
        self.highlighted = True
        self.highlight_start_time = time.time()

    def ready_to_remove(self):
        return self.highlighted and time.time() - self.highlight_start_time >= self.flash_duration * len(self.highlight_colors)

def main():
    init_pygame()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Typing Game")
    
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 32)
    text_input_surface = pygame.Surface((TEXT_INPUT_WIDTH, TEXT_INPUT_HEIGHT))

    # Set the position of the keyboard image at the bottom of the screen
    keyboard_image_filename = KEYBOARD_IMAGE
    keyboard_image_width = int(WIDTH * 0.9)
    keyboard_image_height = int(HEIGHT * 0.3)
    keyboard_image = load_image(keyboard_image_filename, keyboard_image_width, keyboard_image_height)
    keyboard_image_x = (WIDTH - keyboard_image.get_width()) // 2
    keyboard_image_y = HEIGHT - keyboard_image.get_height()
    keyboard_rect = keyboard_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))


    TEXT_INPUT_X = (WIDTH - TEXT_INPUT_WIDTH) // 2
    TEXT_INPUT_Y = keyboard_image_y - TEXT_INPUT_HEIGHT - PADDING

    input_rect = pygame.Rect(TEXT_INPUT_X, TEXT_INPUT_Y, TEXT_INPUT_WIDTH, TEXT_INPUT_HEIGHT)

    running = True
    user_input = ''
    cursor_visible = True
    last_blink_time = time.time()

    floating_letters = []
    last_spawn_time = time.time()

    
    hands_image = load_image(HANDS_IMAGE, int(WIDTH * 0.9), int(HEIGHT * 0.3))
    hands_rect = hands_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    hands_image_x = (WIDTH - hands_image.get_width()) // 2
    hands_image_y = HEIGHT - hands_image.get_height()



    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    user_input = ''
                elif event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    user_input += event.unicode

        # Spawn new floating letters
        if time.time() - last_spawn_time >= LETTER_SPAWN_INTERVAL:
            new_letter = create_floating_letter(font, WIDTH, HEIGHT - TEXT_INPUT_HEIGHT)
            floating_letters.append(new_letter)
            last_spawn_time = time.time()

        # Update floating letters
        for letter in floating_letters:
            letter.update(dt)
            if user_input and user_input[-1].lower() == letter.letter.lower() and not letter.highlighted:
                letter.highlight()
                user_input = user_input[:-1]

        floating_letters = [letter for letter in floating_letters if not letter.is_offscreen(HEIGHT - TEXT_INPUT_HEIGHT) and not letter.ready_to_remove()]

        # Cursor blink handling
        cursor_visible, last_blink_time = handle_cursor_blinking(time.time(), last_blink_time, cursor_visible, CURSOR_BLINK_RATE)

        # Draw
        screen.fill(BACKGROUND_COLOR)
        screen.blit(keyboard_image, (keyboard_image_x, keyboard_image_y))
        screen.blit(hands_image, (hands_image_x, hands_image_y))


        # Draw floating letters
        for letter in floating_letters:
            letter.draw(screen)

        # Draw input box
        text_input_surface.fill(INPUT_BACKGROUND_COLOR)
        text_input_surface.set_alpha(128)
        screen.blit(text_input_surface, input_rect)

        # Draw user input
        input_text = font.render(user_input, True, INPUT_TEXT_COLOR)
        input_text_x = TEXT_INPUT_X + PADDING
        input_text_y = TEXT_INPUT_Y + PADDING
        screen.blit(input_text, (input_text_x, input_text_y))


        # Draw cursor
        if cursor_visible:
            cursor_x = input_text.get_width() + PADDING
            cursor_y = PADDING
            cursor_h = font.get_height()
            cursor = pygame.Rect(cursor_x, cursor_y, 2, cursor_h)
            pygame.draw.rect(screen, INPUT_TEXT_COLOR, cursor)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
