import typing
import pygame

from cultivate.sprites import UpdatableSprite
from cultivate.settings import MAP_HEIGHT, MAP_WIDTH
from cultivate.loader import get_bed


class Bed(UpdatableSprite):
    def __init__(self, map_x, map_y, surface: pygame.Surface):
        bed_image = get_bed()
        rect = bed_image.get_rect()
        rect.x = map_x
        rect.y = map_y
        surface.blit(bed_image, (map_x, map_y))
        super().__init__(rect)

    @property
    def help_text(self):
        return "go to sleep"

    @property
    def interaction_result(self):
        return self
