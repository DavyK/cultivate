import typing

import pygame

from cultivate.loader import (get_cabinet, get_floor, get_herbs,
                              get_kitchen_sign, get_lemon_basket,
                              get_roof_small, get_vegetables, get_walls,
                              get_walls_edge)
from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import Building


class Kitchen(Building):
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
        return get_kitchen_sign()

    def draw_items(self, map_background: pygame.Surface):
        veggies = get_vegetables(180, 200)
        lemon = get_lemon_basket()
        herbs = get_herbs()
        cheesecabinet = get_cabinet()
        map_background.blit(veggies, (self.rect.x +5, self.rect.y))
        map_background.blit(lemon, (self.rect.x + 100, self.rect.y + 70))
        map_background.blit(herbs, (self.rect.x + 7, self.rect.y + 5))
        map_background.blit(cheesecabinet, (self.rect.x + 68, self.rect.y + 5))
        map_background.blit(herbs, (self.rect.x + 130, self.rect.y + 5))
        impassable_cheesecabinate = UpdatableSprite(
            pygame.Rect(self.rect.x + 68, self.rect.y + 5,
                        cheesecabinet.get_rect().w, cheesecabinet.get_rect().h)
        )
        self.impassables.add(impassable_cheesecabinate)
