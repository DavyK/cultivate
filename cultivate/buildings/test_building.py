import pygame

from cultivate.loader import get_floor


class TestBuilding:
    """Test building, please ignore."""
    def __init__(self, game_map: pygame.Surface):
        self.floor = get_floor(200, 200)
        game_map.blit(self.floor, (500, 500))
        # todo: load roof
        # self.roof = get_small_roof()

    def draw(self, surface):
        # todo: draw roof unless player is close
        pass
