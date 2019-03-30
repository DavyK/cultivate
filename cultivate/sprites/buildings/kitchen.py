import pygame

from cultivate.loader import (get_cabinet, get_herbs, get_kitchen_sign,
                              get_lemon_basket, get_vegetables)
from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import DefaultBuilding


class Kitchen(DefaultBuilding):
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
