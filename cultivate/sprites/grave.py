import pygame

from cultivate.loader import get_grave, get_dug_grave, get_planted_grave
from cultivate.sprites import UpdatableSprite


class Grave(UpdatableSprite):
    dug = False
    planted = False

    def __init__(self, map_x, map_y, rotation=0):
        self.rotation = rotation
        self.grave_image = pygame.transform.rotate(get_grave(), rotation)
        rect = self.grave_image.get_rect()
        rect.x = map_x
        rect.y = map_y
        super().__init__(rect)

    @property
    def help_text(self):
        if not self.dug:
            return "dig with shovel"
        elif not self.planted:
            return "plant the flower"

    def dig(self):
        if not self.dug:
            self.dug = True
            self.grave_image = pygame.transform.rotate(get_dug_grave(), self.rotation)
        return

    def plant(self):
        if not self.planted:
            self.planted = True
            self.grave_image = pygame.transform.rotate(get_planted_grave(), self.rotation)
        return


    @property
    def interaction_result(self):
        return self

    def draw(self, surface):
        surface.blit(self.grave_image, self.rect)
