from checkers import pygame, screen
from checkers.Button import Button
from checkers.surfaces import small_font, smaller_font

class TextButton(Button):
    def __init__(self, pos, size, color, text, font, text_color):
        self.font = font
        self.text_color = text_color
        surf = pygame.Surface(size)
        surf.fill(color)
        super().__init__(pos, size, surf, text)
        self.text = self.font.render(text, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.pos))

    def update_text(self, text):
        self.text = self.font.render(str(text), True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.pos))
