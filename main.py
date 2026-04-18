import os
import sys
import json
import pygame

# --- ИСПРАВЛЕНИЕ ПУТЕЙ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

try:
    import settings
    from settings import *
except ImportError:
    print(f"Ошибка: settings.py не найден в {BASE_DIR}")
    sys.exit()

from player import Player
from raycaster import draw_raycasting
from minimap import draw_minimap
import ui

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

# Установка Full HD из настроек
WIDTH, HEIGHT = settings.RESOLUTIONS["1920x1080"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Engine 2.5D - Final Build v2")
clock = pygame.time.Clock()

# Оптимизация текстуры (после создания окна)
if settings.WALL_TEXTURE:
    try:
        settings.WALL_TEXTURE = settings.WALL_TEXTURE.convert()
    except:
        pass

# --- ОБЪЕКТЫ И ПЕРЕМЕННЫЕ ---
player = Player()
game_state = "MENU" 
game_started = False
selected_class = "ВОИН"

def get_slot_info(slot):
    filename = f"save_slot_{slot}.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                s = data["stats"]
                return f"{s['Class']} ({s['Level']} ур.)"
        except: return "Ошибка данных"
    return "Пусто"

# --- ГЛАВНЫЙ ЦИКЛ ---
while True:
    W, H = screen.get_size()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "GAME":
                    game_state = "MENU"
                elif game_state == "MENU" and game_started:
                    game_state = "GAME"
                elif game_state in ["CLASS_SELECT", "SAVE_MENU", "LOAD_MENU"]:
                    game_state = "MENU"

    screen.fill(BLACK)

    # 1. МЕНЮ (ГЛАВНОЕ И ПАУЗА)
    if game_state == "MENU":
        ui.draw_text(screen, "ПАУЗА" if game_started else "ГЛАВНОЕ МЕНЮ", ui.font_main, GOLD, W//2, 100, center=True)
        
        bx, bw, bh = W//2 - 150, 300, 50
        
        # Кнопка: Продолжить / Новая игра
        txt = "ПРОДОЛЖИТЬ" if game_started else "НОВАЯ ИГРА"
        if ui.draw_button(screen, txt, bx, 200, bw, bh, (0, 80, 0), (0, 120, 0)):
            game_state = "GAME" if game_started else "CLASS_SELECT"
        
        # Кнопка: Сохранить
        if game_started:
            if ui.draw_button(screen, "СОХРАНИТЬ", bx, 265, bw, bh, (0, 80, 80), (0, 120, 120)):
                game_state = "SAVE_MENU"
        
        # Кнопка: Загрузить
        if ui.draw_button(screen, "ЗАГРУЗИТЬ", bx, 330, bw, bh, (80, 80, 0), (120, 120, 0)):
            game_state = "LOAD_MENU"

        # Кнопка: В ГЛАВНОЕ МЕНЮ (Сброс текущей игры)
        if game_started:
            if ui.draw_button(screen, "В ГЛАВНОЕ МЕНЮ", bx, 395, bw, bh, (60, 60, 60), (90, 90, 90)):
                game_started = False
                game_state = "MENU"

        # Кнопка: ВЫХОД (Закрыть приложение)
        if ui.draw_button(screen, "ВЫХОД", bx, 460, bw, bh, (100, 0, 0), (150, 0, 0)):
            pygame.quit(); sys.exit()

    # 2. ИГРОВОЙ ПРОЦЕСС
    elif game_state == "GAME":
        player.move()
        draw_raycasting(screen, player)
        draw_minimap(screen, player)
        
        # Интерфейс игрока
        st = player.stats
        res_col = CLASSES[st['Class']]['res_color']
        ui.draw_text(screen, f"{st['Class']} | LVL: {st['Level']}", ui.font_small, WHITE, 20, H-80, left=True)
        ui.draw_text(screen, f"HP: {st['HP']}", ui.font_small, RED, 20, H-45, left=True)
        ui.draw_text(screen, f"{st['Res_Name']}: {st['RES']}", ui.font_small, res_col, 250, H-45, left=True)
        ui.draw_text(screen, f"FPS: {int(clock.get_fps())}", ui.font_small, GREEN, W - 20, 20)

    # 3. ВЫБОР КЛАССА
    elif game_state == "CLASS_SELECT":
        ui.draw_text(screen, "ВЫБЕРИТЕ ГЕРОЯ", ui.font_main, GOLD, W//2, 80, center=True)
        for i, cls in enumerate(CLASSES.keys()):
            if ui.draw_button(screen, cls, 150, 200 + i*70, 250, 60, (40, 40, 40), CLASSES[cls]['color']):
                selected_class = cls
        ui.draw_class_info(screen, selected_class)
        if ui.draw_button(screen, "НАЧАТЬ ПРИКЛЮЧЕНИЕ", W - 400, H - 120, 350, 70, (0, 100, 0), (0, 150, 0)):
            player.init_class(selected_class)
            game_started = True
            game_state = "GAME"

    # 4. СОХРАНЕНИЯ
    elif game_state in ["SAVE_MENU", "LOAD_MENU"]:
        is_save = (game_state == "SAVE_MENU")
        ui.draw_text(screen, "СЛОТЫ СОХРАНЕНИЙ", ui.font_main, WHITE, W//2, 80, center=True)
        for i in range(1, 4):
            info = get_slot_info(i)
            if ui.draw_button(screen, f"СЛОТ {i}: {info}", W//2-250, 200 + i*80, 500, 60, (30,30,30), (60,60,60)):
                if is_save:
                    with open(f"save_slot_{i}.json", "w") as f: json.dump(player.get_save_data(), f)
                    game_state = "GAME"
                elif info != "Пусто":
                    with open(f"save_slot_{i}.json", "r") as f: player.load_save_data(json.load(f))
                    game_started = True; game_state = "GAME"
        if ui.draw_button(screen, "НАЗАД", W//2-150, H-100, 300, 50, GRAY, (80,80,80)): game_state = "MENU"

    pygame.display.flip()
    
    # ОГРАНИЧЕНИЕ 60 FPS
    clock.tick(60)