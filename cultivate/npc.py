from itertools import cycle

import pygame

from cultivate.loader import get_character


class Npc:
    def __init__(self, points, speed=3):
        self.points = points
        self.path = cycle(points[1:]+points[0:1])
        self.rect = pygame.Rect(self.points[0][0], self.points[0][1], 10, 20)
        self.next_pos = next(self.path)
        self.image = get_character()
        self.speed = speed
        self.paused = False

    def draw(self, surface, viewport):
        if viewport.colliderect(self.rect):
            surface.blit(self.image.getCurrentFrame(), (self.rect.x-viewport.x,
                                      self.rect.y-viewport.y))

            rect_near_player = pygame.Rect(viewport.centerx - 100, viewport.centery - 100, 200, 200)

            self.paused = self.rect.colliderect(rect_near_player)

    def update(self):
        if self.paused:
            return

        if self.next_pos[0] > self.rect.x + self.speed:
            self.rect.x += self.speed
        elif self.next_pos[0] < self.rect.x - self.speed:
            self.rect.x -= self.speed
        elif self.next_pos[1] < self.rect.y - self.speed:
            self.rect.y -= self.speed
        elif self.next_pos[1] > self.rect.y + self.speed:
            self.rect.y += self.speed
        else:
            self.rect.x = self.next_pos[0]
            self.rect.y = self.next_pos[1]
            self.next_pos = next(self.path)
