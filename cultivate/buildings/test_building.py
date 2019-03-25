import pygame

from cultivate.loader import get_floor, get_roof_small, get_walls, get_lemon, get_vegetables


class TestBuilding:
    """Test building, please ignore."""
    def __init__(self, map_background: pygame.Surface):
        self.rect = pygame.Rect(700, 700, 200, 200)
        self.floor = get_floor(self.rect.w, self.rect.h)
        self.walls = get_walls(200)
        self.lemon = get_lemon()
        self.veggies = get_vegetables(200, 200)
        map_background.blit(self.floor, (self.rect.x, self.rect.y))
        map_background.blit(self.walls, (self.rect.x, self.rect.y))
        map_background.blit(self.lemon, (self.rect.x, self.rect.y))
        map_background.blit(self.veggies, (self.rect.x, self.rect.y))
        self.roof = get_roof_small()

    def draw(self, map_foreground: pygame.Surface, viewport: pygame.Rect):
        rect_near_player = pygame.Rect(viewport.centerx, viewport.centery, 200, 200)
        # draw if the building is on screen but not near the player
        if viewport.colliderect(self.rect) and not self.rect.colliderect(rect_near_player):
            map_foreground.blit(
                self.roof,
                pygame.Rect(self.rect.x - viewport.x, self.rect.y - viewport.y,
                            self.rect.width, self.rect.height)
            )
