import os
from functools import lru_cache

import pygame
import pyganim
import random

from cultivate import settings

# todo: the spritesheets may be loaded from disk multiple tiles


@lru_cache(None)
def get_music(path: str) -> pygame.mixer.Sound:
    path = path.replace("/", os.sep).replace("\\", os.sep)
    path = os.path.join(settings.MUSIC_DIR, path)
    return pygame.mixer.Sound(path)


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

def get_bridge():
    tiles = [
        (416, 32, 44, 32)
    ]
    images = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage1.png'),
        rects=tiles)
    bridge = pygame.Surface((44, 32), pygame.SRCALPHA, 32)

    bridge.blit(images[0], (0, 0))
    return bridge

def get_dirt_path():
    tiles = [
        (130, 0, 28, 32)
    ]
    images = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage4.png'),
        rects=tiles)
    dirt_path = pygame.Surface((28, 32), pygame.SRCALPHA, 32)

    dirt_path.blit(images[0], (0, 0))
    return dirt_path

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

@lru_cache(None)
def get_forest(width, height):
    tiles = [
        (0, 220, 130, 130),
        (258, 290, 125, 220), # this is the annoyingly long one in case you were wondering
        (130, 95, 120, 126),
        (133, 226, 120, 126)
        ]
    forest_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage2.png'),
        rects=tiles)
    forest = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    # for top edge
    for i in range(0, width, 100):
        forest.blit(forest_tile[1], (i,-50))
        forest.blit(random.choice(forest_tile), (i+random.randint(-30,0),0+random.randint(-20,20)))
        forest.blit(random.choice(forest_tile), (i+random.randint(-30,0),150+random.randint(-20,20)))
        forest.blit(random.choice([forest_tile[0], forest_tile[2], forest_tile[3]]), (i+random.randint(-25,25),250+random.randint(-25,25)))
    # left edge
    for i in range(0, height, 100):
        forest.blit(forest_tile[1], (-50, i+random.randint(-30,0)))
        for i_x in range(50, 450, 90):
            forest.blit(random.choice(forest_tile), (i_x+random.randint(-30,30), i+random.randint(-30,0)))
    # right edge
    for i in range(0, height, 100):
        forest.blit(forest_tile[1], (width-100, i+random.randint(-30,0)))
        for i_x in range(50, 550, 90):
            forest.blit(random.choice(forest_tile), ((width - i_x)+random.randint(-30,30), i+random.randint(-30,0)))
    # bottom edge
    for i in range(0, width, 100):
        for i_y in range(50, 400, 90):
            forest.blit(random.choice(forest_tile), (i+random.randint(-30,0), (width - i_y)+random.randint(-30,30)))
        forest.blit(forest_tile[1], (i, height-100))
    return forest
