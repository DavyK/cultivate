import pygame

from cultivate.loader import (get_library_sign, get_painting, get_shelf_l,
                              get_shelf_m)
from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import DefaultBuilding


class Library(DefaultBuilding):
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
        impassable_shelfL = UpdatableSprite(
            pygame.Rect(self.rect.x + 60, self.rect.y + 30,
                        shelfL.get_rect().w, shelfL.get_rect().h)
        )
        impassable_shelfM = UpdatableSprite(
            pygame.Rect(self.rect.x + 120, self.rect.y + 80,
                        shelfM.get_rect().w, shelfM.get_rect().h)
        )
        self.impassables.add(impassable_shelfL, impassable_shelfM)
