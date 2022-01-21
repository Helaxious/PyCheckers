from checkers import pygame, screen
from checkers.surfaces import small_font

class Button:
    def __init__(self, pos, size, surf, text=None):
        self.pos = pos
        self.size = size
        self.surf = pygame.transform.scale(surf, tuple(map(int, size)))
        self.surf_rect = self.surf.get_rect(center=pos)
        self.text = text
        if text:
            self.text = small_font.render(str(text), True, (38,23,26))
            self.text_rect = self.text.get_rect(center=(self.pos))

    def set_surf(self, new_surf):
        self.surf_rect = new_surf

    def update(self):
        screen.blit(self.surf, self.surf_rect)
        if self.text:
            screen.blit(self.text, self.text_rect)
