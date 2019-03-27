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
        self.image = get_conversation_box()
        self.render = None
        self.rect = pygame.Rect(0, HEIGHT - self.height, self.width, self.height)
        self.padding = 10

    def set_data(self, npc_name, text, responses):
        font_width, font_height = MD_FONT.size(text)
        self.render = self.image.copy()

        pd = self.padding

        self.render.blit(
            MD_FONT.render(npc_name, True, FOREGROUND),
            (pd, pd)
        )

        self.render.blit(
            MD_FONT.render(text, True, FOREGROUND),
            (
                pd,
                pd + (font_height + pd),
            )
        )

        for idx, (key, response_text) in enumerate(responses):
            self.render.blit(MD_FONT.render(
                f'{idx+1} => {response_text}', True, FOREGROUND),
                (
                    pd,
                    pd + ((idx + 2) * (pd + font_height)),
                )
            )

        if not responses:
            self.render.blit(
                MD_FONT.render('press q to quit', True, FOREGROUND),
                (
                    pd,
                    2 * (pd  + font_height),
                )
            )

    def draw(self, surface):
        surface.blit(self.render, self.rect)
