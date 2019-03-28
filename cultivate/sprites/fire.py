
import pygame
from pygame.sprite import Sprite

from cultivate.loader import get_fire

class Fire(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = get_fire()
        self.rect = self.image.getCurrentFrame().get_rect()

    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y

    def draw(self, surface):
        surface.blit(self.image.getCurrentFrame(), self.rect)
