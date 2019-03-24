import pygame

from cultivate.buildings.test_building import TestBuilding
from cultivate.loader import get_grass
from cultivate.settings import MAP_WIDTH, MAP_HEIGHT, WIDTH, HEIGHT


class Map:
    def __init__(self):
        self.image = get_grass(MAP_WIDTH, MAP_HEIGHT)
        self.map_view_x = WIDTH
        self.map_view_y = HEIGHT
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.left = 0
        self.right = self.width - WIDTH
        self.up = 0
        self.down = self.height - HEIGHT
        self.move_amount = 50
        self.buildings = {"test building": TestBuilding(self.image)}

    def update_map_view(self, key_pressed):
        if key_pressed[pygame.K_DOWN]:
            if self.map_view_y <= self.down - self.move_amount:
                self.map_view_y += self.move_amount
        elif key_pressed[pygame.K_UP]:
            if self.map_view_y >= self.up + self.move_amount:
                self.map_view_y -= self.move_amount
        elif key_pressed[pygame.K_RIGHT]:
            if self.map_view_x <= self.right - self.move_amount:
                self.map_view_x += self.move_amount
        elif key_pressed[pygame.K_LEFT]:
            if self.map_view_x >= self.left + self.move_amount:
                self.map_view_x -= self.move_amount

    def draw(self, surface):
        surface.blit(self.image, (0, 0), area=(self.map_view_x, self.map_view_y,
                                               self.map_view_x+WIDTH, self.map_view_y+HEIGHT))
        for building in self.buildings.values():
            building.draw(surface)
