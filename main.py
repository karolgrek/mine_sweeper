import pygame
import sys
import os
import random
from uncover import Minesweeper, GameStatus
from draw import (
    draw_menu,
    draw_ask_reset,
    draw_mode_selection,
    draw_game,
    draw_game_over,
    draw_win_screen,
    draw_mode_selection_known_user
)

PLAYERS_FILE = "data/players.txt"
HIGHSCORES_FILE = "data/highscores.txt"

#constants
INIT_WIDTH = 7
INIT_HEIGHT = 5
INIT_MINES = 5
CELL_SIZE = 40
FONT_SIZE = 28
BACKGROUND = (217, 217, 217)
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

HARDCORE = "hardcore"
PEACEFUL = "peaceful"

def load_players():
    players = {}
    if not os.path.exists(PLAYERS_FILE):
        open(PLAYERS_FILE, "w").close()
    with open(PLAYERS_FILE, "r") as f:
        for line in f:
            name, lvl_p, score_p, _, lvl_h, score_h, _ = line.strip().split(";")
            players[name] = {
                PEACEFUL: (int(lvl_p), int(score_p)),
                HARDCORE: (int(lvl_h), int(score_h)),
            }
    return players


def save_players(players):
    with open(PLAYERS_FILE, "w") as f:
        for name, modes in players.items():
            lvl_p, score_p = modes[PEACEFUL]
            lvl_h, score_h = modes[HARDCORE]
            f.write(f"{name};{lvl_p};{score_p};{PEACEFUL};{lvl_h};{score_h};{HARDCORE}\n")


class Player:
    def __init__(self, name: str, cache: dict):
        self.name = name
        self.level = 0
        self.total_score = 0
        self.mode = None
        self.cache = cache

    def load(self):
        if self.name in self.cache:
            return True
        return False

    def sync_from_cache(self):
        if self.name not in self.cache:
            return
        lvl_p, score_p = self.cache[self.name][PEACEFUL]
        lvl_h, score_h = self.cache[self.name][HARDCORE]
        if self.mode == PEACEFUL:
            self.level, self.total_score = lvl_p, score_p
        else:
            self.level, self.total_score = lvl_h, score_h

    def save(self, score):
        if self.name not in self.cache:
            self.cache[self.name] = {PEACEFUL: (0, 0), HARDCORE: (0, 0)}
        self.cache[self.name][self.mode] = (self.level, score)
        save_players(self.cache)


class GameSession:
    def __init__(self, player: Player, game_class):
        self.level = player.level
        self.game_class = game_class
        self.width = 16
        self.height = 10
        self.mines_count = 25
        self.width, self.height, self.mines_count = self.level_settings()
        self.game = self.generate_game()

    def level_settings(self):

        if self.level <= 6:
            width = INIT_WIDTH + self.level * 2
            height = INIT_HEIGHT + self.level * 1
            mines_count = INIT_MINES + self.level * 5
        else:
            width = 20
            height = 12 
            if self.level <= 8:
                self.mines_count += 5
            elif self.level <= 12:
                self.mines_count += 2
            elif self.level <= 15:
                self.mines_count += 1

        return width, height, mines_count

    def generate_game(self):
        self.level_settings()
        positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        mines = set(random.sample(positions, self.mines_count))
        return self.game_class(self.width, self.height, mines)


