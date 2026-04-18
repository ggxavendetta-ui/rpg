import pygame
from settings import WHITE, BLACK, GOLD, GRAY, RED, BLUE, GREEN, YELLOW, CLASSES

# Принудительно задаем цвета, если их нет в settings
LIGHT_GRAY = (180, 180, 180)

pygame.font.init()
# Используем стандартный шрифт, который точно есть в системе
try:
    font_main = pygame.font.SysFont('Arial', 48, bold=True)
    font_small = pygame.font.SysFont('Arial', 24)
except:
    font_main = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 24)

def draw_text(screen, text, font, color, x, y, center=False, left=False):
    img = font.render(str(text), True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    elif left:
        rect.topleft = (x, y)
    else:
        rect.topright = (x, y)
    screen.blit(img, rect)

def draw_button(screen, text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mouse)
    
    current_color = hover_color if is_hover else color
    
    # Рисуем кнопку с закруглением и обводкой
    pygame.draw.rect(screen, current_color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    
    draw_text(screen, text, font_small, WHITE, x + w//2, y + h//2, center=True)
    
    return is_hover and click[0]

def draw_class_info(screen, class_name):
    if class_name not in CLASSES: return
    
    cls = CLASSES[class_name]
    W, H = screen.get_size()
    
    # Смещаем инфо в правую часть экрана
    info_x = W // 2 + 50
    info_y = 200
    
    # Отрисовка описания
    draw_text(screen, f"КЛАСС: {class_name}", font_main, cls["color"], info_x, info_y, left=True)
    draw_text(screen, cls["desc"], font_small, LIGHT_GRAY, info_x, info_y + 60, left=True)
    
    # Отрисовка характеристик
    y_off = 120
    for stat, val in cls["base"].items():
        draw_text(screen, f"{stat}: {val}", font_small, WHITE, info_x, info_y + y_off, left=True)
        y_off += 35