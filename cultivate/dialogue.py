import pygame
from cultivate.loader import get_conversation_box
from cultivate.settings import WIDTH, HEIGHT, MD_FONT

# BORDER = pygame.Color(255, 255, 255)
BACKGROUND = pygame.Color(100, 120, 120)
FOREGROUND = pygame.Color(0, 0, 0)


class Dialogue:
    def __init__(self):
        self.width = 1100
        self.height = 175
        self.render = None
        self.image = get_conversation_box()
        self.rect = pygame.Rect(0, HEIGHT - self.height, self.width, self.height)
        self.inner_rect = pygame.Rect(
            25,
            HEIGHT - (self.height) + 25,
            self.width - 50,
            self.height - 50,
        )

    def set_text(self, text):
        self.render = MD_FONT.render(text, True, FOREGROUND)

    def clear(self):
        self.render = None

    def draw(self, surface):
        if self.render:
            surface.blit(self.image, self.rect)
            surface.blit(self.render, self.inner_rect)
