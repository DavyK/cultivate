import os
from functools import lru_cache

import pygame
import pyganim

from cultivate import settings


@lru_cache(None)
def get_image(path):
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(canonicalized_path)
    return image


@lru_cache(None)
def get_grass(width, height):
    tiles = [
        (269, 333, 16, 16),
    ]
    images = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage4.png'),
        rects=tiles)
    grass = pygame.Surface((width, height), pygame.SRCALPHA, 32)

    for i in range(0, height, 16):
        for j in range(0, width, 16):
            grass.blit(images[0], (j, i))
    return grass

@lru_cache(None)
def get_character():
  tiles = [
    (0, 0, 32, 32)
  ]
  images = pyganim.getImagesFromSpriteSheet(
    os.path.join(settings.SPRITES_DIR, 'chars2.png'),
    rects=tiles)
  character = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
  character.blit(images[0], 0,0)
  return character