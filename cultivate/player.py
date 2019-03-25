
import pygame
from pygame import font
from pygame.sprite import Sprite
from cultivate.loader import get_character
from cultivate.settings import WIDTH, HEIGHT, SM_FONT


def display_current_pickup(surface, pickup):
    # TODO: placeholder - we will need a different way of showing what the current pick up is
    text = SM_FONT.render(str(pickup), True, (0,0,0))
    inventory_box_rect = (WIDTH // 2, HEIGHT - 100, 300, 150)
    text_rect = (WIDTH // 2 + 30, HEIGHT - 90, 300, 150)
    pygame.draw.rect(surface, (200,200,200), inventory_box_rect)
    surface.blit(text, text_rect)


class Player(Sprite):
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = get_character()
        self.x = x - self.image.get_width() // 2
        self.y = y - self.image.get_height() // 2

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self._pickup = None

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        display_current_pickup(surface, self.pickup)

    def tooltip_boundary(self, view_port):
        return pygame.Rect(
            self.rect.x - 25,
            self.rect.y - 25,
            self.rect.width + 50,
            self.rect.height + 50
        )

    @property
    def pickup(self):
        return self._pickup

    @pickup.setter
    def pickup(self, item):
        self._pickup = item
