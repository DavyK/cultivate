import pygame
from cultivate.settings import MAP_WIDTH, MAP_HEIGHT, MD_FONT

BLACK = pygame.Color(0, 0, 0)


class Fader:
    def __init__(self):
        self.fade = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.opacity = 0
        self.opacity_step = 2
        self.increasing = True
        self.fading = False
        self.black = False
        self.rect = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)

    def start(self):
        self.fading = True

    def stop(self):
        self.fading = False

    def reset(self):
        self.opacity = 0
        self.increasing = True
        self.fading = False

    def draw(self, surface):
        self.fade.set_alpha(self.opacity)
        pygame.draw.rect(self.fade, BLACK, self.rect)
        surface.blit(self.fade, self.rect)
        self.adjust_opacity()

    def adjust_opacity(self):
        if not self.increasing and self.opacity <= 0:
            self.reset()

        if self.increasing:
            self.opacity += self.opacity_step
        else:
            self.opacity -= self.opacity_step

        if self.opacity < 0:
            self.increasing = True
        elif self.opacity > 255:
            self.increasing = False

        if self.opacity > 230 and self.opacity < 255:
            self.black = True
        else:
            self.black = False








