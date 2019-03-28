import pygame
from pygame.sprite import Sprite
from cultivate.sprites.river import River

from cultivate.sprites.fire import Fire
from cultivate.settings import WIDTH, HEIGHT
from cultivate import loader

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

    @property
    def help_text(self):
        return "pickup"

    def combine(self, item):
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
        return loader.get_lemon()

    def combine(self, item):
        if isinstance(item, WaterBucket):
            return LemonyWater(self.x, self.y)
        if isinstance(item, SugaryWater):
            return SugaryLemonWater(self.x, self.y)
        return None

class EmptyBucket(BasePickUp):
    name = 'bucket'

    def get_image(self):
        return loader.get_basin_empty()

    def combine(self, item):
        if isinstance(item, River):
            return WaterBucket(self.x, self.y)
        return None

class WaterBucket(BasePickUp):
    name = 'water bucket'

    def get_image(self):
        return loader.get_basin_water()

    def combine(self, item):
        if isinstance(item, Lemon):
            return LemonyWater(self.x, self.y)
        if isinstance(item, Sugar):
            return SugaryWater(self.x, self.y)
        if isinstance(item, Soap):
            return SoapyWater(self.x, self.y)
        return None

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
            return SugaryWater(self.x, self.y)


class LemonyWater(BasePickUp):
    name = 'lemon water'
    color = (250, 250, 210)
    size = (30, 30)

    def combine(self, item):
        if isinstance(item, Sugar):
            return SugaryLemonWater(self.x, self.y)
        return None

class SugaryWater(BasePickUp):
    name = 'sugary water'
    color = (50, 50, 100)
    size = (30, 30)

    def combine(self, item):
        if isinstance(item, Lemon):
            return SugaryLemonWater(self.x, self.y)
        return None

class SugaryLemonWater(BasePickUp):
    name = 'sugary lemon water'
    color = (123, 123, 105)
    size = (30, 30)

    def combine(self, item):
        if isinstance(item, Fire):
            return Lemonade(self.x, self.y)
        return None

class Lemonade(BasePickUp):
    name = 'lemonade'
    color = (50, 100, 100)
    size = (30, 30)

class Soap(BasePickUp):
    name = 'soap'
    color = (255, 255, 255)
    size = (25, 25)

    def get_image(self):
        return loader.get_soap()

    def combine(self, item):
        if isinstance(item, WaterBucket):
            return SoapyWater(self.x, self.y)
        return None


class RedSock(BasePickUp):
    name = 'red sock'
    color = (255, 60, 60)
    size = (25, 25)

    def combine(self, item):
        if isinstance(item, WhiteLaundry):
            return ColorRunLaundry(self.x, self.y)
        return None

class DirtyRobes(BasePickUp):
    name = 'dirty robes'
    color = (200, 200, 200)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_dirty()


    def combine(self, item):
        if isinstance(item, SoapyWater):
            return WhiteLaundry(self.x, self.y)
        return None

class SoapyWater(BasePickUp):
    name = 'soapy water'
    color = (136, 209, 243)
    size = (25, 25)

    def combine(self, item):
        if isinstance(item, DirtyRobes):
            return WhiteLaundry(self.x, self.y)
        return None

class WhiteLaundry(BasePickUp):
    name = 'whites laundry'
    color = (152, 183, 203)
    size = (25, 25)

    def combine(self, item):
        if isinstance(item, RedSock):
            return ColorRunLaundry(self.x, self.y)
        return None

class ColorRunLaundry(BasePickUp):
    name = 'color ruined laundry'
    color = (234, 164, 217)
    size = (25, 25)

class WhiteRobes(BasePickUp):
    name = 'white robes'
    color = (255, 255, 255)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_clean_white()

class PinkRobes(BasePickUp):
    name = 'pink robes'
    color = (255, 255, 255)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_clean_pink()
