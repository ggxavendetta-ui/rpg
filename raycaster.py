import pygame
import math
import settings # Обязательно импортируем сам модуль

def draw_raycasting(screen, player):
    W, H = screen.get_size()
    screen.fill(settings.SKY, (0, 0, W, H // 2))
    screen.fill(settings.FLOOR, (0, H // 2, W, H // 2))

    start_angle = player.angle - settings.HALF_FOV
    delta_angle = settings.FOV / settings.NUM_RAYS
    scale = math.ceil(W / settings.NUM_RAYS)

    for ray in range(settings.NUM_RAYS):
        sin_a, cos_a = math.sin(start_angle), math.cos(start_angle)
        
        for depth in range(1, settings.MAX_DEPTH, 2):
            tx, ty = player.x + cos_a * depth, player.y + sin_a * depth
            
            if settings.MAP[int(ty // settings.TILE_SIZE)][int(tx // settings.TILE_SIZE)] == 1:
                dist = depth * math.cos(player.angle - start_angle)
                dist = max(dist, 0.1)
                proj_height = (settings.TILE_SIZE * 600) / dist
                
                # Рассчет X координаты на текстуре
                x_tile, y_tile = tx % settings.TILE_SIZE, ty % settings.TILE_SIZE
                wall_x = x_tile if abs(y_tile % settings.TILE_SIZE) > 2 else y_tile
                pixel_x = int((wall_x * settings.TEXTURE_SIZE) / settings.TILE_SIZE) % settings.TEXTURE_SIZE

                # РИСУЕМ ТЕКСТУРУ
                try:
                    # Берем текстуру ИМЕННО из settings
                    column = settings.WALL_TEXTURE.subsurface(pixel_x, 0, 1, settings.TEXTURE_SIZE)
                    column = pygame.transform.scale(column, (scale, int(proj_height)))
                    screen.blit(column, (ray * scale, H // 2 - int(proj_height) // 2))
                except:
                    pygame.draw.rect(screen, settings.GRAY, (ray * scale, H // 2 - int(proj_height) // 2, scale, int(proj_height)))
                break
        start_angle += delta_angle