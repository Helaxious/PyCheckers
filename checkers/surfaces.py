from checkers import pygame, screen, width, height

font_unit = ((width + height) * 0.85) / 1000
font_size = lambda x: round(font_unit * x)

surf_size = (round(width/12), round(height/12))
pygame.font.init()

font = pygame.font.Font("checkers/assets/JetBrainsMono-ExtraBold.ttf", font_size(45))
small_font = pygame.font.Font("checkers/assets/JetBrainsMono-ExtraBold.ttf", font_size(30))
kinda_small_font = pygame.font.Font("checkers/assets/JetBrainsMono-ExtraBold.ttf", font_size(25))
smaller_font = pygame.font.Font("checkers/assets/JetBrainsMono-ExtraBold.ttf", font_size(21))

beige_knight = pygame.image.load("checkers/assets/beige_knight.png").convert_alpha()
beige_knight = pygame.transform.scale(beige_knight, surf_size)
beige_queen = pygame.image.load("checkers/assets/beige_queen.png").convert_alpha()
beige_queen = pygame.transform.scale(beige_queen, surf_size)
red_knight = pygame.image.load("checkers/assets/red_knight.png").convert_alpha()
red_knight = pygame.transform.scale(red_knight, surf_size)
red_queen = pygame.image.load("checkers/assets/red_queen.png").convert_alpha()
red_queen = pygame.transform.scale(red_queen, surf_size)
home_surf = pygame.image.load("checkers/assets/home_button.png").convert_alpha()
home_surf = pygame.transform.scale(home_surf, surf_size)


pointer_off_surf = pygame.image.load("checkers/assets/pointer_off.png").convert_alpha()
pointer_off_surf = pygame.transform.scale( pointer_off_surf, surf_size)
pointer_on_surf = pygame.image.load("checkers/assets/pointer_on.png").convert_alpha()
pointer_on_surf = pygame.transform.scale(pointer_on_surf, surf_size)
