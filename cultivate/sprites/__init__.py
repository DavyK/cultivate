import random

import pygame

from cultivate import settings


class UpdatableSprite(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        super().__init__()

        if settings.DEBUG:
            self.image = pygame.Surface(self.rect.size)
            random_color = pygame.Color(random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))
            self.image.fill(random_color)

    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y

    @property
    def help_text(self):
        return None

    @property
    def interaction_result(self):
        return None
