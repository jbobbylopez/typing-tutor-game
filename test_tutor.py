import unittest
import pygame
from main import create_floating_letter, create_floating_word, wrap_text, simple_words, FloatingWord

class TestFloatingLetterCreation(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_create_floating_letter(self):
        font = pygame.font.Font(None, 32)
        letter = create_floating_letter(font, 800, 600 - 100)
        self.assertIsNotNone(letter)

class TestFloatingWordCreation(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_create_floating_word(self):
        font = pygame.font.Font(None, 32)
        floating_objects = []
        word = create_floating_word(font, 200, 100, floating_objects)
        self.assertIsNotNone(word)

class TestTextWrapping(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_wrap_text(self):
        font = pygame.font.Font(None, 32)
        text = "This is a long sentence that needs to be wrapped"
        wrapped_text = wrap_text(text, font, 200)
        self.assertIsNotNone(wrapped_text)

class TestWordGeneration(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_word_in_simple_words(self):
        font = pygame.font.Font(None, 32)
        floating_objects = []
        word = create_floating_word(font, 200, 100, floating_objects)
        self.assertIn(word.word, simple_words)

class TestFloatingWordBehavior(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_floating_word_upward_speed(self):
        font = pygame.font.Font(None, 32)
        floating_word = FloatingWord("test", font, 100, 100, (0, -2), (255, 255, 255))
        self.assertEqual(floating_word.speed, (0, -2))

class TestFloatingWordPosition(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_floating_word_position(self):
        screen_width, screen_height = 800, 600
        font = pygame.font.Font(None, 32)
        floating_objects = []

        INPUT_BOX_HEIGHT = 50  # Adjust this value to match the height of the green text input box

        for _ in range(10):  # Test 10 random floating words
            word = create_floating_word(font, screen_width, screen_height, floating_objects)
            self.assertIsNotNone(word)
            self.assertGreaterEqual(screen_height - INPUT_BOX_HEIGHT, word.y + font.size(word.word)[1])
            self.assertLessEqual(word.y, screen_height - INPUT_BOX_HEIGHT) 

if __name__ == '__main__':
    unittest.main()
