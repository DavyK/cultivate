import pygame

from cultivate.loader import get_desk
from cultivate.madlibs import Madlibs
from cultivate.sprites import UpdatableSprite


class Desk(UpdatableSprite):
    def __init__(self, map_x, map_y, surface: pygame.Surface, madlibs: Madlibs):
        self.madlibs = madlibs
        desk_image = get_desk()
        rect = desk_image.get_rect()
        rect.x = map_x
        rect.y = map_y
        surface.blit(desk_image, (map_x + 15, map_y))
        super().__init__(rect)

    @property
    def help_text(self):
        return "edit the scroll"

    @property
    def interaction_result(self):
        return self.madlibs
