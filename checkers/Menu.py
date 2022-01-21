from checkers import pygame, screen
from checkers.MenuButton import MenuButton
from checkers.surfaces import smaller_font, font

class Menu:
    def __init__(self, name, button_names, redirects, text, width, height, small_text=None):
        self.background_color = (11,138,156)
        self.surf = pygame.Surface((width, height))
        self.surf.fill(self.background_color)
        self.rect = self.surf.get_rect(topleft=(0, 0))
        self.button_names = button_names
        self.redirects = redirects
        self.small_text = small_text
        self.text = font.render(str(text), True, (0,0,0))
        if not self.small_text:
            self.text_rect = self.text.get_rect(center=(width/2, height/4))
        else:
            self.text_rect = self.text.get_rect(center=(width/2, height/8))
        self.name = name
        if len(redirects) < len(button_names):
            redirects += ["main_menu"] * (len(button_names) - len(redirects))

        self.button_list = []

        # Generating the buttons
        for i, (name, redirect) in enumerate(zip(button_names, redirects)):
            offset = height/7
            if not self.small_text:
                center_height = height*0.6
            else:
                center_height = height*0.85

            pos = (width/2, (center_height)+(i*offset)-(len(button_names)*offset/4))
            size = (len(name)*22 * (width/600) + 20, height/9)
            new_button = MenuButton(pos, size, redirect, text=name)

            # Case for empty buttons for padding
            if name != "empty":
                self.button_list.append(new_button)

        # Generating the small_text
        if self.small_text:
            self.small_text_list = []
            text = self.small_text

            limit = 40
            pointer = 0
            y_pos = 0

            while pointer+2 <= len(text):
                next_pointer = min(len(text)-1, pointer+limit)
                while text[next_pointer] not in (" ",",",".","!","?") or next_pointer == len(text):
                    next_pointer -= 1
                text_surf = smaller_font.render(text[pointer:next_pointer].strip(" "), True, (0,0,0))
                x_pos = (width - text_surf.get_width())/2
                self.small_text_list.append((text_surf, (x_pos, height/5.5 +(height/15 * y_pos))))
                pointer = next_pointer
                y_pos += 1

    def draw(self):
        screen.blit(self.surf, self.rect)
        screen.blit(self.text, self.text_rect)

    def draw_small_text(self):
        for surf, pos in self.small_text_list:
            screen.blit(surf, pos)

    def update(self):
        self.draw()
        for button in self.button_list:
            button.draw_outline()
            redirect = button.update()
            if redirect:
                return redirect
        return self.name
