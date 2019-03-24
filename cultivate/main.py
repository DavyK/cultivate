#!/usr/bin/env python3
import pygame
import sys

from npc import Npc

WIDTH = 600
HEIGHT = 600
MAP = pygame.image.load("cultivate/assets/map.png")

class Map():
    def __init__(self, image):
        self.image = image
        self.map_view_x = WIDTH
        self.map_view_y = HEIGHT
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.left = 0
        self.right = self.width - WIDTH
        self.up = 0
        self.down = self.height - HEIGHT
        self.move_amount = 5

    def update_map_view(self, key_pressed):
        if key_pressed[pygame.K_DOWN]:
            if self.map_view_y <= self.down - self.move_amount:
                self.map_view_y += self.move_amount
        elif key_pressed[pygame.K_UP]:
            if self.map_view_y >= self.up + self.move_amount:
                self.map_view_y -= self.move_amount
        elif key_pressed[pygame.K_RIGHT]:
            if self.map_view_x <= self.right - self.move_amount:
                self.map_view_x += self.move_amount
        elif key_pressed[pygame.K_LEFT]:
            if self.map_view_x >= self.left + self.move_amount:
                self.map_view_x -= self.move_amount

    def get_viewport(self):
        return pygame.Rect(self.map_view_x, self.map_view_y,
                           self.map_view_x+WIDTH,
                           self.map_view_y+HEIGHT)

    def draw(self, surface):
        surface.blit(self.image, (0, 0), area=(self.map_view_x, self.map_view_y,
                                               self.map_view_x+WIDTH, self.map_view_y+HEIGHT))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Blob():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 100, 0), (self.x, self.y),  5)


def main():
    # init
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    npc = Npc([(300, 300), (300, 400), (400, 400), (400, 300)])
    b = Blob(WIDTH//2, HEIGHT//2)
    m = Map(MAP)
    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        m.update_map_view(pygame.key.get_pressed())
        npc.update()

        m.draw(screen)
        b.draw(screen)
        npc.draw(screen, m.get_viewport())

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
