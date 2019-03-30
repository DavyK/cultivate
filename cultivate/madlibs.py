import collections
import logging
import os
import string
import typing
import copy

import pygame

from cultivate import loader, settings

class Madlibs:
    text_color = pygame.Color("black")
    text_editable_color = pygame.Color("0x4c60b3")
    text_editing_color = pygame.Color("0xa94cb3")

    def __init__(self, format_string: str, format_dict: collections.OrderedDict, expected_changes: collections.OrderedDict):
        """
        :param format_string: a format with named parameters that the player can change
        :param format_dict: containing default values for all the format parameters
        """
        self.unformattted_prose = format_string
        self.original_words = format_dict
        self.changed_words = copy.deepcopy(self.original_words)
        self.expected_changes = expected_changes
        self.selected_word_index = 0
        self.editable_words = len(format_dict.keys())
        # test that format_dict has all the required format parameters
        self.unformattted_prose.format_map(format_dict)

        # static inits
        self.scroll = loader.get_image(os.path.join(settings.SPRITES_DIR, "scroll.png"), True)
        self.rect = self.scroll.get_rect()
        self.font = loader.get_font("Cultivate-Regular.ttf", settings.FONT_SIZE_LG)
        self.pencil_sound = loader.get_sound("pencil.ogg")

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the madlibs box onto {surface}.

        :param surface: To blit the madlibs box to. Expected to be {settings.WIDTH x settings.HEIGHT}.
        """
        # draw background
        x = (surface.get_rect().w - self.rect.w) // 2
        y = (surface.get_rect().h - self.rect.h) // 2
        surface.blit(self.scroll, (x, y))

        # calculate rect for text to be drawn in
        text_border = min(self.rect.w // 10, self.rect.h // 10)
        text_rect = pygame.Rect(x + text_border,
                                y + text_border,
                                self.rect.w - 2 * text_border,
                                self.rect.h - 2 * text_border)

        # split prose into lines
        unformatted_lines = self.unformattted_prose.splitlines()
        lines = []
        colors = []
        words_formatted_count = 0
        for line in unformatted_lines:
            # split each line into words and calculate word_colors
            unformatted_words = line.split(" ")
            words = []
            word_colors = []
            for word in unformatted_words:
                if "{" in word and "}" in word:
                    words.append(word.format_map(self.changed_words))
                    if self.selected_word_index == words_formatted_count:
                        word_colors.append(self.text_editing_color)
                    else:
                        word_colors.append(self.text_editable_color)
                    words_formatted_count += 1
                else:
                    words.append(word)
                    word_colors.append(self.text_color)
            lines.append(words)
            colors.append(word_colors)

        # draw lines of words
        self.draw_text(surface, text_rect, lines, colors)

    def draw_text(self, surface: pygame.Surface, draw_rect: pygame.Rect,
                  lines: typing.List[typing.List[str]],
                  colors: typing.List[typing.List[pygame.Color]]) -> None:
        cursor_y = draw_rect.top

        # get the height of the font
        font_height = self.font.size("Tg")[1]

        for words, word_colors in zip(lines, colors):
            while len(words) > 0:
                # number of words on this line
                i = 1

                # determine if the row of text will be outside our area
                if cursor_y + font_height > draw_rect.bottom:
                    # give up rendering text and stop where we are
                    logging.error("Could not fit all of the text onto screen")
                    break

                # try and fit more words on this line
                while self.font.size(" ".join(words[:i + 1]))[0] < draw_rect.width and i < len(words):
                    i += 1

                # render the words
                rendered_words = []
                rendered_space = self.font.render(" ", True, self.text_color)
                for word, word_color in zip(words[:i], word_colors[:i]):
                    if word == "":
                        continue
                    if word[-1] not in string.ascii_lowercase:
                        # always render punctuation at the end of a word in {self.text_color}
                        rendered_words.append(self.font.render(word[:-1], True, word_color))
                        rendered_words.append(self.font.render(word[-1], True, self.text_color))
                    else:
                        rendered_words.append(self.font.render(word, True, word_color))
                    rendered_words.append(rendered_space)

                # blit the rendered words to the surface
                cursor_x = draw_rect.left
                for rendered_word in rendered_words:
                    surface.blit(rendered_word, (cursor_x, cursor_y))
                    cursor_x += rendered_word.get_width()

                cursor_y += font_height + 2

                # remove the text we just blitted
                words = words[i:]
                word_colors = word_colors[i:]

    @property
    def edited(self):
        for key, word in self.changed_words.items():
            if not self.original_words[key] == word:
                return True
        return False


    @property
    def correct(self):
        for key, word in self.changed_words.items():
            if not self.expected_changes[key] == word:
                return False
        return True

    def handle_keypress(self, key) -> None:
        if key == pygame.K_TAB or key == pygame.K_RETURN:
            self.selected_word_index += 1
            if self.selected_word_index >= len(self.changed_words):
                self.selected_word_index = 0

        selected_word = list(self.changed_words.keys())[self.selected_word_index]
        if key == pygame.K_BACKSPACE:
            word = self.changed_words[selected_word]
            self.changed_words[selected_word] = word[:-1]
            # self.pencil_sound.play()

        letter = pygame.key.name(key)
        if letter in string.ascii_lowercase:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                letter = letter.upper()
            self.changed_words[selected_word] += letter
            self.pencil_sound.play()
