import pygame

from cultivate.sprites import UpdatableSprite
from cultivate.settings import MAP_HEIGHT, MAP_WIDTH
from cultivate.loader import get_bridge, get_dirt_path, get_river


class River(UpdatableSprite):
    def __init__(self, surface: pygame.Surface):
        x = MAP_WIDTH // 2
        y = 0

        water = get_river(MAP_HEIGHT)
        surface.blit(water, (x, y))
        rect = water.get_rect()
        rect.x = x
        rect.y = y

        super().__init__(rect)

        bridge = get_bridge()
        bridge_coords = [(((MAP_WIDTH / 2) + 2), (MAP_HEIGHT * 2 / 3)),
                         (((MAP_WIDTH / 2) + 2), (MAP_HEIGHT / 3))]
        for coords in bridge_coords:
            surface.blit(bridge, coords)

        dirt_path = get_dirt_path()
        dirt_path_coords = [(((MAP_WIDTH / 2) - 26), (MAP_HEIGHT * 2 / 3)),
                            (((MAP_WIDTH / 2) + 46), (MAP_HEIGHT * 2 / 3)),
                            (((MAP_WIDTH / 2) - 26), (MAP_HEIGHT / 3)),
                            (((MAP_WIDTH / 2) + 46), (MAP_HEIGHT / 3))
                            ]
        for coords in dirt_path_coords:
            surface.blit(dirt_path, coords)
