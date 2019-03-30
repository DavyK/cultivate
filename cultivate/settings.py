import os

import pygame

DEBUG = False

HEIGHT = 700
WIDTH = 1100
MAP_HEIGHT = MAP_WIDTH = 700 * 6


VIEW_PORT_SIZE = (WIDTH, HEIGHT)

TOTAL_MAP_SIZE = (MAP_HEIGHT, MAP_WIDTH)

pygame.font.init()

FONT = 'Consolas'
FONT_SIZE_XS = 14
XS_FONT = pygame.font.SysFont(FONT, FONT_SIZE_XS)
FONT_SIZE_SM = 16
SM_FONT = pygame.font.SysFont(FONT, FONT_SIZE_SM)
FONT_SIZE_MD = 24
MD_FONT = pygame.font.SysFont(FONT, FONT_SIZE_MD)
FONT_SIZE_LG = 32
LG_FONT = pygame.font.SysFont(FONT, FONT_SIZE_LG)
FONT_SIZE_XL = 40
XL_FONT = pygame.font.SysFont(FONT, FONT_SIZE_XL)
FONT_SIZE_TITLE = 72

LINE_SPACING = 15

FPS = 60

MAX_SIMULTANEOUS_SOUNDS = 6

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
