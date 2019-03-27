import pygame

from cultivate.loader import get_fire, get_shovel, get_floor, get_roof_small, get_walls, get_lemon, get_vegetables, get_walls_edge, get_tool_sign

class ToolShed:
    WALL_WIDTH = 12
    WALL_HEIGHT = 100
    BUILDING_X = 200
    BUILDING_Y = 200
    """Test building, please ignore."""
    def __init__(self, map_background: pygame.Surface):
        self.rect = pygame.Rect(1300, 1000, self.BUILDING_X, self.BUILDING_Y*1.5)
        self.floor = get_floor(self.rect.w, self.rect.h)
        self.walls = get_walls(self.BUILDING_X)
        self.sides = get_walls_edge(self.BUILDING_Y)
        self.sign = get_tool_sign()
        map_background.blit(self.floor, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.walls, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.sides, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.sides, (self.rect.right - self.WALL_WIDTH, self.rect.y+self.WALL_HEIGHT))
        self.roof = get_roof_small()

        # items
        self.shovel = get_shovel()
        map_background.blit(self.shovel, (self.rect.x, self.rect.y))


    def draw(self, map_foreground: pygame.Surface, viewport: pygame.Rect):
        rect_near_player = pygame.Rect(viewport.centerx, viewport.centery, self.rect.x, self.rect.y-self.WALL_HEIGHT)
        # draw if the building is on screen but not near the player
        if viewport.colliderect(self.rect) and not self.rect.colliderect(rect_near_player):
            map_foreground.blit(
                self.roof,
                pygame.Rect(self.rect.x - viewport.x, self.rect.y - viewport.y,
                            self.rect.width, self.rect.height)
            )
            map_foreground.blit(
                self.sign, pygame.Rect(self.rect.x - viewport.x + (self.BUILDING_X - 48)/2, 
                            self.rect.y - viewport.y + (self.BUILDING_Y -34),
                            self.rect.width, self.rect.height)
            )

