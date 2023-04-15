import pygame
import os
import time

class TextInput:
    def __init__(self, x, y, width, height, font, max_lines, padding=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.max_lines = max_lines
        self.padding = padding

        self.text_lines = [""]
        self.current_line_index = 0
        self.cursor_position = 0
        self.line_height = self.font.get_height() + 2
        self.cursor_blink_timer = 0
        self.cursor_visible = True

    def draw(self, surface, x, y):
        for index, line in enumerate(self.text_lines):
            rendered_line = self.font.render(line, True, (0, 0, 0))
            surface.blit(rendered_line, (x, y + index * (self.font.get_height() + self.line_height)))


    def handle_keydown(self, event_key, event_unicode):
        if event_key == pygame.K_RETURN:
            self.text_lines.append("")
            self.current_line_index += 1
        elif event_key == pygame.K_BACKSPACE:
            if self.text_lines[self.current_line_index]:
                self.text_lines[self.current_line_index] = self.text_lines[self.current_line_index][:-1]
            elif self.current_line_index > 0:
                self.text_lines.pop(self.current_line_index)
                self.current_line_index -= 1
        elif event_key == pygame.K_DELETE:
            self.text_lines = [">"]
            self.current_line_index = 0
        else:
            if len(self.text_lines[self.current_line_index]) < self.width:
                self.text_lines[self.current_line_index] += event_unicode
            elif len(self.text_lines) * (self.font.get_height() + self.line_spacing) < self.height - self.font.get_height() - self.line_spacing:
                self.text_lines.append(event_unicode)
                self.current_line_index += 1

    def cursor_position(self):
        cursor_x = self.padding + self.font.size(self.text[self.current_line])[0]
        cursor_y = self.current_line * (self.font.get_height() + self.line_spacing)
        return cursor_x, cursor_y

    def draw_cursor(self, screen):
        """Draw the cursor on the screen."""
        if not self.text_lines:  # Check if the list is empty
            self.text_lines.append("")
        x = self.padding + self.font.size(self.text_lines[self.current_line_index][:self.cursor_position])[0]
        y = self.padding + self.line_height * self.current_line_index
        cursor_rect = pygame.Rect(x, y, 2, self.line_height)
        pygame.draw.rect(screen, (0, 0, 0), cursor_rect)

class Keyboard:
    def __init__(self, image, key_map):
        self.image = image
        self.key_map = key_map
        self.pressed_keys = set()

    def draw(self, screen):
        screen.blit(self.image, (0, HEIGHT - self.image.get_height()))

        for key_data in self.pressed_keys:
            key_code, x, y, w, h = key_data
            pygame.draw.rect(screen, (0, 0, 255), (x, HEIGHT - self.image.get_height() + y, w, h), 2)

    def handle_keydown(self, key_code):
        if key_code in self.key_map:
            x, y, w, h = self.key_map[key_code]
            self.pressed_keys.add((key_code, x, y, w, h))

    def handle_keyup(self, key_code):
        if key_code in self.pressed_keys:
            self.pressed_keys.remove(key_code)

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

def draw_border(surface, rect, color, thickness):
    pygame.draw.lines(surface, color, True, [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom)
    ], thickness)

def generate_qwerty_key_map():
    key_map = {
        # Add the key codes and their corresponding (x, y, w, h) rectangular areas
        pygame.K_a: (125, 140, 60, 58),  # Example values, replace with actual coordinates and dimensions
        pygame.K_b: (430, 209, 57, 54), # Example values, replace with actual coordinates and dimensions
        pygame.K_c: (295, 208, 57, 56), # Example values, replace with actual coordinates and dimensions
        # ...
    }
    return key_map

# Constants
MAX_LINES = 5
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
TEXT_INPUT_HEIGHT = int(HEIGHT * 0.1)
CURSOR_BLINK_RATE = 500
PADDING = 10
LINE_SPACING = 4
TEXT_INPUT_X = 0
TEXT_INPUT_Y = 0
TEXT_INPUT_WIDTH = int(WIDTH * 0.9)
TEXT_INPUT_HEIGHT = int(HEIGHT * 0.1)


# Initialize Pygame
init_pygame()

# Create a display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hands on Keyboard")

# Load images
keyboard_image = load_image("keyboard.png", WIDTH, int(HEIGHT * 0.4))
hands_image = load_image("hands.png", WIDTH, int(HEIGHT * 0.6), alpha=153)

# Initialize font and text input
font = pygame.font.Font(None, 24)
max_chars_per_line = (WIDTH - 2 * PADDING) // (font.size("a")[0])
text_input = TextInput(TEXT_INPUT_X, TEXT_INPUT_Y, TEXT_INPUT_WIDTH, TEXT_INPUT_HEIGHT, font, MAX_LINES)

# Initialize keyboard
key_map = generate_qwerty_key_map()
keyboard = Keyboard(keyboard_image, key_map)

# Main loop
running = True
cursor_visible = True
last_blink_time = time.time()

while running:
    current_time = time.time()
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            text_input.handle_keydown(event.key, event.unicode)
            keyboard.handle_keydown(event.key)
        elif event.type == pygame.KEYUP:
            keyboard.handle_keyup(event.key)

    # Draw text input
    text_input.draw(screen, PADDING, HEIGHT - TEXT_INPUT_HEIGHT - keyboard_image.get_height())

    # Draw border around text input
    draw_border(screen, pygame.Rect(PADDING, HEIGHT - TEXT_INPUT_HEIGHT - keyboard_image.get_height(), WIDTH - 2 * PADDING, TEXT_INPUT_HEIGHT), (0, 0, 0), 2)

    # Draw keyboard
    keyboard.draw(screen)

    # Draw hands
    hands_rect = hands_image.get_rect()
    hands_rect.y = HEIGHT - hands_image.get_height() * 0.75
    screen.blit(hands_image, hands_rect)

    # Cursor blinking
    cursor_visible, last_blink_time = handle_cursor_blinking(current_time, last_blink_time, cursor_visible, CURSOR_BLINK_RATE)
    if cursor_visible:
        text_input.draw_cursor(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
