import abc
import random
import typing

import pygame

from cultivate import settings
from cultivate.loader import (get_floor, get_roof_small, get_walls,
                              get_walls_edge)
from cultivate.sprites import UpdatableSprite


class Building(abc.ABC):
    def __init__(self, map_x, map_y, map_background: pygame.Surface):
        self.map_x = map_x
        self.map_y = map_y
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
        impassable_top_wall = UpdatableSprite(
            pygame.Rect(self.rect.x, self.rect.y,
                        self.top_wall.get_rect().w, self.top_wall.get_rect().h)
        )
        impassable_left_wall = UpdatableSprite(
            pygame.Rect(self.rect.x, self.rect.y,
                        self.side_wall.get_rect().w, self.side_wall.get_rect().h)
        )
        impassable_right_wall = UpdatableSprite(
            pygame.Rect(self.rect.right - self.side_wall.get_rect().w, self.rect.y,
                        self.side_wall.get_rect().w, self.side_wall.get_rect().h)
        )
        self.impassables = pygame.sprite.Group(impassable_top_wall, impassable_left_wall, impassable_right_wall)
        self.passables = pygame.sprite.Group()
        self.draw_items(map_background)

    def update(self, view_port: pygame.Rect):
        self.rect.x = self.map_x - view_port.x
        self.rect.y = self.map_y - view_port.y

    def draw(self, map_foreground: pygame.Surface) -> None:
        """Draw the roof if the player is not near the building."""
        rect_near_player = pygame.Rect(
            settings.WIDTH // 2 - 75, settings.HEIGHT // 2 - 75,
            150, 150
        )
        if not rect_near_player.colliderect(self.rect):
            map_foreground.blit(
                self.roof,
                pygame.Rect(self.rect.x, self.rect.y - self.roof_y_overlap,
                            self.rect.width, self.rect.height + self.roof_y_overlap)
            )
            map_foreground.blit(
                self.sign,
                pygame.Rect(self.rect.x + self.rect.w // 2 - self.sign.get_rect().w // 2,
                            self.rect.y + self.roof_y_overlap - self.sign.get_rect().h,
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


class DefaultBuilding(Building):
    """Default building without a sign or items."""

    @property
    def width(self) -> int:
        return 200

    @property
    def height(self) -> int:
        return 200

    def get_floor(self) -> pygame.Surface:
        return get_floor(self.rect.w, self.rect.h)

    def get_top_wall(self) -> pygame.Surface:
        return get_walls(self.rect.w)

    def get_side_wall(self) -> pygame.Surface:
        return get_walls_edge(self.rect.h)

    def get_roof(self) -> typing.Tuple[pygame.Surface, int]:
        return get_roof_small(), 100

    @abc.abstractmethod
    def get_sign(self) -> pygame.Surface:
        pass

    @abc.abstractmethod
    def draw_items(self, map_background: pygame.Surface):
        pass
