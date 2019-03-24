import os
from cultivate import settings
import pygame
import pyganim


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
