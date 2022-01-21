from checkers import width, height
from checkers.surfaces import *
from checkers.MenuButton import MenuButton
from datetime import datetime
from time import time

class Board:
    def __init__(self, width, height, first_player):
        self.game_won = False
        self.current_turn = first_player
        self.turn_counter = 0
        self.red_pieces_counter = 12
        self.beige_pieces_counter = 12

        self.time_passed = "00:00"
        self.accumulated_time = 0
        self.current_time = pygame.time.get_ticks()
        self.init_surfaces(width, height)
        self.init_board_elements()

        self.click_queue = [None, None]
        self.selected_piece = None
        self.highlight_squares = []
        self.target_pieces = {}

    def load_info(self, info):
        self.current_time = None
        self.turn_counter = info["info"]["turn_number"]
        self.accumulated_time = info["info"]["time_spent"]
        self.beige_pieces = info["beige_pieces"]
        self.red_pieces = info["red_pieces"]
        self.red_pieces_counter = len([x for x in self.red_pieces.values() if x])
        self.beige_pieces_counter = len([x for x in self.beige_pieces.values() if x])

    def get_save_info(self):
        current_time = datetime.now().strftime("%d %b %H:%M")
        turn_number = self.turn_counter
        current_turn = self.current_turn
        beige_pieces = {str(k): v for k, v in self.beige_pieces.items()}
        red_pieces = {str(k): v for k, v in self.red_pieces.items()}
        time_spent = self.accumulated_time
        info = {"current_time": current_time, "turn_number": turn_number, "time_spent": time_spent}
        save_info = {"info": info, "current_turn": current_turn, "beige_pieces":beige_pieces, "red_pieces":red_pieces}
        return save_info

    def reset_current_time(self):
        self.current_time = None

    def update_time(self):
        if self.current_time is None:
            self.current_time = pygame.time.get_ticks() - (self.accumulated_time * 1000)
        secs_passed = (pygame.time.get_ticks() - self.current_time) // 1000
        minutes = str(secs_passed // 60).zfill(2)
        seconds = str(secs_passed % 60).zfill(2)
        self.accumulated_time = secs_passed
        self.time_passed = f"{minutes}:{seconds}"

    def set_game_interface(self, interface):
        self.interface = interface
        if self.current_turn != self.interface.current_player:
            self.interface.toggle_pointer()

    def check_win(self):
        if not any(self.red_pieces.values()) or not any(self.beige_pieces.values()):
            winner = "Player 1 Wins!" if self.current_turn == "player_1" else "Player 2 Wins!"
            self.interface.win_surfs_init(winner, self.turn_counter, self.time_passed)
            self.mouse_pos = (-100,-100)
            self.game_won = True

        for color in ("beige", "red"):
            ally_pieces = self.beige_pieces if color == "beige" else self.red_pieces
            enemy_pieces = self.red_pieces if color == "beige" else self.beige_pieces
            moves_left = False
            for ally_piece, enemy_piece in zip(ally_pieces.items(), enemy_pieces.items()):
                if moves_left:
                    break
                if ally_piece[1]:
                    inverter = 1 if color == "red" else -1
                    x, y = ally_piece[0]
                    if ally_piece[1].split("_")[1] == "knight":
                        vacant_spaces = [(x+1, y+inverter), (x-1, y+inverter)]
                    else:
                        vacant_spaces = [(x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)]
                    for space in vacant_spaces:
                        if min(space) >= 0 and max(space) <= 7:
                            if not any((ally_pieces[space], enemy_pieces[space])):
                                moves_left = True
                            if enemy_pieces[space]:
                                x_offset = space[0] - ally_piece[0][0]
                                y_offset = space[1] - ally_piece[0][1]
                                behind_pos = (space[0]+x_offset, space[1]+y_offset)
                                if min(behind_pos) >= 0 and max(behind_pos) <= 7:
                                    if not any((ally_pieces[behind_pos], enemy_pieces[behind_pos])):
                                        moves_left = True
            if moves_left == False:
                winner = "Player 1 Wins!" if color == "beige" else "Player 2 Wins!"
                self.interface.win_surfs_init(winner, self.turn_counter, self.time_passed)
                self.mouse_pos = (-100,-100)
                self.game_won = True

    def init_board_elements(self):
        self.red_pieces = {(i, j):"red_knight" if j <= 2 else None
                            for i in range(8) for j in range(8) if (i+j) % 2}
        self.beige_pieces = {(i, j):"beige_knight" if j >= 5 else None
                            for i in range(8) for j in range(8) if (i+j) % 2}
        x_size, y_size = tuple(map(lambda x: x/8, self.board_rect.size))
        self.square_size = (x_size, y_size)
        self.squares = [pygame.Rect(j*x_size, i*y_size, x_size, y_size) for i in range(8) for j in range(8)]

    def init_surfaces(self, width, height):
        self.board_surf = pygame.Surface((width - width/3.5, height - height/3.5))
        self.board_surf.fill((226,206,178))

        self.board_rect = self.board_surf.get_rect(center=(width/2, height/2))
        inner_board_size = (width - width/4.5, height - height/4.5)
        self.frame_rect = pygame.Rect((0,0), inner_board_size)
        self.frame_rect.center = (width/2, height/2)

    def get_mouse_input(self):
        self.click_queue.pop(0)
        self.click_queue.append(pygame.mouse.get_pressed()[0])
        mouse_pos = pygame.mouse.get_pos()
        x, y = self.board_rect.topleft
        self.mouse_pos = (mouse_pos[0]-x, mouse_pos[1]-y)

    def draw_numbers(self):
        size = self.board_rect.size
        board_x, board_y = self.board_rect.topleft
        x_size, y_size = (size[0]/8, size[1]/8)
        for i in range(8):
            num = smaller_font.render(str(i), True, (0,0,0))
            screen.blit(num, ((board_x+x_size/2)+(i*x_size), board_y-(height/25)))
        for j in range(8):
            num = smaller_font.render(str(j), True, (0,0,0))
            screen.blit(num, (board_x-(width/40), board_y+(y_size*j)))

    def move_pieces(self):
        color = "beige" if self.current_turn == "player_1" else "red"
        ally_pieces = self.beige_pieces if color == "beige" else self.red_pieces
        enemy_pieces = self.red_pieces if color == "beige" else self.beige_pieces

        sqr_x, sqr_y = self.square_size
        if not self.click_queue[0] and self.click_queue[1]:
            highlight_rects = [pygame.Rect(x_pos*sqr_x, y_pos*sqr_y,
            sqr_x, sqr_y) for x_pos, y_pos in self.highlight_squares]

            for square in highlight_rects:
                if square.collidepoint(self.mouse_pos):
                    moved_piece = self.selected_piece[0]
                    destination = round(square.topleft[0]/sqr_x), round(square.topleft[1]/sqr_y)
                    piece_type = self.selected_piece[1]

                    if self.target_pieces.get(destination):
                        for target in self.target_pieces[destination]:
                            enemy_pieces[target] = None

                    if destination[1] in (0, 7):
                        piece_type = f"{color}_queen"

                    ally_pieces[(destination)] = piece_type
                    ally_pieces[moved_piece] = None
                    self.current_turn = {"player_1":"player_2",
                                        "player_2":"player_1"}[self.current_turn]
                    self.interface.toggle_pointer()
                    self.turn_counter += 1
                    self.check_win()
                    self.red_pieces_counter = len([x for x in self.red_pieces.values() if x])
                    self.beige_pieces_counter = len([x for x in self.beige_pieces.values() if x])
            self.highlight_squares = self.selected_piece = []
            self.target_pieces = {}

    def update_pieces(self):
        for piece in zip(self.red_pieces.items(), self.beige_pieces.items()):
            if all(piece[0]) or all(piece[1]):
                active_piece = piece[0] if piece[0][1] else piece[1]
                piece_surf = {"red_knight":red_knight,"beige_knight":beige_knight,
                "red_queen":red_queen, "beige_queen":beige_queen}[active_piece[1]]
                x_pos, y_pos = active_piece[0]
                x_size, y_size = self.square_size
                self.get_pieces_input(x_pos, y_pos, active_piece[1])
                self.board_surf.blit(piece_surf, ((x_pos*x_size, y_pos*y_size)))

    def draw_grid(self):
        for i, square in enumerate(self.squares):
            if (i+(i//8)) % 2:
                color = (38,23,26)
                if square.collidepoint(self.mouse_pos):
                    color = (255,255,255)
            if not (i+(i//8)) % 2:
                color = (226,206,178)
                if square.collidepoint(self.mouse_pos):
                    color = (255,255,255)

            if self.selected_piece:
                x, y = square.topleft
                size_x, size_y = self.square_size
                square_board_pos = (round(x/size_x), round(y/size_y))
                if self.selected_piece[0] == square_board_pos:
                    color = (198,209,69)
                    if square.collidepoint(self.mouse_pos):
                        color = (213,237,63)
                if square_board_pos in self.highlight_squares:
                    color = (213,237,63)
                    if square.collidepoint(self.mouse_pos):
                        color = (236,249,157)

            pygame.draw.rect(self.board_surf, color, square)

    def search_captures(self, piece_pos, enemy_pos, game_pieces, path=None):
        if path == None:
            path = []
        _, enemy_pieces = game_pieces
        x_offset = enemy_pos[0] - piece_pos[0]
        y_offset = enemy_pos[1] - piece_pos[1]
        behind_enemy_pos = (enemy_pos[0]+x_offset, enemy_pos[1]+y_offset)
        if max(behind_enemy_pos) <= 7 and min(behind_enemy_pos) >= 0:
            if not any([pieces[behind_enemy_pos] for pieces in game_pieces]):
                self.highlight_squares.append(behind_enemy_pos)
                self.target_pieces[behind_enemy_pos] = path
                path.append(enemy_pos)
                x, y = behind_enemy_pos
                vacant_spaces = [(x+1,y+1),(x-1,y+1),(x+1,y-1),(x-1,y-1)]
                vacant_spaces.remove((enemy_pos[0], enemy_pos[1]))
                for space in vacant_spaces[:]:
                    if max(space) <= 7 and min(space) >= 0:
                        if not enemy_pieces[space]:
                            vacant_spaces.remove(space)
                for space in vacant_spaces:
                    self.search_captures(behind_enemy_pos, space, game_pieces, path[:])

    def get_highlight_squares(self, x_pos, y_pos, color, type):
        inverter = 1 if color == "red" else -1
        ally_pieces = self.red_pieces if color == "red" else self.beige_pieces
        enemy_pieces = self.beige_pieces if color == "red" else self.red_pieces
        game_pieces = (ally_pieces, enemy_pieces)

        self.highlight_squares = [(x_pos-1, y_pos+(1 * inverter)),
                                (x_pos+1, y_pos+(1 * inverter))]

        if type == "queen":
            self.highlight_squares += [(x_pos-1, y_pos-(1 * inverter)),
                                     (x_pos+1, y_pos-(1 * inverter))]

        for pos in self.highlight_squares[:]:
            if min(pos) == -1 or max(pos) == 8 or ally_pieces[pos]:
                self.highlight_squares.remove(pos)
            elif enemy_pieces[pos]:
                x, y = pos
                self.search_captures(self.selected_piece[0], (x, y), game_pieces)
                self.highlight_squares.remove(pos)

    def get_pieces_input(self, x_pos, y_pos, name):
        color = "beige" if name[0] == "b" else "red"
        type = "knight" if name[-1] == "t" else "queen"
        current_turn = "beige" if self.current_turn == "player_1" else "red"
        x, y = self.square_size
        if not self.click_queue[0] and self.click_queue[1]:
            hovered_square = pygame.Rect(x_pos*x, y_pos*y, x, y)
            if hovered_square.collidepoint(self.mouse_pos):
                if color == current_turn:
                    self.selected_piece = ((x_pos, y_pos), name)
                    self.get_highlight_squares(x_pos, y_pos, color, type)

    def update(self):
        if not self.game_won:
            self.update_time()
            self.get_mouse_input()
            self.move_pieces()
        pygame.draw.rect(screen, (226,206,178), self.frame_rect)
        screen.blit(self.board_surf,self.board_rect)
        pygame.draw.rect(screen, (38,23,26), self.board_rect, 5)
        self.draw_grid()
        self.update_pieces()
        self.draw_numbers()
