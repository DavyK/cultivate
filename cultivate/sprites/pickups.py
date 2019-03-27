import pygame
from pygame.sprite import Sprite
from cultivate.settings import WIDTH, HEIGHT
from cultivate.loader import get_lemon, get_basin_empty

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

    def get_image(self):
        return get_basin_empty()

    def can_combine(self, item):
        if isinstance(item, Lemon):
            return True
        if isinstance(item, Sugar):
            return True
        return False

    def combine(self, item):
        if isinstance(item, Lemon):
            print("lemony water")
            return LemonyWater(self.x, self.y)
        if isinstance(item, Sugar):
            print("sugary water")
            return SugaryWater(self.x, self.y)


class Sugar(BasePickUp):
    name = 'sugar'
    color = (10, 10, 10)
    size = (30, 30)

    def can_combine(self, item):
        if isinstance(item, WaterBucket):
            return True
        return False

    def combine(self, item):
        if isinstance(item, WaterBucket):
            print("sugary water")
            return SugaryWater(self.x, self.y)


class LemonyWater(BasePickUp):
    name = 'lemon_water'
    color = (250, 250, 210)
    size = (30, 30)

    def can_combine(self, item):
        if isinstance(item, Sugar):
            return True
        return False

    def combine(self, item):
        if isinstance(item, Sugar):
            print("sugary lemon water")
            return SugaryLemonWater(self.x, self.y)


class SugaryWater(BasePickUp):
    name = 'sugary water'
    color = (50, 50, 100)
    size = (30, 30)

    def can_combine(self, item):
        if isinstance(item, Lemon):
            return True
        return False

    def combine(self, item):
        if isinstance(item, Lemon):
            print("sugary lemony water")
            return SugaryLemonyWater(self.x, self.y)


class SugaryLemonWater(BasePickUp):
    name = 'sugary_lemon_water'
    color = (123, 123, 105)
    size = (30, 30)


class Lemonade(BasePickUp):
    name = 'lemonade'
    color = (50, 100, 100)
    size = (30, 30)
