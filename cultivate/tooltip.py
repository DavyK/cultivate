from datetime import date, timedelta
import pygame
from cultivate import loader
from cultivate.settings import WIDTH, HEIGHT, MD_FONT, SM_FONT

BACKGROUND = pygame.Color(245, 245, 220)
FONT_COLOR = pygame.Color("black")


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
        font_width, font_height = MD_FONT.size(text)
        self.rect.width = font_width + (self.padding * 2)
        self.render = MD_FONT.render(text,
                                     True, FONT_COLOR)

    @property
    def empty(self):
        return self.render is None

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
        rect = self.rect
        if self.name:
            font_width, _ = MD_FONT.size(self.name)
            rect.width = max(rect.width, font_width + (self.padding * 2))
            rect.x = WIDTH - rect.width
        else:
            rect.width = self.width
            rect.x = WIDTH - self.width

        scaled_image = pygame.transform.scale(self.image, (rect.w, rect.h))
        surface.blit(scaled_image, rect)
        if self.icon:
            icon_x = rect.x + rect.width // 2 - self.icon.get_width() // 2
            icon_y = rect.y + rect.height // 2 - self.icon.get_width() // 2
            surface.blit(self.icon, (icon_x, icon_y))
        if self.name:
            surface.blit(MD_FONT.render(self.name, True, FONT_COLOR),
                         (rect.x + self.padding, rect.y + self.padding))

class InfoBox:
    def __init__(self, game_state):
        self.image = loader.get_info_box()
        self.width, self.height = self.image.get_size()
        self.game_state = game_state
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.day_zero = date(1966, 5, 31)
        self.padding = 15

    @property
    def current_date(self):
        day = self.day_zero + timedelta(days=self.game_state.day)
        return day.strftime('%d/%m/%Y')


    def draw(self, surface):
        font_width, font_height = MD_FONT.size(self.current_date)
        rect = self.rect
        if self.game_state.current_task:
            font_width, _ = MD_FONT.size(self.game_state.current_task)
            rect.width = max(rect.width, font_width + (self.padding * 2))
        else:
            rect.width = self.width
        scaled_image = pygame.transform.scale(self.image, (rect.w, rect.h))
        surface.blit(scaled_image, rect)
        surface.blit(
            MD_FONT.render(self.current_date, True, FONT_COLOR),
            (self.rect.x + self.padding, self.rect.y + self.padding)
        )
        if self.game_state.current_task:
            surface.blit(
                SM_FONT.render(self.game_state.current_task, True, FONT_COLOR),
                (self.rect.x + self.padding, self.rect.y + self.padding + font_height + self.padding)
            )
