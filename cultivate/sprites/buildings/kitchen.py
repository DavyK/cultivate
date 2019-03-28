import pygame

from cultivate.loader import get_floor, get_roof_small, get_walls, get_walls_edge, get_kitchen_sign
from cultivate.loader import get_lemon_basket, get_vegetables, get_herbs, get_cabinet

class Kitchen:
    WALL_WIDTH = 12
    WALL_HEIGHT = 100
    BUILDING_X = 200
    BUILDING_Y = 200
    def __init__(self, map_background: pygame.Surface):
        self.rect = pygame.Rect(800, 1200, self.BUILDING_X, self.BUILDING_Y*1.5)
        self.floor = get_floor(self.rect.w, self.rect.h)
        self.walls = get_walls(self.BUILDING_X)
        self.sides = get_walls_edge(self.BUILDING_Y)
        self.sign = get_kitchen_sign()
        map_background.blit(self.floor, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.walls, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.sides, (self.rect.x, self.rect.y+self.WALL_HEIGHT))
        map_background.blit(self.sides, (self.rect.right - self.WALL_WIDTH, self.rect.y+self.WALL_HEIGHT))
        self.roof = get_roof_small()

        # items
        self.veggies = get_vegetables(180, 200)
        self.lemon = get_lemon_basket()
        self.herbs = get_herbs()
        self.cheesecabinet = get_cabinet()
        map_background.blit(self.veggies, (self.rect.x +5, self.rect.y+100))
        map_background.blit(self.lemon, (self.rect.x +100, self.rect.y+170))
        map_background.blit(self.herbs, (self.rect.x+7, self.rect.y+105))
        map_background.blit(self.cheesecabinet, (self.rect.x+68, self.rect.y+105))
        map_background.blit(self.herbs, (self.rect.x+130, self.rect.y+105))


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

