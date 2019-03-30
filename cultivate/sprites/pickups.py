import random
import pygame
from pygame.sprite import Sprite
from cultivate.sprites.river import River

from cultivate.sprites.fire import Fire
from cultivate.sprites.clothes_line import ClothesLine
from cultivate import loader

class BasePickUp(Sprite):
    scale = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = self.get_image()

        if self.scale:
            self.image = pygame.transform.scale(self.image, self.size)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = 'pickup'

    def get_image(self):
        image = pygame.Surface(self.size)
        image.fill(self.color)
        return image

    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y

    @property
    def help_text(self):
        msg = f'{self.action}'
        if self.name:
            msg += f' the {self.name}'
        return msg

    def combine(self, item):
        return None, None

    def can_combine(self, item):
        new_item, reusable = self.combine(item)
        return new_item is not None

    def __str__(self):
        return self.name

    def interact(self, key):
        return

    @property
    def interaction_result(self):
        return self


class Lemon(BasePickUp):
    name = 'lemon basket'

    def get_image(self):
        return loader.get_lemon_basket()

    def combine(self, item):
        if isinstance(item, WaterBucket):
            return LemonyWater(self.x, self.y), None
        if isinstance(item, SugaryWater):
            return SugaryLemonWater(self.x, self.y), None
        return None, None

class EmptyBucket(BasePickUp):
    name = 'bucket'

    def get_image(self):
        return loader.get_basin_empty()

    def combine(self, item):
        if isinstance(item, River):
            return WaterBucket(self.x, self.y), None
        if isinstance(item, MeltedBlackWax):
            return BlackCandles(self.x, self.y), None
        if isinstance(item, ScentedMeltedBlackWax):
            return ScentedBlackCandles(self.x, self.y), None
        return None, None

class WaterBucket(BasePickUp):
    name = 'water bucket'

    def get_image(self):
        return loader.get_basin_water()

    def combine(self, item):
        if isinstance(item, River):
            return EmptyBucket(self.x, self.y), None
        if isinstance(item, Lemon):
            return LemonyWater(self.x, self.y), None
        if isinstance(item, Sugar):
            return SugaryWater(self.x, self.y), None
        if isinstance(item, Soap):
            return SoapyWater(self.x, self.y), None
        if isinstance(item, DirtyRobes):
            return RobesInWater(self.x, self.y), None
        return None, None

class Sugar(BasePickUp):
    name = 'sugar'
    color = (10, 10, 10)
    size = (30, 30)

    def get_image(self):
        return loader.get_empty_bottle()

    def combine(self, item):
        if isinstance(item, WaterBucket):
            return SugaryWater(self.x, self.y), None
        return None, None


class LemonyWater(BasePickUp):
    name = 'lemon water'
    color = (250, 250, 210)
    size = (30, 30)

    def get_image(self):
        return loader.get_lemonade_pitcher()

    def combine(self, item):
        if isinstance(item, Sugar):
            return SugaryLemonWater(self.x, self.y), None
        return None, None

class SugaryWater(BasePickUp):
    name = 'sugary water'
    color = (50, 50, 100)
    size = (30, 30)

    def get_image(self):
        return loader.get_lemonade_pitcher()

    def combine(self, item):
        if isinstance(item, Lemon):
            return SugaryLemonWater(self.x, self.y), None
        return None, None

class SugaryLemonWater(BasePickUp):
    name = 'sugary lemon water'
    color = (123, 123, 105)
    size = (30, 30)

    def get_image(self):
        return loader.get_lemonade_pitcher()

    def combine(self, item):
        if isinstance(item, Fire):
            return Lemonade(self.x, self.y), EmptyBucket(self.x, self.y)
        return None, None

class Lemonade(BasePickUp):
    name = 'lemonade'
    color = (50, 100, 100)
    size = (30, 30)

    def get_image(self):
        return loader.get_lemonade_pitcher()

class RatPoison(BasePickUp):
    name = 'rat poison'
    color = (0,0,0)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_rat_poison()

    def combine(self, item):
        if isinstance(item, River):
            return EmptyBottle(self.x, self.y), None
        return None, None

class EmptyBottle(BasePickUp):
    name = 'empty bottle'
    color = (100, 100, 200)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_empty_bottle()


class Soap(BasePickUp):
    name = 'soap'
    color = (255, 255, 255)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_soap()

    def combine(self, item):
        if isinstance(item, WaterBucket):
            return SoapyWater(self.x, self.y), None
        if isinstance(item, RobesInWater):
            return WhiteLaundry(self.x, self.y), None
        if isinstance(item, RobesAndSockInWater):
            return ColorRunLaundry(self.x, self.y), None
        return None, None


class RedSock(BasePickUp):
    name = 'red sock'
    color = (255, 60, 60)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_sock()

    def combine(self, item):
        if isinstance(item, WhiteLaundry):
            return ColorRunLaundry(self.x, self.y), None
        if isinstance(item, RobesInWater):
            return RobesAndSockInWater(self.x, self.y), None
        return None, None

class DirtyRobes(BasePickUp):
    name = 'dirty robes'
    color = (200, 200, 200)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_dirty()

    def combine(self, item):
        if isinstance(item, SoapyWater):
            return WhiteLaundry(self.x, self.y), None
        if isinstance(item, WaterBucket):
            return RobesInWater(self.x, self.y), None
        return None, None

