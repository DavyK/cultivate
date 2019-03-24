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

def get_river(height):
    tiles = [
        (64, 48, 16, 16),  # left river
        (80, 48, 16, 16),  # middle river
        (112, 48, 16, 16)  # right river
    ]
    images = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'river1.png'),
        rects=tiles)
    river = pygame.Surface((48, height), pygame.SRCALPHA, 32)

    # make left column
    for i in range(0, height, 16):
        river.blit(images[0], (0, i))
        river.blit(images[1], (16, i))
        river.blit(images[2], (32, i))
    return river