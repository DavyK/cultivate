import pygame

from cultivate.sprites import UpdatableSprite


class CandleMold(UpdatableSprite):

    color = (245, 245, 220)

    def __init__(self, map_x, map_y):
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        rect = self.image.get_rect()
        rect.x = map_x
        rect.y = map_y
        super().__init__(rect)

    @property
    def help_text(self):
        return "mold candles"

    @property
    def interaction_result(self):
        return self

    def draw(self, surface):
        surface.blit(self.image, self.rect)
