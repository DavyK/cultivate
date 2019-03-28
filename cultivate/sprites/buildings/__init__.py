import abc
import typing

import pygame


class Building(abc.ABC):
    def __init__(self, rect: pygame.Rect, map_background: pygame.Surface):
        self.rect = rect
        self.floor = self.get_floor()
        self.top_wall = self.get_top_wall()
        self.side_wall = self.get_side_wall()
        self.roof, self.roof_y_overlap = self.get_roof()
        self.sign = self.get_sign()
        map_background.blit(self.floor,     (self.rect.x, self.rect.y))
        map_background.blit(self.top_wall,  (self.rect.x, self.rect.y))
        map_background.blit(self.side_wall, (self.rect.x, self.rect.y))
        map_background.blit(self.side_wall, (self.rect.right, self.rect.y))
        self.draw_items(map_background)

    def draw(self, map_foreground: pygame.Surface, viewport: pygame.Rect) -> None:
        """Draw the roof and sign if the building is on screen but not near the player."""
        rect_near_player = pygame.Rect(viewport.centerx, viewport.centery, self.rect.w, self.rect.h)
        if viewport.colliderect(self.rect) and not self.rect.colliderect(rect_near_player):
            map_foreground.blit(
                self.roof,
                pygame.Rect(self.rect.x - viewport.x, self.rect.y - viewport.y - self.roof_y_overlap,
                            self.rect.width, self.rect.height + self.roof_y_overlap)
            )
            map_foreground.blit(
                self.sign, pygame.Rect(self.rect.x - viewport.x + self.rect.w // 2,
                                       self.rect.y - viewport.y + self.roof_y_overlap // 2,
                                       self.rect.w, self.rect.h)
            )

    @abc.abstractmethod
    def get_floor(self) -> pygame.Surface:
        pass

    @abc.abstractmethod
    def get_top_wall(self) -> pygame.Surface:
        pass

    @abc.abstractmethod
    def get_side_wall(self) -> pygame.Surface:
        pass

    @abc.abstractmethod
    def get_roof(self) -> typing.Tuple[pygame.Surface, int]:
        pass

    @abc.abstractmethod
    def get_sign(self) -> pygame.Surface:
        pass

    @abc.abstractmethod
    def draw_items(self, map_background: pygame.Surface):
        pass
