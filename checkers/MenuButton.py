from checkers import pygame, screen
from checkers.Button import Button

class MenuButton(Button):
    mouse_queue = [None, None]
    def __init__(self, pos, size, redirect, surf=None, text=None):
        self.redirect = redirect
        self.is_image = bool(surf)

        def redirect():
            return self.redirect
        self.on_click_function = redirect
        if not surf:
            surf = pygame.Surface(size)
            surf.fill((64,184,201))

        super().__init__(pos, size, surf, text)
        
    @classmethod
    def reset_queue(cls, queue):
        MenuButton.mouse_queue = queue

    def set_onclick(self, function):
        self.on_click_function = function

    def draw_outline(self):
        pygame.draw.rect(screen,(28,111,124), self.surf_rect, 5)

    @classmethod
    def update_input(cls):
        MenuButton.mouse_queue.pop(0)
        MenuButton.mouse_queue.append(pygame.mouse.get_pressed()[0])

    def update(self):
        if self.surf_rect.collidepoint(pygame.mouse.get_pos()):
            if not self.is_image:
                self.surf.fill((119,209,222))
            if MenuButton.mouse_queue[0] == False and MenuButton.mouse_queue[1]:
                MenuButton.mouse_queue = [None, None]
                function = self.on_click_function()
                if function:
                    return function
        else:
            if not self.is_image:
                self.surf.fill((64,184,201))
        super().update()
