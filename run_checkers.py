from sys import exit
from checkers import *

game = Game()
interface = GameInterface(width, height)
Game.set_interface(interface)
clock = pygame.time.Clock()

main_menu = Menu(name="main_menu", button_names=["Play Game", "Rules", "Quit"],
redirects=["load_save", "about", "quit"], text="PyCheckers!", width=width, height=height)
about_menu = Menu(name="about", button_names=["Back", "Next Page"],
                 redirects=["main_menu", "about_2"],text="Rules of Checkers", width=width, height=height, small_text=about_text)

about_menu_2 = Menu(name="about_2", button_names=["Previous Page", "Next Page"], redirects=["about", "about_3"], text="Rules of Checkers (2)", width=width, height=height, small_text=about_text_2)

about_menu_3 = Menu(name="about_3", button_names=["Previous Page", "Back"],
                 redirects=["about_2", "main_menu"],text="Local Rules", width=width, height=height, small_text=about_text_3)

select_menu = Menu(name="select_menu", button_names=["1 Player (soon)", "2 Players", "Back"],
                 redirects=["one_player_game", "first_player_menu", "load_save"],text="Select a Mode", width=width, height=height)

one_player_game = Menu(name="one_player_game", button_names=["Back"],
                 redirects=["select_menu"],text="Yeah, about that..", width=width, height=height, small_text=comming_soon_text)

first_player_menu = Menu(name="first_player_menu", button_names=["Player 1", "Player 2", "Back"],
                 redirects=["game","game","select_menu"],text="Who should play first?", width=width, height=height)
first_player_buttons = first_player_menu.button_list

def make_game(first_player):
    def return_game():
        Game.first_player = first_player
        Game.create_game()
        return "game"
    return return_game

first_player_buttons[0].set_onclick(make_game("player_1"))
first_player_buttons[1].set_onclick(make_game("player_2"))

confirm_save = Menu(name="confirm_save", button_names=["Save", "Exit", "Back"], redirects=["main_menu", "main_menu", "game"], text="Save Game?", width=width, height=height, small_text="(Quitting the game means you will lose all progress!).")

def save_game():
    Game.save_current_game()
    return "main_menu"

confirm_save_buttons = confirm_save.button_list
confirm_save_buttons[0].set_onclick(save_game)

# Doing manual adjustments to the buttons
for button in confirm_save_buttons:
    button.surf_rect.y -= 90
    button.text_rect.y -= 90

current_menu = "main_menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((242,242,242))

    MenuButton.update_input()
    if current_menu == "quit":
        pygame.quit()
        exit()
    if current_menu == "main_menu":
        current_menu = main_menu.update()
    if current_menu == "about":
        current_menu = about_menu.update()
        about_menu.draw_small_text()
    if current_menu == "about_2":
        current_menu = about_menu_2.update()
        about_menu_2.draw_small_text()
    if current_menu == "about_3":
        current_menu = about_menu_3.update()
        about_menu_3.draw_small_text()
    if current_menu == "select_menu":
        current_menu = select_menu.update()
    if current_menu == "one_player_game":
        current_menu = one_player_game.update()
        one_player_game.draw_small_text()
    if current_menu == "first_player_menu":
        current_menu = first_player_menu.update()
    if current_menu == "load_save":
        current_menu = Game.load_save_menu()
    if current_menu == "game":
        Game.current_game.update()
        current_menu = interface.update()
    if current_menu == "confirm_save":
        current_menu = confirm_save.update()
        confirm_save.draw_small_text()

    pygame.display.update()
    clock.tick(60)
