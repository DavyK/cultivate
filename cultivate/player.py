
import pygame
from pygame import font
from pygame.sprite import Sprite
from cultivate.loader import get_character
from cultivate.settings import WIDTH, HEIGHT, SM_FONT


def display_current_pickup(surface, pickup):
    # TODO: placeholder - we will need a different way of showing what the current pick up is
    text = SM_FONT.render(str(pickup), True, (0, 0, 0))
    inventory_box_rect = (WIDTH // 2, HEIGHT - 100, 300, 150)
    text_rect = (WIDTH // 2 + 30, HEIGHT - 90, 300, 150)
    pygame.draw.rect(surface, (200, 200, 200), inventory_box_rect)
    surface.blit(text, text_rect)


class Player(Sprite):
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = get_character()
        self.rect = self.image.getCurrentFrame().get_rect()
        self.x = x - self.rect.width // 2
        self.y = y - self.rect.height // 2

        self.rect.x = self.x
        self.rect.y = self.y
        self._pickup = None
        self._direction = None

    def draw(self, surface, key_pressed):
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.image = get_character('forward')
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.image = get_character('backward')
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.image = get_character('right')
        elif key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.image = get_character('left')
        else:
            self.image = get_character()
        surface.blit(self.image.getCurrentFrame(), (self.x, self.y))
        display_current_pickup(surface, self.pickup)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def pickup(self):
        return self._pickup

    @pickup.setter
    def pickup(self, item):
        self._pickup = item
    
    def tooltip_boundary(self, view_port):
        return pygame.Rect(
            self.rect.x - 25,
            self.rect.y - 25,
            self.rect.width + 50,
            self.rect.height + 50
        )
