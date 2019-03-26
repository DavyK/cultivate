import pygame
from cultivate.settings import WIDTH, HEIGHT, MD_FONT

# BORDER = pygame.Color(255, 255, 255)
BACKGROUND = pygame.Color(100, 120, 120)
FOREGROUND = pygame.Color(0, 0, 0)


class Dialogue:
    def __init__(self):
        self.render = None
        self.rect = pygame.Rect(WIDTH//2, HEIGHT // 2, 300, 50)
        # self.border_rect = pygame.Rect(WIDTH//2 - 10, HEIGHT - 50 + 10, WIDTH//2 + 20, 60)

    def set_text(self, text):
        self.render = MD_FONT.render(text, True, FOREGROUND)

    def clear(self):
        self.render = None

    def draw(self, surface):
        if self.render:
            # pygame.draw.rect(surface, BORDER, self.border_rect)
            pygame.draw.rect(surface, BACKGROUND, self.rect)
            surface.blit(self.render, self.rect)
