import pygame

from cultivate.loader import get_clothes_line
from cultivate.sprites import UpdatableSprite


class ClothesLine(UpdatableSprite):

    def __init__(self, map_x, map_y):
        self.image = get_clothes_line()
        rect = self.image.get_rect()
        rect.x = map_x
        rect.y = map_y
        super().__init__(rect)

    @property
    def help_text(self):
        return "dry laundry"

    @property
    def interaction_result(self):
        return self

    def draw(self, surface):
        surface.blit(self.image, self.rect)
