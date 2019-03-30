import pygame
from pygame.sprite import Sprite
from cultivate.loader import get_demon

class Demon(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.animation = get_demon()
        self.rect = self.image.get_rect()

    @property
    def image(self):
         return pygame.transform.scale(self.animation.getCurrentFrame(), (1000,1000))

    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    @property
    def help_text(self):
        return None

    @property
    def interaction_result(self):
        return None
