
import pygame
from pygame import font
from pygame.sprite import Sprite
from cultivate.loader import get_player
from cultivate.dialogue import Dialogue
from cultivate.conversation_tree import ConversationTree
from cultivate.sprites.bed import Bed
from cultivate.settings import WIDTH, HEIGHT, SM_FONT


def display_current_pickup(surface, pickup):
    # TODO: placeholder - we will need a different way of showing what the current pick up is
    text = SM_FONT.render(str(pickup), True, (0, 0, 0))
    inventory_box_rect = (WIDTH // 2, HEIGHT - 100, 300, 150)
    text_rect = (WIDTH // 2 + 30, HEIGHT - 90, 300, 150)
    pygame.draw.rect(surface, (200, 200, 200), inventory_box_rect)
    surface.blit(text, text_rect)


class Player(Sprite):
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = get_player()
        self.rect = self.image.getCurrentFrame().get_rect()
        self.x = x - self.rect.width // 2
        self.y = y - self.rect.height // 2

        self.rect.x = self.x
        self.rect.y = self.y
        self._pickup = None
        self._direction = None
        self.conversation = None
        self.sleeping = False
        self.nearby_interactable = None
        self.interacting_with = None

    def draw(self, surface, key_pressed):
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.image = get_player('forward')
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.image = get_player('backward')
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.image = get_player('right')
        elif key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.image = get_player('left')
        else:
            self.image = get_player()

        if self.conversation:
            self.image = get_player()
        surface.blit(self.image.getCurrentFrame(), (self.x, self.y))

        if self.conversation:
            d = Dialogue()
            d.set_data(
                self.conversation.npc_name,
                self.conversation.current['text'],
                self.conversation.current['responses']
            )
            d.draw(surface)



    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def pickup(self):
        return self._pickup

    @pickup.setter
    def pickup(self, item):
        self._pickup = item

    def tooltip_boundary(self, view_port):
        return pygame.Rect(
            self.rect.x - 25,
            self.rect.y - 25,
            self.rect.width + 50,
            self.rect.height + 50
        )

    def end_conversation(self):
        self.conversation = None
        print('ending conversation')

    def set_nearby(self, thing):
        self.nearby_interactable = thing

    def key_press(self, key):
        if key == pygame.K_x:
            self.start_interact()
        elif key == pygame.K_q:
            self.stop_interact()
        elif self.conversation:
            self.conversation.progress(key)


    def start_interact(self):
        if self.interacting_with is None and self.nearby_interactable is not None:
            self.interacting_with = self.nearby_interactable
            if isinstance(self.interacting_with.interaction_result, ConversationTree):
                self.conversation = self.interacting_with.interaction_result
            if isinstance(self.interacting_with.interaction_result, Bed):
                self.sleeping = True
                self.map.fader.start()
                self.interacting_with = None

    def stop_interact(self):
        if self.interacting_with == self.nearby_interactable and self.interacting_with is not None:
            if isinstance(self.interacting_with.interaction_result, ConversationTree):
                self.conversation = None
            if isinstance(self.interacting_with.interaction_result, Bed):
                self.sleeping = False
            self.interacting_with = None
