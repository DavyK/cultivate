from itertools import cycle

import pygame

from cultivate.loader import get_npc
from cultivate.settings import WIDTH, HEIGHT

class Npc(pygame.sprite.Sprite):
    def __init__(self, points, speed=3):
        super().__init__()

        self.points = points
        self.path = cycle(points)
        self.x, self.y = next(self.path)
        self.next_x, self.next_y = next(self.path)

        self.image = get_npc().getCurrentFrame()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = speed
        self.paused = False

    def update(self, viewport):
        rect_near_player = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 200)
        direction = None
        if not self.rect.colliderect(rect_near_player):
            if self.next_x > self.x + self.speed:
                direction = 'right'
                self.x += self.speed
            elif self.next_x < self.x - self.speed:
                direction = 'left'
                self.x -= self.speed
            elif self.next_y < self.y - self.speed:
                direction = 'backward'
                self.y -= self.speed
            elif self.next_y > self.y + self.speed:
                direction = 'forward'
                self.y += self.speed
            else:
                self.x = self.next_x
                self.y = self.next_y
                self.next_x, self.next_y = next(self.path)
        self.image = get_npc(direction).getCurrentFrame()
        self.rect.x = self.x - viewport.x
        self.rect.y = self.y - viewport.y
    
    def get_help_text(self):
        return "Press X to talk"
