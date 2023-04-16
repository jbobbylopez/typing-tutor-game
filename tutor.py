import pygame
import os
import time
import random
import string
import textwrap
import nltk
from nltk.corpus import words
nltk.download('words')
english_words = set(words.words())

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

def create_floating_word(font, screen_width, screen_height):
    word = random.choice(list(english_words))
    x = random.randint(TEXT_INPUT_HEIGHT, screen_width - font.size(word)[0])
    y = random.randint(TEXT_INPUT_HEIGHT, screen_height - font.size(word)[1])
    speed = MAX_SPEED
    return FloatingWord(word, font, x, y, speed, color=DEFAULT_COLOR)

def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = words[0]

    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# Create the FloatingObject base class
class FloatingObject:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, dt):
        self.y -= self.speed * dt

    def draw(self, surface):
        pass

    def is_offscreen(self, screen_height):
        return False

    def highlight(self):
        pass

    def ready_to_remove(self):
        return False


# Create the FloatingLetter class
class FloatingLetter(FloatingObject):
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

class FloatingWord(FloatingObject):
    def __init__(self, word, font, x, y, speed, color=DEFAULT_COLOR):
        super().__init__(x, y, speed)
        self.word = word
        self.font = font
        self.color = color
        self.letters = [FloatingLetter(letter, font, x + i * font.size(letter)[0], y, speed, color=color) for i, letter in enumerate(word)]

    def draw(self, surface):
        for letter in self.letters:
            letter.draw(surface)

    def update(self, dt):
        for letter in self.letters:
            letter.update(dt)

    def is_offscreen(self, screen_height):
        return all(letter.is_offscreen(screen_height) for letter in self.letters)

    def highlight(self):
        for letter in self.letters:
            letter.highlight()

    def ready_to_remove(self):
        return all(letter.ready_to_remove() for letter in self.letters)

def main():
    init_pygame()

    current_mode = 'words'  # Change this to 'words' for floating words mode

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

    floating_objects = []
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

        # Spawn new floating objects based on the current mode
        if time.time() - last_spawn_time >= LETTER_SPAWN_INTERVAL:
            if current_mode == 'letters':
                new_object = create_floating_letter(font, WIDTH, HEIGHT - TEXT_INPUT_HEIGHT)
            elif current_mode == 'words':
                new_object = create_floating_word(font, WIDTH, HEIGHT - TEXT_INPUT_HEIGHT)
            floating_objects.append(new_object)
            last_spawn_time = time.time()

        # Update floating objects based on the current mode
        for obj in floating_objects:
            obj.update(dt)
            if isinstance(obj, FloatingLetter) and user_input and user_input[-1].lower() == obj.letter.lower() and not obj.highlighted:
                obj.highlight()
                user_input = user_input[:-1]
            elif isinstance(obj, FloatingWord) and user_input.lower() == obj.word.lower() and not obj.highlighted:
                obj.highlight()
                user_input = ''

        floating_objects = [obj for obj in floating_objects if not obj.is_offscreen(HEIGHT - TEXT_INPUT_HEIGHT) and not obj.ready_to_remove()]

        # Cursor blink handling
        cursor_visible, last_blink_time = handle_cursor_blinking(time.time(), last_blink_time, cursor_visible, CURSOR_BLINK_RATE)

        # Draw
        screen.fill(BACKGROUND_COLOR)
        screen.blit(keyboard_image, (keyboard_image_x, keyboard_image_y))
        screen.blit(hands_image, (hands_image_x, hands_image_y))


        # Draw floating objects
        for obj in floating_objects:
            obj.draw(screen)

        # Draw input box
        text_input_surface.fill(INPUT_BACKGROUND_COLOR)
        text_input_surface.set_alpha(128)
        screen.blit(text_input_surface, input_rect)

        # Draw user input
        wrapped_text = wrap_text(user_input, font, TEXT_INPUT_WIDTH - PADDING * 2)
        for i, line in enumerate(wrapped_text):
            input_text = font.render(line, True, INPUT_TEXT_COLOR)
            screen.blit(input_text, (TEXT_INPUT_X + PADDING, TEXT_INPUT_Y + PADDING + i * (font.get_height() + LINE_SPACING)))

        # Draw cursor
        if cursor_visible:
            last_line_width = font.size(wrapped_text[-1])[0] if wrapped_text else 0
            cursor_x = TEXT_INPUT_X + PADDING + last_line_width
            cursor_y = TEXT_INPUT_Y + PADDING + (len(wrapped_text) - 1) * (font.get_height() + LINE_SPACING)
            cursor_h = font.get_height()
            cursor = pygame.Rect(cursor_x, cursor_y, 2, cursor_h)
            pygame.draw.rect(screen, INPUT_TEXT_COLOR, cursor)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
