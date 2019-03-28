from datetime import date, timedelta
import pygame
from cultivate import loader
from cultivate.settings import WIDTH, HEIGHT, MD_FONT, SM_FONT

BACKGROUND = pygame.Color(100, 120, 120)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

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
        self.rect = pygame.Rect(0, HEIGHT-50, 250, 50)
        self.padding = 20

    def set_tooltip(self, text):
        self.render = MD_FONT.render(text,
                                     True, WHITE)

    def clear_tooltip(self):
        self.render = None

    def draw(self, surface):
        if self.render:
            pygame.draw.rect(surface, BACKGROUND, self.rect)
            surface.blit(self.render, pad_rect(self.rect, self.padding))


class InventoryBox:
    def __init__(self):
        self.image = loader.get_inventory_box()
        self.width, self.height = self.image.get_size()
        self.rect = pygame.Rect(WIDTH-self.width, 0, self.width, self.height)
        self.icon = None
        self.name = ""
        self.padding = 10

    def set_icon(self, item):
        print('set icon: ', item)
        if item:
            self.icon = item.image
            if hasattr(item, 'name'):
                self.name = item.name
        else:
            self.clear_icon()

    def clear_icon(self):
        self.icon = None
        self.name = ""

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.icon:
            icon_x = self.rect.x + self.rect.width // 2 - self.icon.get_width() // 2
            icon_y = self.rect.y + self.rect.height // 2 - self.icon.get_width() // 2
            surface.blit(self.icon, (icon_x, icon_y))
        if self.name:
            surface.blit(MD_FONT.render(self.name, True, WHITE),
                         (self.rect.x + self.padding, self.rect.y + self.padding))

class InfoBox:
    def __init__(self):
        self.image = loader.get_info_box()
        self.width, self.height = self.image.get_size()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.day_zero = date(1966, 5, 31)
        self.day = 0
        self.task = None
        self.padding = 15

    def set(self, day, task=None):
        self.day = day
        self.task = task

    def clear_task(self):
        self.task = None

    @property
    def current_date(self):
        day = self.day_zero + timedelta(days=self.day)
        return day.strftime('%d/%m/%Y')


    def draw(self, surface):
        font_width, font_height = MD_FONT.size(self.current_date)
        surface.blit(self.image, self.rect)
        surface.blit(
            MD_FONT.render(self.current_date, True, WHITE),
            (self.rect.x + self.padding, self.rect.y + self.padding)
        )
        if self.task:
            surface.blit(
                SM_FONT.render(self.task, True, WHITE),
                (self.rect.x + self.padding, self.rect.y + self.padding + font_height + self.padding)
            )
