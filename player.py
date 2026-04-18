import pygame
import math
from settings import MAP, TILE_SIZE, CLASSES

class Player:
    def __init__(self):
        self.x, self.y = 150, 150
        self.angle = 0
        self.speed = 4
        self.stats = {}

    def init_class(self, class_name):
        cls = CLASSES[class_name]
        self.stats = {
            "Class": class_name,
            "Level": 1,
            "XP": 0, "Max_XP": 100,
            "Res_Name": cls["res_name"]
        }
        self.stats.update(cls["base"])
        self.stats.update(cls["combat"])

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.angle -= 0.04
        if keys[pygame.K_d]: self.angle += 0.04
        
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        
        if keys[pygame.K_w]:
            if MAP[int((self.y + dy) // TILE_SIZE)][int((self.x + dx) // TILE_SIZE)] == 0:
                self.x += dx
                self.y += dy
        if keys[pygame.K_s]:
            if MAP[int((self.y - dy) // TILE_SIZE)][int((self.x - dx) // TILE_SIZE)] == 0:
                self.x -= dx
                self.y -= dy
# В конец класса Player в файле player.py
    def get_save_data(self):
        return {
            "pos": (self.x, self.y),
            "angle": self.angle,
            "stats": self.stats
        }

    def load_save_data(self, data):
        self.x, self.y = data["pos"]
        self.angle = data["angle"]
        self.stats = data["stats"]