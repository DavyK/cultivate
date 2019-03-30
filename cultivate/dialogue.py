import pygame
from cultivate.loader import get_conversation_box
from cultivate.settings import WIDTH, HEIGHT, MD_FONT

FOREGROUND = pygame.Color(0, 0, 0)
DE_EMPH = pygame.Color("lightgray")

def drawText(surface, text, color, rect, font, line_sp=2):
    rect = pygame.Rect(rect)
    y = rect.top

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        image = font.render(text[:i], True, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_sp

        # remove the text we just blitted
        text = text[i:]

    return y, text


class Dialogue:
    def __init__(self):
        self.width = 1100
        self.height = 250
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

        # This text can be long. We need to wrap the line,
        # if it's longer than the width of the padded dialogue box
        text_rect = pygame.Rect(
            pd,
            pd + (font_height + pd),
            (self.width - self.padding * 2),
            (self.height - self.padding * 2),
        )
        text_height, _ = drawText(self.render, text, FOREGROUND, text_rect, MD_FONT)
        text_height += pd

        for idx, (key, response_text) in enumerate(responses):
            self.render.blit(MD_FONT.render(
                f'{idx+1} => {response_text}', True, FOREGROUND),
                (
                    pd,
                    text_height + ((font_height + pd // 2) * (idx)),
                )
            )

        quit_msg = 'press q to quit'
        quit_width, quit_height = MD_FONT.size(quit_msg)
        self.render.blit(
            MD_FONT.render(quit_msg, True, DE_EMPH),
            (
                self.width - pd - quit_width,
                self.height - pd - quit_height,
            )
        )

    def draw(self, surface):
        surface.blit(self.render, self.rect)
