from itertools import cycle
import time
import random
import pygame

from cultivate.loader import get_npc5, get_character, get_npc, get_npc_cat
from cultivate.settings import WIDTH, HEIGHT, MD_FONT
from cultivate.dialogue import Dialogue
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

BACKGROUND = pygame.Color(100, 120, 120)
FOREGROUND = pygame.Color(0, 0, 0)


class TimedDialogue:
    def __init__(self, text, duration):
        padding = 10

        (self.width, self.height) = MD_FONT.size(text)

        self.image = pygame.Surface((self.width+padding*2, self.height+padding*2))
        pygame.draw.rect(self.image, BACKGROUND,
                         (0, 0, *self.image.get_size()))
        self.image.blit(MD_FONT.render(text, True, FOREGROUND), (padding, padding))

        self.expired = time.time() + duration

    def draw(self, screen, x, y):
        # Draw centered above this point
        if self.expired >= time.time():
            screen.blit(self.image, (x-self.width//2, y-self.height-30))
            return True
        return False


class Npc(pygame.sprite.Sprite):
    def __init__(self, speed=3):
        super().__init__()

        self.path = cycle(self.points)
        self.x, self.y = next(self.path)
        self.next_x, self.next_y = next(self.path)

        self.image = get_npc5().getCurrentFrame()
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

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.dialogue:
            present = self.dialogue.draw(surface, self.rect.x, self.rect.y)
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
        self.image = get_npc5(direction).getCurrentFrame()
        self.rect.x = self.x - viewport.x
        self.rect.y = self.y - viewport.y

    @property
    def help_text(self):
        msg = f'{self.action}'
        if self.name:
            msg += f' to {self.name}'
        return msg


    def get_conversations(self):
        if self.conversation:
            return ConversationTree(npc_name=self.name, conversation_data=self.conversation)

        return {
            task_name: ConversationTree(npc_name=self.name, conversation_data=task_conv_data)
            for task_name, task_conv_data in task_conversations.items()
        }

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

    def update(self, viewport):

        super().update(viewport)
        self.next_x, self.next_y = (viewport.centerx, viewport.centery)
