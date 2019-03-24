import os
import random
import pygame
from functools import lru_cache
from cultivate import settings

@lru_cache(None)
def get_image(path):
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(canonicalized_path)
    return image
