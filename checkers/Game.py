from checkers.surfaces import small_font, kinda_small_font
from checkers import pygame, width, height, screen, glob
from checkers.Board import Board
from checkers.Menu import Menu
from checkers.MenuButton import MenuButton
from json import load, dump
from os import remove

class Game:
    first_player = "player_1"
    current_game = None
    current_menu = "load_save_0"
    menus = {}

    @classmethod
    def set_interface(cls, interface):
        Game.interface = interface

    def adjust_menu(menu, button_names):
        button_list = menu.button_list

        for i, button in enumerate(button_list):
            button.surf = pygame.Surface((button.text.get_width()+ (width/60),
                                        button.surf.get_height()- (height/25)))
            button.surf_rect = button.surf.get_rect(midtop=(width/2,
                                                button.surf_rect.y+(height/15 - ((height/15) * i))))
            button.text_rect.y += (height/20 - ((height/15) * i))
            button.text = kinda_small_font.render(button_names[i], True, (38,23,26))
            button.text_rect = button.text.get_rect(midtop=(width/2, button.text_rect.y))

        menu.text_rect.y = 20
        surf_y_size = button_list[0].surf_rect.top - menu.text_rect.bottom

        menu_surf = pygame.Surface((width*0.8, surf_y_size- (height/20)))
        menu_rect = menu_surf.get_rect(midtop=(width/2, menu.text_rect.bottom + height/40))
        menu_surf.fill((5,123,140))

        return menu, (menu_surf, menu_rect)

    def make_menu(save_states=None, save=None, i=0):
        if save_states:
            button_names = ["Next Page", "Previous Page", "Create New Game"]
            redirects = [f"load_save_{i+1}",f"load_save_{i-1}","select_menu"]
            if i == 0:
                button_names.remove("Previous Page")
                redirects.remove(f"load_save_{i-1}")
            if (i+1) == len(save_states) or len(save_states) <= 1:
                button_names.remove("Next Page")
                redirects.remove(f"load_save_{i+1}")

            # Putting some filler buttons to pad the space
            button_names = button_names + ["empty"] * (3 - len(button_names))
        else:
            button_names = ["Create New Game"]
            redirects = ["select_menu"]

        menu = Menu(name=f"load_save_{i}", button_names=button_names, redirects=redirects, text="Load Menu", width=width, height=height, small_text="blank.")
        def make_game():
            Game.create_game()
            return "select_menu"

        menu.button_list[-1].set_onclick(make_game)
        menu, menu_surf = Game.adjust_menu(menu, button_names)

        if save_states:
            contents = Game.get_contents(menu, menu_surf, save)
        else:
            contents = {}

        contents["menu_surf"] = menu_surf
        Game.menus[f"load_save_{i}"] = (menu, contents)

    def init_menu():
        div = 3
        get_id = lambda x: int(x[26:-5])
        save_states = (sorted(glob("game_save/*.json"), key=get_id, reverse=True))
        save_states = [save_states[i:i+div] for i in range(0, len(save_states), div)]

        Game.menus = {}
        Game.back_button = MenuButton(pos=(width*0.12, height/12), size=(width/6, height/12.5), redirect="main_menu", text="Back")
        if save_states:
            for i, save in enumerate(save_states):
                Game.make_menu(save_states, save, i)
        else:
            Game.empty_message = kinda_small_font.render("Empty :/", True, (38,23,26))
            Game.empty_message_rect = Game.empty_message.get_rect(center=(width/2, height/2.3))
            Game.make_menu()

    def get_contents(menu, menu_surf, saves):
        surf_width = menu_surf[1].width
        surf_height = menu_surf[1].height
        border = (height+width) / 120
        surf_width = surf_width - (border * 2)
        surf_height = (surf_height - (border * 4)) / 3

        get_id = lambda x: int(x[26:-5])
        contents = {"surfs":[], "buttons":[], "text":[]}
        for i, save_state in enumerate(saves):
            save_state_surf = pygame.Surface((surf_width, surf_height))
            save_state_rect = save_state_surf.get_rect(midtop=((surf_width/2)+border, (surf_height * i) + (border * (i+1))))
            save_state_surf.fill((4,103,117))
            contents["surfs"].append((save_state_surf, save_state_rect))

            save_info = Game.get_save_info(save_state)
            w, h = save_state_rect.width, save_state_rect.height
            x, y = save_state_rect.midbottom
            x, y = x+(border/2)+(surf_width/8), y+(surf_height/8)

            load_button = MenuButton(pos=(x+w/8, border+y+h/2), size=(w*(0.48/2), h*0.45), redirect="game" ,text="Load")
            delete_button = MenuButton(pos=(x+w/2.75, border+y+h/2), size=(w*(0.48/2), h*0.45), redirect="load_save" ,text="Delete")

            def load_game(save_state):
                def load():
                    Game.load_save(get_id(save_state))
                    return "game"
                return load

            def delete_game(save_state):
                def delete():
                    menu_name = f"delete_confirm_{get_id(save_state)}"
                    previous_menu = Game.current_menu
                    Game.menus[menu_name] = Game.make_delete_menu(save_state, menu_name, previous_menu)
                    Game.current_menu = menu_name
                    return "load_save"
                return delete

            load_button.on_click_function = (load_game(save_state))
            delete_button.on_click_function = (delete_game(save_state))
            contents["buttons"].append(load_button)
            contents["buttons"].append(delete_button)

            pos_list = ((w*0.25, h*0.75), (w*0.75, h*0.25), (w*0.25, h*0.25))
            for i, (text, pos) in enumerate(zip(save_info, pos_list)):
                text_surf = small_font.render(str(text), True, (38,23,26))
                text_rect = text_surf.get_rect(center=pos)
                contents["text"].append((text_surf, text_rect))
        return contents

    def get_save_info(save_state):
        with open(save_state) as f:
            contents = load(f)

        info = contents["info"]
        secs_passed = info["time_spent"]
        minutes = str(secs_passed // 60).zfill(2)
        seconds = str(secs_passed % 60).zfill(2)
        time_passed = f"Time: {minutes}:{seconds}"
        turn_number = f"Turns: {info['turn_number']}"
        current_time = f"{info['current_time']}"
        return (time_passed, turn_number, current_time)

    @classmethod
    def load_save_menu(cls):
        if not len(Game.menus):
            Game.init_menu()
        if Game.current_menu[:15] == "delete_confirm_":
            menu = Game.menus[Game.current_menu]
            Game.current_menu = menu.update()
            menu.draw_small_text()
            return "load_save"

        menu, contents = Game.menus[Game.current_menu]
        menu_surf, menu_rect = contents["menu_surf"]

        menu_surf.fill((5,123,140))
        redirect = menu.update()
        if redirect == "select_menu": return "select_menu"
        if redirect: Game.current_menu = redirect

        if contents.get("surfs"):
            for i, (slot_surf, slot_rect) in enumerate(contents["surfs"]):
                slot_surf.fill((4,103,117))
                for text_surf, text_rect in contents["text"][(i*3):(i*3)+3]:
                    slot_surf.blit(text_surf, text_rect)
                menu_surf.blit(slot_surf, slot_rect)

            screen.blit(menu_surf, menu_rect)
            for i, button in enumerate(contents["buttons"]):
                button.draw_outline()
                redirect = button.update()
                if redirect: return redirect
        else:
            screen.blit(menu_surf, menu_rect)
            screen.blit(Game.empty_message, Game.empty_message_rect)

        Game.back_button.draw_outline()
        redirect = Game.back_button.update()
        if redirect: return redirect

        return "load_save"

    @classmethod
    def load_save(cls, id):
        file_name = f"game_save/pycheckers_save_{id}.json"
        if file_name in glob("game_save/*json"):
            with open(file_name, "r") as f:
                contents = load(f)
                for list in ("beige_pieces", "red_pieces"):
                    contents[list] = {(int(k[1]), int(k[4])):v for k, v in contents[list].items()}
        Game.current_game = Board(width, height, contents["current_turn"])
        Game.current_game.load_info(contents)
        Game.current_game.set_game_interface(Game.interface)
        Game.interface.set_board(Game.current_game)
        return "select_menu"

    def make_delete_menu(save_state, menu_name, previous_menu):
        confirm_text = "Are you sure you want to delete this save file? (This will delete the save file in the game folder)."
        delete_menu =  Menu(name=menu_name, button_names=["Delete", "Back"], redirects=[previous_menu, previous_menu], text="Deleting Game", width=width, height=height, small_text=confirm_text)

        def delete_function(save_state):
            def delete():
                try:
                    remove(save_state)
                except:
                    print("Something went Wrong while deleting the file, try again")
                    exit()
                finally:
                    Game.menus = {}
                    Game.init_menu()
                    return previous_menu
            return delete
        delete_menu.button_list[0].set_onclick(delete_function(save_state))
        return delete_menu

    @classmethod
    def save_current_game(cls):
        Game.menus = {}
        info = Game.current_game.get_save_info()
        file_id = len(glob("game_save/*"))
        save_name = f"pycheckers_save_{file_id}.json"
        with open(f"game_save/{save_name}", "w") as f:
            dump(info, f)

    @classmethod
    def create_game(cls):
        Game.current_game = Board(width, height, Game.first_player)
        Game.current_game.click_queue = [True, True]
        Game.current_game.set_game_interface(Game.interface)
        Game.interface.set_board(Game.current_game)

    @classmethod
    def delete_current_game(cls):
        Game.current_game = []
