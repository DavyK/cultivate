import abc
import random
import typing

import pygame

from cultivate import settings


class Building(abc.ABC):
    def __init__(self, map_x, map_y, map_background: pygame.Surface):
        self.rect = pygame.Rect(map_x, map_y, self.width, self.height)
        self.floor = self.get_floor()
        self.top_wall = self.get_top_wall()
        self.side_wall = self.get_side_wall()
        self.roof, self.roof_y_overlap = self.get_roof()
        self.sign = self.get_sign()
        map_background.blit(self.floor, (self.rect.x, self.rect.y))
        if settings.DEBUG:
            random_color = pygame.Color(random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))
            pygame.draw.rect(map_background, random_color, self.rect)
        map_background.blit(self.top_wall, (self.rect.x, self.rect.y))
        map_background.blit(self.side_wall, (self.rect.x, self.rect.y))
        map_background.blit(self.side_wall, (self.rect.right - self.side_wall.get_rect().w, self.rect.y))
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
                self.sign, pygame.Rect(self.rect.x - viewport.x + self.rect.w // 2 - self.sign.get_rect().w // 2,
                                       self.rect.y - viewport.y + self.roof_y_overlap - self.sign.get_rect().h,
                                       self.rect.w, self.rect.h)
            )

    @property
    @abc.abstractmethod
    def width(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def height(self) -> int:
        pass

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
