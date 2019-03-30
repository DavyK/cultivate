import pygame
from cultivate.loader import get_stone_cross_floor, get_stone_cross_wall, get_altar, get_pews, get_church_roof
from cultivate import settings


class Church:
    def __init__(self, map_background: pygame.Surface):
        self.rect = pygame.Rect(3000, 1500, 288, 544)
        self.floor = get_stone_cross_floor(self.rect.w, self.rect.h)
        self.walls = get_stone_cross_wall(288, 544)
        self.pews = get_pews()
        self.altar = get_altar()
        map_background.blit(self.floor, (self.rect.x, self.rect.y))
        map_background.blit(self.walls, (self.rect.x, self.rect.y))
        pew_coords = [(self.rect.x + 112, self.rect.y + (int((544 - 32) * 7 / 16) + 48)),
                      (self.rect.x + 112, self.rect.y + (int((544 - 32) * 7 / 16) + 96)),
                      (self.rect.x + 112, self.rect.y + (int((544 - 32) * 7 / 16) + 144)),
                      (self.rect.x + 112, self.rect.y + (int((544 - 32) * 7 / 16) + 182))]
        for coord in pew_coords:
            map_background.blit(self.pews, coord)
        map_background.blit(self.altar, ((self.rect.x + 128), (self.rect.y + (int((544 - 32) * 7 / 16) - 64))))
        self.roof = get_church_roof()


    def update(self, view_port: pygame.Rect):
        self.rect.x = 3000 - view_port.x
        self.rect.y = 1500 - view_port.y

    def draw(self, map_foreground: pygame.Surface) -> None:
        """Draw the roof if the player is not near the building."""
        rect_near_player = pygame.Rect(
            settings.WIDTH // 2 - 75, settings.HEIGHT // 2 - 75,
            150, 150
        )
        if not rect_near_player.colliderect(self.rect):
            map_foreground.blit(
                self.roof,
                pygame.Rect(self.rect.x + 1, self.rect.y - 84,
                            self.rect.width, self.rect.height + 100)
            )

