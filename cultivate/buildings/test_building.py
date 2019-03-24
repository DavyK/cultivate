import pygame

from cultivate.loader import get_floor, get_roof_small


class TestBuilding:
    """Test building, please ignore."""
    def __init__(self, map_background: pygame.Surface):
        self.rect = pygame.Rect(700, 700, 200, 200)
        self.floor = get_floor(self.rect.w, self.rect.h)
        map_background.blit(self.floor, (self.rect.x, self.rect.y))
        self.roof = get_roof_small()

    def draw(self, map_foreground: pygame.Surface, viewport: pygame.Rect):
        # todo: don't render roof if player is close
        if viewport.colliderect(self.rect):
            map_foreground.blit(
                self.roof,
                pygame.Rect(self.rect.x - viewport.x, self.rect.y - viewport.y,
                            self.rect.width, self.rect.height)
            )
