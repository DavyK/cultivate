import pygame
from pygame.sprite import DirtySprite
from cultivate.settings import WIDTH, HEIGHT


class BasePickUp(DirtySprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y


class Lemon(BasePickUp):
    name = 'lemon'
    color = (255, 244, 79)
    size = (50, 50)
