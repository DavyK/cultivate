import os

import pygame

# I dislike that settings imports loader  - Ed
from cultivate.loader import get_font


DEBUG = False
FPS = 60

# dimensions
HEIGHT = 700
WIDTH = 1100
VIEW_PORT_SIZE = (WIDTH, HEIGHT)

MAP_HEIGHT = MAP_WIDTH = 700 * 6
TOTAL_MAP_SIZE = (MAP_HEIGHT, MAP_WIDTH)


# file paths
PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
RUN_DIR = os.path.join(PROJECT_DIR, 'cultivate')
ROOT_ASSETS_DIR = os.path.join(RUN_DIR, 'assets')
SPRITES_DIR = os.path.join(ROOT_ASSETS_DIR, 'sprites')
SOUNDS_DIR = os.path.join(ROOT_ASSETS_DIR, 'sounds')
MUSIC_DIR = os.path.join(ROOT_ASSETS_DIR, 'music')
DIALOGUE_DIR = os.path.join(ROOT_ASSETS_DIR, 'dialogue')
FONTS_DIR = os.path.join(ROOT_ASSETS_DIR, 'fonts')


# default fonts
pygame.font.init()

FONT = "NixieOne.ttf"
FONT_SIZE_XS = 12
XS_FONT = get_font(FONT, FONT_SIZE_XS)
FONT_SIZE_SM = 14
SM_FONT = get_font(FONT, FONT_SIZE_SM)
FONT_SIZE_MD = 18
MD_FONT = get_font(FONT, FONT_SIZE_MD)
FONT_SIZE_LG = 20
LG_FONT = get_font(FONT, FONT_SIZE_LG)
FONT_SIZE_XL = 24
XL_FONT = get_font(FONT, FONT_SIZE_XL)
MADLIBS_FONT = get_font("Cultivate-Regular.ttf", 32)
TITLE_FONT = get_font("Cultivate-Regular.ttf", 72)
