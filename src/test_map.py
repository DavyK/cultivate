import pygame
import sys


pygame.init()
screen = pygame.display.set_mode((600, 600))

clock = pygame.time.Clock()


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


b = Blob(0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)


    b.update()
    screen.fill((255, 255, 255))
    b.draw(screen)

    pygame.display.flip()
    clock.tick(60)
