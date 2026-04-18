import pygame
from settings import MAP, TILE_SIZE, WHITE, GRAY, RED, GOLD

def draw_minimap(screen, player):
    # Настройки миникарты
    MAP_SCALE = 0.2  # Коэффициент уменьшения (20% от реального размера)
    OFFSET_X, OFFSET_Y = 20, 20 # Отступ от края экрана
    
    # 1. Рисуем стены
    for row_index, row in enumerate(MAP):
        for col_index, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen, 
                    GRAY, 
                    (OFFSET_X + col_index * TILE_SIZE * MAP_SCALE, 
                     OFFSET_Y + row_index * TILE_SIZE * MAP_SCALE, 
                     TILE_SIZE * MAP_SCALE - 1, 
                     TILE_SIZE * MAP_SCALE - 1)
                )

    # 2. Рисуем игрока
    p_x = OFFSET_X + player.x * MAP_SCALE
    p_y = OFFSET_Y + player.y * MAP_SCALE
    
    pygame.draw.circle(screen, GOLD, (int(p_x), int(p_y)), 5)

    # 3. Рисуем направление взгляда (маленькая линия)
    import math
    line_x = p_x + math.cos(player.angle) * 15
    line_y = p_y + math.sin(player.angle) * 15
    pygame.draw.line(screen, GOLD, (p_x, p_y), (line_x, line_y), 2)