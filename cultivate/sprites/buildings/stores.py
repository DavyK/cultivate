import typing

import pygame

from cultivate.loader import (get_boxes, get_cans,
                              get_carpet, get_floor, get_roof_small,
                              get_stores_sign, get_walls, get_walls_edge)
from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import Building


class Stores(Building):
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
        return get_stores_sign()

    def draw_items(self, map_background: pygame.Surface):
        boxes, boxes_x, boxes_y = get_boxes(), self.rect.x + 30, self.rect.y + 100
        cans, cans_x, cans_y = get_cans(), self.rect.x + 150, self.rect.y + 100

        map_background.blit(boxes, (boxes_x, boxes_y))
        map_background.blit(cans, (cans_x, cans_y))
        impassable_boxes = UpdatableSprite(
            pygame.Rect(boxes_x, boxes_y,
                        boxes.get_rect().w, boxes.get_rect().h)
        )
        self.impassables.add(impassable_boxes)
