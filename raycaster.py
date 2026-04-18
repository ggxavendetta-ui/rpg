import pygame
import math
from settings import *
import settings # Импортируем модуль для доступа к WALL_TEXTURE

def draw_raycasting(screen, player):
    W, H = screen.get_size()
    
    # Отрисовка неба и пола
    pygame.draw.rect(screen, SKY, (0, 0, W, H // 2))
    pygame.draw.rect(screen, FLOOR, (0, H // 2, W, H // 2))

    ray_angle = player.angle - HALF_FOV
    # Увеличиваем шаг для точности (W / NUM_RAYS)
    scale = W / NUM_RAYS

    for ray in range(NUM_RAYS):
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Вертикали и горизонтали (DDA или упрощенный проход)
        for depth in range(1, MAX_DEPTH, 2):
            tx = player.x + cos_a * depth
            ty = player.y + sin_a * depth

            # Проверка границ карты, чтобы не вылететь с ошибкой
            map_x, map_y = int(tx // TILE_SIZE), int(ty // TILE_SIZE)
            
            if MAP[map_y][map_x] == 1:
                # 1. Убираем эффект рыбьего глаза
                dist = depth * math.cos(player.angle - ray_angle)
                dist = max(dist, 0.0001) # Защита от деления на 0
                
                # 2. Высота стены на экране
                proj_height = (TILE_SIZE / dist) * 800 # 800 - коэффициент проекции
                
                # 3. ВЫЧИСЛЕНИЕ СМЕЩЕНИЯ ТЕКСТУРЫ (offset)
                # Определяем, куда ударился луч: в горизонтальную или вертикальную часть тайла
                x_offset = tx % TILE_SIZE
                y_offset = ty % TILE_SIZE
                
                # Выбираем смещение в зависимости от того, какая грань ближе к точке удара
                if abs(y_offset) < 2 or abs(y_offset - TILE_SIZE) < 2:
                    offset = x_offset
                else:
                    offset = y_offset
                
                # Масштабируем смещение под размер текстуры (256)
                pixel_x = int((offset * TEXTURE_SIZE) / TILE_SIZE) % TEXTURE_SIZE

                # 4. Отрисовка текстурированной полоски
                try:
                    # Вырезаем вертикальную полоску в 1 пиксель из текстуры
                    column = settings.WALL_TEXTURE.subsurface(pixel_x, 0, 1, TEXTURE_SIZE)
                    # Масштабируем полоску под высоту стены на экране
                    column = pygame.transform.scale(column, (math.ceil(scale), int(proj_height)))
                    # Рисуем на экран
                    screen.blit(column, (ray * scale, H // 2 - int(proj_height) // 2))
                except:
                    # Если текстура не загружена, рисуем серый прямоугольник
                    pygame.draw.rect(screen, GRAY, (ray * scale, H // 2 - int(proj_height) // 2, math.ceil(scale), int(proj_height)))
                break
        
        ray_angle += FOV / NUM_RAYS