import random
import pygame
from flow import settings, colors, utils, mixins, difficulty
from flow.map import Map
from flow.signal import Signal


class Scene:
    font_color = colors.BLACK
    background_color = colors.BLACK
    fps = 60

    def __init__(self):
        pass

    def key_pressed(self, key):
        return False

    def mouse_pressed(self, pos):
        return False

    def draw(self, surface):
        pass

    def update(self):
        pass

    def is_finished(self):
        return False

    def finish(self):
        self.is_finished = True
