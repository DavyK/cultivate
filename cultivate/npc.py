from itertools import cycle
import time
import random
import pygame

from cultivate.loader import get_npc5, get_npc_cat, get_pentagram
from cultivate.settings import WIDTH, HEIGHT, MD_FONT
from cultivate.conversation_tree import ConversationTree
from cultivate.tasks import task_conversations



SPEECH = [
    "Hey. How's it going?",
    "Did you get the lemon?"
    ]


SPEECH_FOLLOWERS = [
    "Oooh",
    "Aaah",
    "This place is so pretty!",
    "I can't wait to live a long life here"
]

BACKGROUND = pygame.Color(245, 245, 220)
FOREGROUND = pygame.Color(0, 0, 0)


class TimedDialogue:
    def __init__(self, text, duration):
        padding = 10

        text_width, text_height = MD_FONT.size(text)

        self.image = pygame.Surface((text_width + padding * 2,
                                     text_height + padding * 2))
        pygame.draw.rect(self.image, BACKGROUND,
                         (0, 0, *self.image.get_size()))
        self.image.blit(MD_FONT.render(text, True, FOREGROUND), (padding, padding))

        self.expired = time.time() + duration

    def draw(self, screen, x, y):
        # Draw centered above this point
        if self.expired >= time.time():
            screen.blit(self.image,
                        (x - self.image.get_rect().w // 2,
                         y - self.image.get_rect().bottom - 10))
            return True
        return False


class Npc(pygame.sprite.Sprite):
    def __init__(self, speed=3):
        super().__init__()

        self.path = cycle(self.points)
        self.x, self.y = next(self.path)
        self.next_x, self.next_y = next(self.path)

        self.image = self.get_images().getCurrentFrame()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = speed
        self.paused = False

        self.tips = SPEECH
        self.dialogue = None
        self.pause_between_tips = 5
        self.next_helpful_hint = time.time() + self.pause_between_tips

        self.conversation = None
        self.in_conversation = False

        self.action = 'talk'

    def get_images(self, direction=None):
        return get_npc5(direction=direction)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.dialogue:
            present = self.dialogue.draw(surface, self.rect.centerx, self.rect.y)
            if not present:
                self.dialogue = None
                self.next_helpful_hint = time.time() + self.pause_between_tips

    def update(self, viewport):
        rect_near_player = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 200)

        if not self.dialogue and self.next_helpful_hint <= time.time():
            self.dialogue = TimedDialogue(random.choice(self.tips), 5)

        direction = None

        if not self.rect.colliderect(rect_near_player):
            if self.next_x > self.x + self.speed:
                direction = 'right'
                self.x += self.speed
            elif self.next_x < self.x - self.speed:
                direction = 'left'
                self.x -= self.speed
            elif self.next_y < self.y - self.speed:
                direction = 'backward'
                self.y -= self.speed
            elif self.next_y > self.y + self.speed:
                direction = 'forward'
                self.y += self.speed
            else:
                self.x = self.next_x
                self.y = self.next_y
                try:
                    self.next_x, self.next_y = next(self.path)
                except:
                    self.next_x, self.next_y = self.x, self.y
        self.image = self.get_images(direction=direction).getCurrentFrame()
        self.rect.x = self.x - viewport.x
        self.rect.y = self.y - viewport.y

    @property
    def help_text(self):
        return None

    def get_conversations(self):
        return None

    @property
    def interaction_result(self):
        return self.get_conversations()


class Susan(Npc):
    name = "Susan"
    points = [
        (1000, 1000),
        (1000, 1200),
        (1200, 1200),
        (1200, 1000),
    ]


# TOTALLY an NPC
class Pentagram(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 3010
        self.y = 870
        self.image = pygame.transform.scale(get_pentagram(), (540, 540))
        self.rect = self.image.get_rect()

    def update(self, view_port):
        self.rect.x = self.x - view_port.x
        self.rect.y = self.y - view_port.y
        print(self.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    @property
    def help_text(self):
        return None

    @property
    def interaction_result(self):
        return None


class NpcFollowerBackup(Npc):
    def __init__(self, x, y, game_map):
        self.points = [(x, y)]
        super().__init__(speed=2+random.random()*3)
        self.x, self.y = x, y
        self.path = iter(self.points)
        self.next_x, self.next_y = x, y
        self.game_map = game_map
        self.tips = SPEECH_FOLLOWERS

    def update(self, viewport):

        prev_x = self.x
        prev_y = self.y

        super().update(viewport)

        if pygame.sprite.spritecollide(self, self.game_map.passables, False) or not pygame.sprite.spritecollide(self, self.game_map.impassables, False):
            self.next_x, self.next_y = (viewport.centerx, viewport.centery)
        else:
            self.next_x, self.next_y = self.x, self.y
            self.rect.x = prev_x - viewport.x
            self.rect.y = prev_y - viewport.y

class NpcFollower(Npc):
    name = "follower"
    def __init__(self, x, y):
        self.points = [(x, y)]
        super().__init__(speed=5+random.random()*5)
        self.x, self.y = x, y
        self.path = iter(self.points)
        self.next_x, self.next_y = x, y
        self.tips = SPEECH_FOLLOWERS
        self.pause_between_tips = 5+random.random()*10
        self.next_helpful_hint = time.time() + self.pause_between_tips

        self.conversation = [
            {'text': "I'm so happy to be invited to be part of this community",
             'responses': []
            }]

    def update(self, viewport):
        super().update(viewport)
        self.next_x, self.next_y = (viewport.centerx, viewport.centery)


class NpcQuester(Npc):
    name = "Quester"
    points = [
        (1800, 900),
        (1300, 900),
        (1300, 1500),
        (1800, 1500),
    ]

    def __init__(self):
        super().__init__()
        self.dialogue = TimedDialogue("!", 99999)

    def get_conversations(self):
        return {
            task_name: ConversationTree(npc_name=self.name, conversation_data=task_conv_data)
            for task_name, task_conv_data in task_conversations.items()
        }

    def get_images(self, direction=None):
        return get_npc_cat(direction=direction)

    @property
    def help_text(self):
        msg = f'{self.action}'
        if self.name:
            msg += f' to {self.name}'
        return msg
