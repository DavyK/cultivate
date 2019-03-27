import pygame

from cultivate.loader import get_floor, get_roof_small, get_walls, get_lemon, get_vegetables, get_walls_edge


class TestBuilding:
    WALL_WIDTH = 12
    WALL_HEIGHT = 100
    BUILDING_X = 200
    BUILDING_Y = 200
    """Test building, please ignore."""
    def __init__(self, map_background: pygame.Surface):
        # WALL_WIDTH = 12
        # BUILDING_X = 160
        # BUILDING_Y = 160
        self.rect = pygame.Rect(800, 800, self.BUILDING_X, self.BUILDING_Y)
        self.floor = get_floor(self.rect.w, self.rect.h)
        self.walls = get_walls(self.BUILDING_X)
        self.sides = get_walls_edge(self.BUILDING_Y)
        map_background.blit(self.floor, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.walls, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.sides, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.sides, (self.rect.right - self.WALL_WIDTH, self.rect.y+self.WALL_HEIGHT))
        self.roof = get_roof_small()

        """Testing items & sprites, please ignore."""
        # self.lemon = get_lemon()
        # self.veggies = get_vegetables(200, 200)
        # map_background.blit(self.lemon, (self.rect.x, self.rect.y))
        # map_background.blit(self.veggies, (self.rect.x, self.rect.y))


    def draw(self, map_foreground: pygame.Surface, viewport: pygame.Rect):
        rect_near_player = pygame.Rect(viewport.centerx, viewport.centery, self.rect.x, self.rect.y-self.WALL_HEIGHT)
        # draw if the building is on screen but not near the player
        if viewport.colliderect(self.rect) and not self.rect.colliderect(rect_near_player):
            map_foreground.blit(
                self.roof,
                pygame.Rect(self.rect.x - viewport.x, self.rect.y - viewport.y,
                            self.rect.width, self.rect.height)
            )

