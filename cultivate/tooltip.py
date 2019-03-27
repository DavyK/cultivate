import pygame
from cultivate.loader import get_inventory_box
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

    def set_tooltip(self, text):
        self.render = MD_FONT.render(text,
                                     True, FOREGROUND)

    def clear_tooltip(self):
        self.render = None

    def draw(self, surface):
        if self.render:
            pygame.draw.rect(surface, BACKGROUND, self.rect)
            surface.blit(self.render, pad_rect(self.rect, self.padding))


class InventoryBox:
    def __init__(self):
        self.image = get_inventory_box()
        self.width, self.height = self.image.get_size()
        self.rect = pygame.Rect(WIDTH-self.width, 0, self.width, self.height)
        self.icon = None
        self.padding = 10

    def set_icon(self, icon):
        self.icon = icon

    def clear_icon(self):
        self.icon = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.icon:
            icon_x = self.rect.x + self.rect.width // 2 - self.icon.get_width() // 2
            icon_y = self.rect.y + self.rect.height // 2 - self.icon.get_width() // 2
            surface.blit(self.icon, (icon_x, icon_y))
