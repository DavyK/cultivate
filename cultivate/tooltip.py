import pygame
from cultivate.settings import WIDTH, HEIGHT, MD_FONT

BACKGROUND = pygame.Color(100, 120, 120)
FOREGROUND = pygame.Color(0, 0, 0)


class Tooltip:
    def __init__(self):
        self.render = None
        self.rect = pygame.Rect(WIDTH//2, HEIGHT-50, WIDTH//2, 50)

    def set_tooltip(self, obj):
        if hasattr(obj, 'get_help_text'):
            self.render = MD_FONT.render(obj.get_help_text(),
                                         True, FOREGROUND)

    def clear_tooltip(self):
        self.render = None

    def draw(self, surface):
        if self.render:
            pygame.draw.rect(surface, BACKGROUND, self.rect)
            surface.blit(self.render, self.rect)
