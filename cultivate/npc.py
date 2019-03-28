from itertools import cycle
import time
import random
import pygame

from cultivate.loader import get_npc5, get_character, get_npc, get_npc_cat
from cultivate.settings import WIDTH, HEIGHT, MD_FONT
from cultivate.dialogue import Dialogue
from cultivate.conversation_tree import ConversationTree



SPEECH = [
    "Hey. How's it going?",
    "Did you get the lemon?"
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

        self.dialogue = None
        self.pause_between_tips = 5
        self.next_helpful_hint = time.time() + self.pause_between_tips

        self.converastion = 'some object'
        self.in_conversation = False

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
            self.dialogue = TimedDialogue(random.choice(SPEECH), 5)

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
                self.next_x, self.next_y = next(self.path)
        self.image = get_npc5(direction).getCurrentFrame()
        self.rect.x = self.x - viewport.x
        self.rect.y = self.y - viewport.y

    def get_help_text(self):
        return "Talk."

    def get_conversations(self):
        return [
            ConversationTree(npc_name=self.name, conversation_data=c)
            for c in self.conversations
        ]
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

    conversations = [
        [
            {
                'text': 'Did you get the lemon yet?',
                'responses': [(1, 'yes'), (2, 'no'), (3, "I don't know where it is")],
            },
            {
                'text': 'Great! now make some lemonade!',
                'responses': [(4, 'ok')],
            },
            {
                'text': "Then go get it! It's in the building" ,
                'responses': [(4, 'Thanks!')],
            },
            {
                'text': "It's in the building!",
                'responses': [(4, 'Thanks!')],
            },
            {
                'text': 'Byeeeeeee!',
                'responses': [],
            },
        ],
        [
            {
                'text': 'Wash the white robes for ceremony',
                'responses': [(1, 'No'), (2, 'where do I wash them?')],
            },
            {
                'text': 'Rude!',
                'responses': [],
            },
            {
                'text': 'Get some soap, put the robes in water with soap, scrub!',
                'responses': [(1, 'obviously!')]
            }
        ]
    ]




