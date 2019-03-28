import pygame

from cultivate.loader import get_grave, get_dug_grave
from cultivate.sprites import UpdatableSprite


class Grave(UpdatableSprite):
    dug = False

    def __init__(self, map_x, map_y):
        self.grave_image = get_grave()
        rect = self.grave_image.get_rect()
        rect.x = map_x
        rect.y = map_y
        super().__init__(rect)

    @property
    def help_text(self):
        return "dig with shovel"

    @property
    def interaction_result(self):
        if not self.dug:
            self.dug = True
            self.grave_image = get_dug_grave()
        return None

    def draw(self, surface):
        surface.blit(self.grave_image, self.rect)
