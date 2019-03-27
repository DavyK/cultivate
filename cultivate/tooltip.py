import pygame
from cultivate.settings import WIDTH, HEIGHT, MD_FONT

BACKGROUND = pygame.Color(100, 120, 120)
FOREGROUND = pygame.Color(0, 0, 0)

def pad_rect(rect, padding):
    return pygame.Rect(
        rect.x + padding,
        rect.y + padding,
        rect.width - padding,
        rect.height - padding
    )


class Tooltip:
    def __init__(self):
        self.render = None
        self.rect = pygame.Rect(0, HEIGHT-50, 200, 50)
        self.padding = 20

    def set_tooltip(self, obj):
        if hasattr(obj, 'get_help_text'):
            self.render = MD_FONT.render(f'press x to {obj.get_help_text()}',
                                         True, FOREGROUND)

    def clear_tooltip(self):
        self.render = None

    def draw(self, surface):
        if self.render:
            pygame.draw.rect(surface, BACKGROUND, self.rect)
            surface.blit(self.render, pad_rect(self.rect, self.padding))
