#!/usr/bin/env python3
import pygame
import sys

WIDTH = 600
HEIGHT = 600
MAP = pygame.image.load("cultivate/assets/map.png")

class Map():
    def __init__(self, image):
        self.image = image
        self.x = 0
        self.y = 0
    def draw(self, surface):
        surface.blit(self.image, (0, 0))


class Blob():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 100, 0), (self.x, self.y),  5)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= 1
        if keys[pygame.K_DOWN]:
            self.y += 1
        if keys[pygame.K_LEFT]:
            self.x -= 1
        if keys[pygame.K_RIGHT]:
            self.x += 1


def main():
    # init
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    b = Blob(0, 0)
    m = Map(MAP)
    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)


        b.update()

        m.draw(screen)
        b.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
