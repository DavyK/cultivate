import random

import pygame

from cultivate.buildings.test_building import TestBuilding
from cultivate.loader import get_grass, get_dirt_path
from cultivate.loader import get_grass, get_weed
from cultivate.settings import MAP_WIDTH, MAP_HEIGHT, WIDTH, HEIGHT
from cultivate.loader import get_river
from cultivate.loader import get_bridge


class Map:
    def __init__(self):
        self.compose_image()
        self.map_view_x = WIDTH
        self.map_view_y = HEIGHT
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.left = 0
        self.right = self.width - WIDTH
        self.up = 0
        self.down = self.height - HEIGHT
        self.move_amount = 50
        self.generate_random_weeds()
        self.buildings = {"test building": TestBuilding(self.image)}


    def compose_image(self):
        self.image = get_grass(MAP_WIDTH, MAP_HEIGHT)
        river = get_river(MAP_HEIGHT)
        self.image.blit(river, ((MAP_WIDTH / 2), 0))
        bridge = get_bridge()
        bridge_coords = [(((MAP_WIDTH / 2) + 2), (MAP_HEIGHT * 2 / 3)), (((MAP_WIDTH / 2) + 2), (MAP_HEIGHT / 3))]
        for coords in bridge_coords:
            self.image.blit(bridge, coords)
        dirt_path = get_dirt_path()
        dirt_path_coords = [(((MAP_WIDTH / 2) - 26), (MAP_HEIGHT * 2 / 3)),
                            (((MAP_WIDTH / 2) + 46), (MAP_HEIGHT * 2 / 3)),
                            (((MAP_WIDTH / 2) - 26), (MAP_HEIGHT / 3)),
                            (((MAP_WIDTH / 2) + 46), (MAP_HEIGHT / 3))
                            ]
        for coords in dirt_path_coords:
            self.image.blit(dirt_path, coords)
        return self.image

    def generate_random_weeds(self, count=100):
        weed = get_weed()
        locations = [(random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT)) for _ in range(count)]
        for x, y in locations:
            self.image.blit(weed, (x, y))

    def update_map_view(self, key_pressed):
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            if self.map_view_y <= self.down - self.move_amount:
                self.map_view_y += self.move_amount
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            if self.map_view_y >= self.up + self.move_amount:
                self.map_view_y -= self.move_amount
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            if self.map_view_x <= self.right - self.move_amount:
                self.map_view_x += self.move_amount
        elif key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            if self.map_view_x >= self.left + self.move_amount:
                self.map_view_x -= self.move_amount

    def get_viewport(self):
        return pygame.Rect(self.map_view_x, self.map_view_y,
                           WIDTH, HEIGHT)

    def draw(self, surface):
        surface.blit(self.image, (0, 0), area=(self.map_view_x, self.map_view_y,
                                               self.map_view_x+WIDTH, self.map_view_y+HEIGHT))
        for building in self.buildings.values():
            building.draw(surface, self.get_viewport())

