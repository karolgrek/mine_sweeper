import pygame

from uncover import CellStatus

MENU_PICTURE_FILE = "data/menu_pic.png"

UNKNOWN = -1
BACKGROUND = (217, 217, 217)
TILE_UNKNOWN = (0, 128, 0)
TILE_EXPLODED = (128, 0, 0)
TILE_HIGHLIGHTED = (255, 165, 0)
TILE_TEXT = [
    BACKGROUND,
    (0, 0, 255),
    (0, 129, 0),
    (255, 19, 0),
    (0, 0, 131),
    (129, 5, 0),
    (42, 148, 148),
    (0, 0, 0),
    (128, 128, 128)
]

def draw_text(screen, text, y, width, font_size, scale=1.0, center=True):
    font = pygame.font.SysFont("system", int(font_size * scale))
    surface = font.render(text, True, (0, 0, 0))
    rect = surface.get_rect()
    rect.center = (width // 2, y) if center else (10, y)
    screen.blit(surface, rect)

def draw_menu(screen, font_size, username):
    screen.fill(BACKGROUND)
    width, height = screen.get_size()
    draw_text(screen, "Welcome to my lil humble Minesweeper!", 50, width, font_size, 2)
    draw_text(screen, "made by Karol Grek", 100, width, font_size, 0.8)
    draw_text(screen, "Enter username : >" + username + "<", 180, width, font_size, 1.5)
    img = pygame.image.load(MENU_PICTURE_FILE).convert_alpha()
    img = pygame.transform.smoothscale(img, (400, 250)) 
    img_rect = img.get_rect(center=(width // 2, 350))
    screen.blit(img, img_rect)
    draw_text(screen, "Press F2 to reset local user-data | Press F1 to Quit", height - 20, width, font_size, 0.8)

def draw_ask_reset(screen, font_size, username):
    screen.fill(BACKGROUND)
    width, height = screen.get_size()
    draw_text(screen, "Welcome to my lil humble Minesweeper!", 50, width, font_size, 2)
    draw_text(screen, "made by Karol Grek", 100, width, font_size, 0.8)
    draw_text(screen, "Enter username : >" + username + "<", 180, width, font_size, 1.5)
    img = pygame.image.load(MENU_PICTURE_FILE).convert_alpha()
    img = pygame.transform.smoothscale(img, (400, 250))  
    img_rect = img.get_rect(center=(width // 2, 350))
    screen.blit(img, img_rect)
    draw_text(screen, "Press F2 to reset local user-data | Press F1 to Quit", height - 20, width, font_size, 0.8)
    draw_text(screen, "Are you SURE to DELETE ALL user data?", 300, width, font_size, 2)
    draw_text(screen, "Press Y to confirm", 340, width, font_size, 1.5)
    draw_text(screen, "Press N to cancel", 380, width, font_size, 1.5)

def draw_mode_selection(screen, font_size):
    screen.fill(BACKGROUND)
    width, height = screen.get_size()
    draw_text(screen, "Select Game Mode", 50, width, font_size, 2)
    draw_text(screen, "Press 1 for: Hardcore", 100, width, font_size, 1.8)
    draw_text(screen, "You step on a mine, you lose", 130, width, font_size)
    draw_text(screen, "Press 2 for: Peaceful", 200, width, font_size, 1.8)
    draw_text(screen, "You step on a mine, you lose 10 points, and continue", 250, width, font_size)
    draw_text(screen, "Press F1 to quit", height - 20, width, font_size, 0.8)

def draw_mode_selection_known_user(screen, font_size, username, lvl_hard, score_hard, lvl_peace, score_peace):
    screen.fill(BACKGROUND)
    width, height = screen.get_size()
    draw_text(screen, f"Welcome back {username}!", 50, width, font_size, 2)
    if lvl_hard == 0:
        draw_text(screen, "Press 1 to start new game Hardcore", 100, width, font_size, 1.8)
    else:
        draw_text(screen, "Press 1 to continue playing Hardcore", 100, width, font_size, 1.8)
        draw_text(screen, f"Level: {lvl_hard} | Score: {score_hard}", 130, width, font_size, 1.5)
    if lvl_peace == 0:
        draw_text(screen, "Press 2 to start new game Peaceful", 200, width, font_size, 1.8)
    else:
        draw_text(screen, "Press 2 to continue playing Peaceful", 200, width, font_size, 1.8)
        draw_text(screen, f"Level: {lvl_peace} | Score: {score_peace}", 230, width, font_size, 1.5)
    draw_text(screen, "Press F1 to quit", height - 20, width, font_size, 0.8)


def draw_game(screen, game, width, height, cell_size, font, show_mines, level, name, highscore, saved_score, highlighted):
    screen.fill(BACKGROUND)
     #* off set to center the board (same as in handle_click)
    screen_width, screen_height = screen.get_size()
    board_width_px = width * cell_size
    board_height_px = height * cell_size
    offset_x = (screen_width - board_width_px) // 2
    offset_y = (screen_height - board_height_px) // 2
    #*
    for y in range(height):
        for x in range(width):
            rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size)
            val = game.status[y][x]


            if game.status[y][x] == CellStatus.EXPLODED:
                color = TILE_EXPLODED
            elif show_mines and (x, y) in game.mines:
                color = TILE_EXPLODED
            elif val == UNKNOWN and (x,y) in highlighted:
                color = TILE_HIGHLIGHTED
            elif val == UNKNOWN:
                color = TILE_UNKNOWN
            else:
                color = BACKGROUND

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            if val >= 0:
                txt = font.render(str(val), True, TILE_TEXT[val])
                screen.blit(txt, txt.get_rect(center=rect.center))
    if not name:    
        draw_text(screen,
        (
        f"Your Score: {game.score} | Level: {level} | "
        f"Highscore not yet set"
        ),
        10, screen_width, font.get_height(), 1.5)
    else:
        draw_text(screen,
        (
        f"Your Score: {saved_score + game.score} | Level: {level} | "
        f"Highscore: Player: >{name}< Score: {highscore}"
        ),
        10, screen_width, font.get_height(), 1.5)
    draw_text(screen, "Press F1 to save level and quit", 550, screen_width, font.get_height())


def draw_game_over(screen, font_size, username):
    width, height = screen.get_size()
    draw_text(screen, "Game Over!", height // 2, width, font_size, 3)
    draw_text(screen, f"Press R to restart as <", height // 2 + 50, width, font_size, 2)
    draw_text(screen, f"> {username} <", height // 2 + 100, width, font_size, 2)
    draw_text(screen, "or press N to start new game", height // 2 + 150, width, font_size, 2)

def draw_win_screen(screen, font_size, level, username):
    width, height = screen.get_size()
    draw_text(screen, "You win!", height // 2, width, font_size, 3)
    draw_text(screen, f"Press C to continue to level {level + 1} as" , height // 2 + 50, width, font_size, 2)
    draw_text(screen, f"> {username} <", height // 2 + 100, width, font_size, 2)
    draw_text(screen, "or press N to start new game", height // 2 + 150, width, font_size, 2)
