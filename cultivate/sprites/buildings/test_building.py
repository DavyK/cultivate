import typing

import pygame

from cultivate.sprites.buildings import Building
from cultivate.loader import get_floor, get_library_sign, get_roof_small, get_walls, get_walls_edge, get_shelf_l, get_shelf_m, get_painting


class TestBuilding(Building):
    """Test building, please ignore."""

    @property
    def width(self) -> int:
        return 200

    @property
    def height(self) -> int:
        return 200

    def get_floor(self) -> pygame.Surface:
        return get_floor(self.rect.w, self.rect.h)

    def get_top_wall(self) -> pygame.Surface:
        return get_walls(self.rect.w)

    def get_side_wall(self) -> pygame.Surface:
        return get_walls_edge(self.rect.h)

    def get_roof(self) -> typing.Tuple[pygame.Surface, int]:
        return get_roof_small(), 100

    def get_sign(self) -> pygame.Surface:
        return get_library_sign()

    def draw_items(self, map_background: pygame.Surface):
        # items
        shelfL = get_shelf_l()
        shelfM = get_shelf_m()
        painting = get_painting()
        map_background.blit(painting, (self.rect.x + 70, self.rect.y + 5))
        map_background.blit(shelfL, (self.rect.x + 60, self.rect.y + 30))
        map_background.blit(shelfM, (self.rect.x + 120, self.rect.y + 80))
