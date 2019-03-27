import pygame
from pygame.sprite import Sprite
from cultivate.settings import WIDTH, HEIGHT
from cultivate.loader import get_lemon, get_laundry_basin_empty

class BasePickUp(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = self.get_image()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_image(self):
        image = pygame.Surface(self.size)
        image.fill(self.color)
        return image

    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y

    def get_help_text(self):
        return "pickup"

    def can_combine(self, item):
        return False

    def __str__(self):
        return self.name

    def interact(self, key):
        return

    @property
    def interaction_result(self):
        return self

class Lemon(BasePickUp):
    name = 'lemon'

    def get_image(self):
        return get_lemon()

    def can_combine(self, item):
        if isinstance(item, WaterBucket):
            return True
        return False

    def combine(self, item):
        if isinstance(item, WaterBucket):
            return LemonyWater(self.x, self.y)

class WaterBucket(BasePickUp):
    name = 'bucket'
    color = (0, 0, 150)
    size = (50, 50)

    def get_image(self):
        return get_laundry_basin_empty()

    def can_combine(self, item):
        if isinstance(item, Lemon):
            return True
        return False

    def combine(self, item):
        if isinstance(item, Lemon):
            print("lemony water")
            return LemonyWater(self.x, self.y)


class LemonyWater(BasePickUp):
    name = 'lemon_water'
    color = (0, 100, 150)
    size = (50, 50)