class SoapyWater(BasePickUp):
    name = 'soapy water'
    color = (136, 209, 243)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_basin()

    def combine(self, item):
        if isinstance(item, DirtyRobes):
            return WhiteLaundry(self.x, self.y), None
        return None, None

class RobesInWater(BasePickUp):
    name = 'robes in water'
    color = (200, 200, 200)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_basin()

    def combine(self, item):
        if isinstance(item, Soap):
            return WhiteLaundry(self.x, self.y), None
        if isinstance(item, RedSock):
            return RobesAndSockInWater(self.x, self.y), None
        return None, None

class RobesAndSockInWater(BasePickUp):
    name = 'robes and red sock in water'
    color = (200, 40, 200)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_basin()

    def combine(self, item):
        if isinstance(item, Soap):
            return ColorRunLaundry(self.x, self.y), None
        return None, None
class WhiteLaundry(BasePickUp):
    name = 'whites laundry'
    color = (152, 183, 203)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_basin()

    def combine(self, item):
        if isinstance(item, RedSock):
            return ColorRunLaundry(self.x, self.y), None
        elif isinstance(item, ClothesLine):
            return WhiteRobes(self.x, self.y), EmptyBucket(self.x, self.y)
        return None, None

class ColorRunLaundry(BasePickUp):
    name = 'color ruined laundry'
    color = (234, 164, 217)
    size = (25, 25)

    def get_image(self):
        return loader.get_laundry_basin()

    def combine(self, item):
        if isinstance(item, ClothesLine):
            return PinkRobes(self.x, self.y), EmptyBucket(self.x, self.y)
        return None, None

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

class BeesWax(BasePickUp):
    name = 'bees wax'
    color = (217, 239, 30)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_empty_bottle()

    def combine(self, item):
        if isinstance(item, Fire):
            return MeltedWax(self.x, self.y), None
        return None, None

class MeltedWax(BasePickUp):
    name = 'melted wax'
    color = (217, 239, 30)
    size = (25, 25)

    def get_image(self):
        return loader.get_melted_wax()

    def combine(self, item):
        if isinstance(item, BlackDye):
            return MeltedBlackWax(self.x, self.y), None
        if isinstance(item, EssenceOfCinnamon):
            return ScentedMeltedWax(self.x, self.y), None
        return None, None

class MeltedBlackWax(BasePickUp):
    name = 'melted black wax'
    color = (217, 239, 30)
    size = (25, 25)

    def get_image(self):
        return loader.get_melted_wax()

    def combine(self, item):
        if isinstance(item, EssenceOfCinnamon):
            return ScentedMeltedBlackWax(self.x, self.y), None
        if isinstance(item, EmptyBucket):
            return BlackCandles(self.x, self.y), EmptyBucket(self.x, self.y)
        return None, None


class BlackDye(BasePickUp):
    name = 'black dye'
    color = (0,0,0)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_brown_jar()

    def combine(self, item):
        if isinstance(item, MeltedWax):
            return MeltedBlackWax(self.x, self.y), None
        if isinstance(item, ScentedMeltedWax):
            return ScentedMeltedBlackWax(self.x, self.y), None
        return None, None

class EssenceOfCinnamon(BasePickUp):
    name = 'essence of cinnamon'
    color = (122, 71, 47)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_pestle_and_mortar()

    def combine(self, item):
        if isinstance(item, MeltedWax):
            return ScentedMeltedWax(self.x, self.y), None
        if isinstance(item, MeltedBlackWax):
            return ScentedMeltedBlackWax(self.x, self.y), None
        return None, None

class ScentedMeltedWax(BasePickUp):
    name = 'scented melted wax'
    color = (217, 239, 30)
    size = (25, 25)

    def get_image(self):
        return loader.get_melted_wax()

    def combine(self, item):
        if isinstance(item, BlackDye):
            return ScentedMeltedBlackWax(self.x, self.y), None
        return None, None

class ScentedMeltedBlackWax(BasePickUp):
    name = 'scented melted black wax'
    color = (217, 239, 30)
    size = (25, 25)

    def get_image(self):
        return loader.get_melted_wax()

    def combine(self, item):
        if isinstance(item, EmptyBucket):
            return ScentedBlackCandles(self.x, self.y), EmptyBucket(self.x, self.y)
        return None, None

class BlackCandles(BasePickUp):
    name = 'black candle'
    color = (20, 20, 20)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_candles_black()

class ScentedBlackCandles(BasePickUp):
    name = 'scented black candle'
    color = (0, 0 ,0)
    size = (25, 25)
    scale = True

    def get_image(self):
        return loader.get_candles_black()

class Shovel(BasePickUp):
    name = "shovel"
    size = (13, 40)
    scale = True

    def get_image(self):
        return loader.get_shovel()

class Flower(BasePickUp):
    name = "flower"

    def get_image(self):
        flowers = [
            loader.get_plant1,
            loader.get_plant2,
            loader.get_plant3,
            loader.get_plant4,
            loader.get_plant5,
            loader.get_plant6,
            loader.get_plant7,
        ]
        return random.choice(flowers)()

