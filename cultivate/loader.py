import os
from functools import lru_cache

import pygame
import pyganim

from cultivate import settings

# todo: the spritesheets may be loaded from disk multiple tiles


@lru_cache(None)
def get_image(path: str) -> pygame.Surface:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(canonicalized_path)
    return image


@lru_cache(None)
def get_grass(width: int, height: int) -> pygame.Surface:
    # load the grass tile from the sprite sheet
    grass_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage4.png'),
        rects=[(269, 333, 16, 16)])[0]

    # create a blank surface to paint with grass
    grass = pygame.Surface((width, height), pygame.SRCALPHA, 32)

    # paint grass tiles onto surface
    for i in range(0, height, 16):
        for j in range(0, width, 16):
            grass.blit(grass_tile, (i, j))
    return grass


@lru_cache(None)
def get_floor(width: int, height: int) -> pygame.Surface:
    # load the floor tile from the sprite sheet
    floor_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'floors1.png'),
        rects=[(0, 0, 16, 16)])[0]

    # create a blank surface to tile
    floor = pygame.Surface((width, height), pygame.SRCALPHA, 32)

    # tile the floor
    for i in range(0, height, 16):
        for j in range(0, width, 16):
            floor.blit(floor_tile, (i, j))
    return floor


@lru_cache(None)
def get_roof_small() -> pygame.Surface:
    return get_image(os.path.join(settings.SPRITES_DIR, "roof.png"))


@lru_cache(None)
def get_character():
    # load the character tile from the sprite sheet
    character_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'chars2.png'),
        rects=[(0, 0, 32, 32)])[0]

    # create surface and add tile to it
    character = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
    character.blit(character_tile, (0, 0))
    return character


@lru_cache(None)
def get_weed():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "foliage2.png"),
        rects=[(131, 453, 58, 58)])[0]

@lru_cache(None)
def get_walls(width):
    wall_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'walls2.png'),
        rects=[(65, 0, 62, 62)])[0]
    wall = pygame.Surface((width,62), pygame.SRCALPHA, 32)
    for i in range(0, width, 62):
        wall.blit(wall_tile, (i,0))
    return wall

