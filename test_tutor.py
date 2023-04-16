import unittest
import pygame
from tutor import create_floating_letter, create_floating_word, wrap_text

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

if __name__ == '__main__':
    unittest.main()
