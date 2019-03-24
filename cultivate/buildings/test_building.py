import pygame

from cultivate.loader import get_floor, get_roof_small


class TestBuilding:
    """Test building, please ignore."""
    def __init__(self, map_background: pygame.Surface):
        self.x = 700
        self.y = 700
        self.location = (self.x, self.y)
        self.floor = get_floor(200, 200)
        map_background.blit(self.floor, self.location)
        self.roof = get_roof_small()

    def draw(self, map_foreground: pygame.Surface):
        # todo: don't render roof if player is close
        map_foreground.blit(self.roof, self.location)
