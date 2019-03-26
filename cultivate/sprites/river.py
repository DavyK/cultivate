import typing

import pygame

from cultivate.sprites import UpdatableSprite
from cultivate.settings import MAP_HEIGHT, MAP_WIDTH
from cultivate.loader import get_bridge, get_river


class Bridge(UpdatableSprite):
    def __init__(self, map_x, map_y, surface: pygame.Surface):
        bridge_image = get_bridge()
        rect = bridge_image.get_rect()
        rect.x = map_x
        rect.y = map_y
        surface.blit(bridge_image, (map_x, map_y))
        super().__init__(rect)


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
        self.bridges = self.make_bridges(surface)

    @staticmethod
    def make_bridges(surface: pygame.Surface) -> typing.List[Bridge]:
        """Create bridge objects and blit them onto {surface}."""
        bridge_coords = [(((MAP_WIDTH / 2) - 2), (MAP_HEIGHT * 2 / 3)),
                         (((MAP_WIDTH / 2) - 2), (MAP_HEIGHT / 3))]
        bridges = []
        for coords in bridge_coords:
            bridges.append(Bridge(*coords, surface))
        return bridges