class MinesweeperUI:
    def __init__(self, game_class):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.players_cache = load_players()
        self.player = Player("", self.players_cache)
        self.game_class = game_class
        self.session = None
        self.phase = "menu"
        self.highlighted = set()
        self.screen = pygame.display.set_mode((22 * CELL_SIZE, 14 * CELL_SIZE))
        self.font = pygame.font.SysFont("system", FONT_SIZE)

    def draw_current_phase(self):
        if self.phase == "menu":
            draw_menu(self.screen, FONT_SIZE, self.player.name)
        elif self.phase == "ask_reset":
            draw_ask_reset(self.screen, FONT_SIZE, self.player.name)
        elif self.phase == "mode_selection":
            draw_mode_selection(self.screen, FONT_SIZE)
        elif self.phase == "mode_selection_known_user":
            p = self.players_cache[self.player.name]
            level_h, score_h = p[HARDCORE]
            level_p, score_p = p[PEACEFUL]
            draw_mode_selection_known_user(
                self.screen,
                FONT_SIZE,
                self.player.name,
                level_h,
                score_h,
                level_p,
                score_p,
            )
        elif self.phase in {"playing", "stepped_on_mine_peaceful"}:
            self.draw_game()
        elif self.phase == "victory_screen":
            self.draw_game(True)
            draw_win_screen(self.screen, FONT_SIZE, self.player.level, self.player.name)
        elif self.phase == "game_over":
            self.draw_game(True)
            draw_game_over(self.screen, FONT_SIZE, self.player.name)

    def draw_game(self, show_mines=False):
        name, highscore = "", 0
        if os.path.exists(HIGHSCORES_FILE):
            with open(HIGHSCORES_FILE, "r") as f:
                for line in f:
                    name, highscore = line.strip().split(";")
        draw_game(
            self.screen,
            self.session.game,
            self.session.width,
            self.session.height,
            CELL_SIZE,
            self.font,
            show_mines,
            self.player.level,
            name,
            int(highscore),
            self.player.total_score,
            self.highlighted,
        )

    def start_game(self):
        self.session = GameSession(self.player, self.game_class)
        self.phase = "playing"

    def handle_click(self, button, x, y):
        sw, sh = self.screen.get_size()
        bw = self.session.width * CELL_SIZE
        bh = self.session.height * CELL_SIZE
        offset_x = (sw - bw) // 2
        offset_y = (sh - bh) // 2
        if button == RIGHT_MOUSE_BUTTON:
            hx, hy = (x - offset_x) // CELL_SIZE, (y - offset_y) // CELL_SIZE
            if (hx, hy) in self.highlighted:
                self.highlighted.remove((hx, hy))
            else:
                self.highlighted.add((hx, hy))
            return
        if not (offset_x <= x < offset_x + bw and offset_y <= y < offset_y + bh):
            return
        cx, cy = (x - offset_x) // CELL_SIZE, (y - offset_y) // CELL_SIZE
        self.session.game.uncover(cx, cy)
        if self.player.mode == HARDCORE and (cx, cy) in self.session.game.mines:
            self.phase = "game_over"
        elif self.player.mode == PEACEFUL and (cx, cy) in self.session.game.mines:
            self.session.game.score -= 10
            self.session.game.uncover(cx, cy)
        elif self.session.game.game_status == GameStatus.GAME_WON:
            self.phase = "victory_screen"

    def handle_key(self, event):
        handlers = {
            "menu": self.menu_key,
            "ask_reset": self.ask_reset_key,
            "mode_selection": self.mode_selection_key,
            "mode_selection_known_user": self.known_user_key,
            "victory_screen": self.victory_key,
            "game_over": self.game_over_key,
        }
        if self.phase in handlers:
            handlers[self.phase](event)

    def menu_key(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.player.name = self.player.name[:-1]
        elif event.key == pygame.K_RETURN and self.player.name:
            if self.player.load():
                self.phase = "mode_selection_known_user"
            else:
                self.phase = "mode_selection"
        elif len(self.player.name) <= 20 and \
             len(event.unicode) == 1 and \
             event.unicode.isprintable() and \
             event.unicode != ";":
            self.player.name += event.unicode
        elif event.key == pygame.K_F2:
            self.phase = "ask_reset"


    def ask_reset_key(self, event):
        if event.key == pygame.K_y:
            open(PLAYERS_FILE, "w").close()
            open(HIGHSCORES_FILE, "w").close()
            self.players_cache.clear()
            self.player = Player("", self.players_cache)
            self.phase = "menu"
        elif event.key == pygame.K_n:
            self.phase = "menu"

    def mode_selection_key(self, event):
        if event.key == pygame.K_1:
            self.player.mode = HARDCORE
            self.start_game()
        elif event.key == pygame.K_2:
            self.player.mode = PEACEFUL
            self.start_game()

    def known_user_key(self, event):
        p = self.players_cache[self.player.name]
        level_h, score_h = p[HARDCORE]
        level_p, score_p = p[PEACEFUL]
        if event.key == pygame.K_1:
            self.player.mode = HARDCORE
            self.player.level, self.player.total_score = level_h, score_h
            self.start_game()
        elif event.key == pygame.K_2:
            self.player.mode = PEACEFUL
            self.player.level, self.player.total_score = level_p, score_p
            self.start_game()

    def victory_key(self, event):
        if event.key == pygame.K_c or event.key == pygame.K_n:
            self.player.total_score += self.session.game.score
            self.update_highscore()
            self.player.level += 1
            self.player.save(self.session.game.score)
            if event.key == pygame.K_c:
                self.highlighted.clear()
                self.start_game()
            elif event.key == pygame.K_n:
                self.phase = "menu"
                self.highlighted.clear()
                self.player = Player("", self.players_cache)

    def game_over_key(self, event):
        self.update_highscore()
        self.player.total_score = 0
        self.player.level = 0
        self.player.save(0)
        self.player.save(self.session.game.score)
        if event.key == pygame.K_r:
            self.phase = "mode_selection"
        elif event.key == pygame.K_n:
            self.phase = "menu"
            self.player = Player("", self.players_cache)

    def update_highscore(self):
        if not os.path.exists(HIGHSCORES_FILE):
            open(HIGHSCORES_FILE, "w").close()
        highscore = 0
        if os.path.exists(HIGHSCORES_FILE):
            with open(HIGHSCORES_FILE, "r") as f:
                for line in f:
                    _, score = line.strip().split(";")
                    highscore = int(score)
        if self.session.game.score > highscore:
            with open(HIGHSCORES_FILE, "w") as f:
                f.write(f"{self.player.name};{self.session.game.score}\n")

    def game_loop(self):
        while True:
            self.screen.fill(BACKGROUND)
            self.draw_current_phase()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.handle_key(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.phase == "playing":
                    self.handle_click(event.button, *event.pos)

if __name__ == "__main__":
    ui = MinesweeperUI(Minesweeper)
    ui.game_loop()
