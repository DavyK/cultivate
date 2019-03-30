import typing

import pygame

from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import Building
from cultivate.loader import get_floor, get_library_sign, get_roof_small, get_walls, get_walls_edge, get_sideways_bed


class Dorm(Building):
    """ Dormitory"""

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
        bed_left = get_sideways_bed()
        bed_right = pygame.transform.flip(bed_left, True, False)
        map_background.blit(bed_left, (self.rect.x + 8, self.rect.y + 50))
        map_background.blit(bed_right, (self.rect.x + 130, self.rect.y + 50))

        map_background.blit(bed_left, (self.rect.x + 8, self.rect.y + 100))
        map_background.blit(bed_right, (self.rect.x + 130, self.rect.y + 100))

        map_background.blit(bed_left, (self.rect.x + 8, self.rect.y + 150))
        map_background.blit(bed_right, (self.rect.x + 130, self.rect.y + 150))
        impassable_bed = UpdatableSprite(
            pygame.Rect(self.rect.x + 8, self.rect.y + 50,
                        bed_left.get_rect().w, bed_right.get_rect().h)
        )

        self.impassables.add(impassable_bed)
