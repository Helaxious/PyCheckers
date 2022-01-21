from checkers.surfaces import *
from checkers.Menu import Menu
from checkers.MenuButton import MenuButton
from checkers.Button import Button
from checkers.TextButton import TextButton
from checkers.Game import Game

surf_size = (round(width/12), round(height/12))

class GameInterface:
    def __init__(self, width, height):
        self.current_player = "player_1"

        self.width = width
        self.height = height
        self.home_button = MenuButton(pos=(width/20, height/20), size=surf_size, surf=home_surf, redirect="confirm_save")

        self.pointer_1 = Button(pos=(width*0.94, height/3), size=(width/15, height/15), surf=pointer_off_surf)

        pointer_2 = pygame.transform.rotate(pointer_on_surf, 180)
        self.pointer_2 = Button(pos=(width*0.94, height/1.5), size=(width/15, height/15), surf=pointer_2)
        self.clock = TextButton(pos=(width/2,height/16), size=(width/6,height/12), color=(222,222,222), text="00:00", font=small_font, text_color=(73,73,73))

        self.red_pieces_counter = Button(pos=(width*0.94, height/2.4), size=surf_size, surf=red_queen)
        self.beige_pieces_counter = Button(pos=(width*0.94, height/1.7), size=surf_size, surf=beige_queen)

    def win_surfs_init(self, player_winner, turns, time):
        MenuButton.reset_queue([True, True])
        width = self.width
        height = self.height
        self.win_menu_surf = pygame.Surface((width/1.7, height/2.4))
        self.win_menu_surf.fill((11,138,156))
        self.win_menu_rect = self.win_menu_surf.get_rect(center=(width/2, height/2))

        self.win_menu_exit = MenuButton(pos=(width/2, height/1.55), size=(width/2.8, height/10), redirect="main_menu", text="Main Menu")
        self.win_menu_player_text = TextButton((width/2, height/2.5), (width/3,height/7), (11,138,156), player_winner, small_font, (38,23,26))

        def exit_game():
            Game.delete_current_game()
            return "main_menu"
        self.win_menu_exit.set_onclick(exit_game)

        self.turns_text = TextButton((width/2, height/2.1), (0,0), (11,138,156), f"Turns: {turns}", smaller_font, (38,23,26))
        self.time_text = TextButton((width/2, height/1.9), (0,0), (11,138,156), f"Time: {time}", smaller_font, (38,23,26))

    def win_screen(self):
        screen.blit(self.win_menu_surf, self.win_menu_rect)
        redirect = self.win_menu_exit.update()
        self.win_menu_player_text.update()
        self.turns_text.update()
        self.time_text.update()
        if redirect: return redirect

    def set_board(self, board):
        self.board = board
        def redirect_reset_time():
            self.board.reset_current_time()
            return "confirm_save"
        self.home_button.on_click_function = redirect_reset_time
        self.beige_pieces_text = TextButton((self.width*0.94, height/1.9), (width/15, height/30), (233,230,227), "12", smaller_font, (48,33,36))
        self.red_pieces_text = TextButton((self.width*0.94, height/2.1), (width/15, height/30), (233,230,227), "12", smaller_font, (48,33,36))

    def toggle_pointer(self):
        self.pointer_1.surf, self.pointer_2.surf = self.pointer_2.surf, self.pointer_1.surf
        self.pointer_1.surf = pygame.transform.rotate(self.pointer_1.surf, 180)
        self.pointer_2.surf = pygame.transform.rotate(self.pointer_2.surf, 180)
        print(self.current_player)
        self.current_player = "player_1" if self.current_player == "player_2" else "player_2"

    def update(self):
        if not self.board.game_won:
            redirect = self.home_button.update()
            if redirect: return redirect
        if self.board.game_won:
            redirect = self.win_screen()
            if redirect: return redirect

        pygame.draw.rect(screen,(226,206,178), pygame.Rect(self.width*0.90, height/3.45, width/12, height/2.35))

        self.pointer_1.update()
        self.pointer_2.update()
        self.clock.update_text(self.board.time_passed)
        self.clock.update()
        self.red_pieces_counter.update()
        self.beige_pieces_counter.update()
        self.red_pieces_text.update()
        self.beige_pieces_text.update()
        self.red_pieces_text.update_text(self.board.red_pieces_counter)
        self.beige_pieces_text.update_text(self.board.beige_pieces_counter)
        return "game"
