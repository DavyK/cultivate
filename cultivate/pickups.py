import pygame
from pygame.sprite import Sprite
from cultivate.settings import WIDTH, HEIGHT
from cultivate.loader import get_lemon

class BasePickUp(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Call the parent class (Sprite) constructor
        super().__init__()

        # replace with an implementation on the child class that sets self image.
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y

    def get_help_text(self):
        return "Walk all over me"

    def __str__(self):
        return self.name


class Lemon(BasePickUp):
    name = 'lemon'
    color = (255, 244, 79)
    size = (50, 50)
