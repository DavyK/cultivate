from itertools import cycle
import time
import random
import pygame

from cultivate.loader import get_character, get_npx
from cultivate.settings import WIDTH, HEIGHT, MD_FONT
from cultivate.dialogue import Dialogue


K_INTERACT = pygame.K_x
K_QUIT_INTERACTION = pygame.K_q
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
    def __init__(self, points, speed=3):
        super().__init__()

        self.points = points
        self.path = cycle(points)
        self.x, self.y = next(self.path)
        self.next_x, self.next_y = next(self.path)

        self.image = get_npc().getCurrentFrame()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = speed
        self.paused = False

        self.dialogue = None
        self.pause_between_tips = 5
        self.next_helpful_hint = time.time() + self.pause_between_tips

        self.conversation = 'some object'
        self.conversation_started = False
        self.conversation_finished = False

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
        self.image = get_npc(direction).getCurrentFrame()
        self.rect.x = self.x - viewport.x
        self.rect.y = self.y - viewport.y

    def get_help_text(self):
        return "Press X to talk"

    def is_in_conversation(self):
        return self.conversation_started and not self.conversation_finished

    def interact(self, key):
        if key[K_QUIT_INTERACTION]:
            self.conversation_finished = True
            return

        if self.is_in_conversation() or key[K_INTERACT]:
            self.conversation_started = True
            self.conversation_finished = False
            d = Dialogue()
            d.set_text('this is a test')

            return d
