import pygame
import math
import os

# --- ЦВЕТА ---
WHITE, BLACK, GOLD, GRAY = (255, 255, 255), (0, 0, 0), (255, 215, 0), (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)
RED, BLUE, GREEN, YELLOW = (200, 50, 50), (50, 100, 200), (50, 150, 50), (200, 200, 50)
SKY, FLOOR = (30, 30, 30), (20, 20, 20)

RESOLUTIONS = {"1920x1080": (1920, 1080)}
TILE_SIZE = 100
TEXTURE_SIZE = 256
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ
WALL_TEXTURE = None

def load_wall_texture():
    path = os.path.join(BASE_PATH, 'img', 'wall01.png')
    if os.path.exists(path):
        try:
            return pygame.image.load(path) # Просто загрузка
        except: pass
    
    # Заглушка, если файл не найден
    surf = pygame.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
    surf.fill(GRAY)
    pygame.draw.rect(surf, WHITE, (0,0,256,256), 5)
    return surf

WALL_TEXTURE = load_wall_texture()

MAP = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,0,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300 
MAX_DEPTH = 1200

CLASSES = {
    "ВОИН": {"color": RED, "desc": "Танк.", "res_name": "Ярость", "res_color": RED, "base": {"STR": 12, "END": 12}, "combat": {"HP": 150, "RES": 0, "Level": 1, "Class": "ВОИН"}},
    "РАЗБОЙНИК": {"color": YELLOW, "desc": "ДД.", "res_name": "Энергия", "res_color": YELLOW, "base": {"STR": 6, "DEX": 15}, "combat": {"HP": 100, "RES": 100, "Level": 1, "Class": "РАЗБОЙНИК"}},
    "МАГ": {"color": BLUE, "desc": "Кастер.", "res_name": "Мана", "res_color": BLUE, "base": {"INT": 18, "SPR": 10}, "combat": {"HP": 80, "RES": 200, "Level": 1, "Class": "МАГ"}},
    "ЛУЧНИК": {"color": GREEN, "desc": "РДД.", "res_name": "Энергия", "res_color": YELLOW, "base": {"DEX": 12, "LUK": 8}, "combat": {"HP": 90, "RES": 100, "Level": 1, "Class": "ЛУЧНИК"}}
}