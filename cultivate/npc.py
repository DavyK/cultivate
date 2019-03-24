import pygame

from itertools import cycle


class Npc:
    def __init__(self, points, speed=5):
        self.points = points
        print(points[1:]+points[0:1])
        self.path = cycle(points[1:]+points[0:1])
        self.pos = self.points[0]
        self.next_pos = next(self.path)
        self.speed = speed

    def draw(self, surface, view_port):
        if view_port.colliderect(pygame.Rect(self.pos[0], self.pos[1], 10, 20)):
            pygame.draw.rect(surface, pygame.Color(255, 0, 0),
                             pygame.Rect(self.pos[0]-view_port.x,self.pos[1]-view_port.y, 10, 20))
            # surface.blit(self.image, (view_port.x-self.pos[0],
            #                           view_port.y-self.pos[1]))

    def update(self):
        if self.next_pos[0] > self.pos[0]:
            self.pos = (self.pos[0] + self.speed, self.pos[1])
        elif self.next_pos[0] < self.pos[0]:
            self.pos = (self.pos[0] - self.speed, self.pos[1])
        elif self.next_pos[1] < self.pos[1]:
            self.pos = (self.pos[0], self.pos[1] - self.speed)
        elif self.next_pos[1] > self.pos[1]:
            self.pos = (self.pos[0], self.pos[1] + self.speed)

        if self.next_pos == self.pos:
            self.next_pos = next(self.path)
