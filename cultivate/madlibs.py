import collections
import logging
import string
import typing

import pygame

from cultivate import settings


class Madlibs:
    box_border = min(settings.WIDTH // 10, settings.HEIGHT // 10)
    box_rect = pygame.Rect(box_border, box_border,
                           settings.WIDTH - 2 * box_border,
                           settings.HEIGHT - 2 * box_border)
    text_border = box_border // 2
    text_rect = pygame.Rect(box_rect.x + text_border,
                            box_rect.y + text_border,
                            box_rect.w - 2 * text_border,
                            box_rect.h - 2 * text_border)
    font = settings.LG_FONT
    background_color = pygame.Color("saddlebrown")
    text_color = pygame.Color("black")
    text_editable_color = pygame.Color("yellow")
    text_editing_color = pygame.Color("green")

    def __init__(self, format_string: str, format_dict: collections.OrderedDict):
        """
        :param format_string: a format with named parameters that the player can change
        :param format_dict: containing default values for all the format parameters
        """
        self.unformattted_prose = format_string
        self.changed_words = format_dict
        self.selected_word_index = 0
        self.editable_words = len(format_dict.keys())

        # test that format_dict has all the required format parameters
        self.unformattted_prose.format_map(format_dict)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the madlibs box onto {surface}.

        :param surface: To blit the madlibs box to. Expected to be {settings.WIDTH x settings.HEIGHT}.
        """
        # draw background
        pygame.draw.rect(surface, self.background_color, self.box_rect)

        # calculate words and word_colors
        unformatted_words = self.unformattted_prose.split(" ")
        words = []
        word_colors = []
        words_formatted_count = 0
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

        # draw words
        self.draw_text(surface, words, word_colors)

    def draw_text(self, surface: pygame.Surface, words: typing.List[str],
                  word_colors: typing.List[pygame.Color]) -> None:
        cursor_y = self.text_rect.top

        # get the height of the font
        font_height = self.font.size("Tg")[1]

        while len(words) > 0:
            # number of words on this line
            i = 1

            # determine if the row of text will be outside our area
            if cursor_y + font_height > self.text_rect.bottom:
                # give up rendering text and stop where we are
                logging.error("Could not fit all of the text onto screen")
                break

            # try and fit more words on this line
            while self.font.size(" ".join(words[:i + 1]))[0] < self.text_rect.width and i < len(words):
                i += 1

            # render the words
            rendered_words = []
            rendered_space = self.font.render(" ", True, self.text_color)
            for word, word_color in zip(words[:i], word_colors[:i]):
                if word[-1] not in string.ascii_lowercase:
                    # always render punctuation at the end of a word in {self.text_color}
                    rendered_words.append(self.font.render(word[:-1], True, word_color))
                    rendered_words.append(self.font.render(word[-1], True, self.text_color))
                else:
                    rendered_words.append(self.font.render(word, True, word_color))
                rendered_words.append(rendered_space)

            # blit the rendered words to the surface
            cursor_x = self.text_rect.left
            for rendered_word in rendered_words:
                surface.blit(rendered_word, (cursor_x, cursor_y))
                cursor_x += rendered_word.get_width()

            cursor_y += font_height + 2

            # remove the text we just blitted
            words = words[i:]
            word_colors = word_colors[i:]

    def handle_keypress(self, key) -> None:
        if key == pygame.K_TAB or key == pygame.K_RETURN:
            self.selected_word_index += 1
            if self.selected_word_index >= len(self.changed_words):
                self.selected_word_index = 0

        selected_word = list(self.changed_words.keys())[self.selected_word_index]
        if key == pygame.K_BACKSPACE:
            word = self.changed_words[selected_word]
            self.changed_words[selected_word] = word[:-1]

        letter = pygame.key.name(key)
        if letter in string.ascii_lowercase:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                letter = letter.upper()
            self.changed_words[selected_word] += letter
