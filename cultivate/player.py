import pygame
from pygame.sprite import Sprite
from cultivate.loader import get_player
from cultivate.dialogue import Dialogue
from cultivate.conversation_tree import ConversationTree
from cultivate.madlibs import Madlibs
from cultivate.sprites.bed import Bed
from cultivate.sprites.grave import Grave
from cultivate.sprites.pickups import Shovel, Flower


class Player(Sprite):
    def __init__(self, x, y, game_state):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = get_player()
        self.rect = self.image.getCurrentFrame().get_rect()
        self.x = x - self.rect.width // 2
        self.y = y - self.rect.height // 2

        self.game_state = game_state
        self.rect.x = self.x
        self.rect.y = self.y
        self._pickup = None
        self._direction = None
        self.conversation = None
        self.madlibs = None
        self.sleeping = False
        self.nearby_interactable = None
        self.interacting_with = None
        self.inventory = None

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

        surface.blit(self.image.getCurrentFrame(), (self.x, self.y))

        if self.conversation:
            d = Dialogue()
            d.set_data(
                self.conversation.npc_name,
                self.conversation.current['text'],
                self.conversation.current['responses']
            )
            d.draw(surface)

        if self.madlibs is not None:
            self.madlibs.draw(surface)

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

    def set_nearby(self, thing):
        self.nearby_interactable = thing

    def key_press(self, key):
        if self.interacting_with is not None and key == pygame.K_ESCAPE:
            self.stop_interact()
            return
        if self.madlibs is not None:
            self.madlibs.handle_keypress(key)
            return
        if self.conversation:
            self.conversation.progress(key)
            return
        if key == pygame.K_x:
            self.start_interact()
            return

    def start_interact(self):
        if self.interacting_with is None and self.nearby_interactable is not None:
            self.interacting_with = self.nearby_interactable

            if isinstance(self.interacting_with.interaction_result, ConversationTree):
                self.conversation = self.interacting_with.interaction_result

            elif (
                isinstance(self.interacting_with.interaction_result, dict) and all([
                    isinstance(thing, ConversationTree)
                    for thing in self.interacting_with.interaction_result.values()
                ])
            ):
                conversations = self.interacting_with.interaction_result
                if self.game_state.current_task:
                    self.conversation = conversations[self.game_state.current_task]
                else:
                    self.conversation = None
                    self.interacting_with = None

            elif isinstance(self.interacting_with.interaction_result, Bed):
                if self.game_state.is_day_done():
                    self.game_state.next_day()
                    self.interacting_with = None

                else:
                    self.interacting_with = self
                    self.nearby_interactable = self
                    self.conversation = ConversationTree(
                        npc_name='You', conversation_data=[
                            {'text': "Hmm. I think there was something I was supposed to do...",
                             'responses': []
                            }])


            elif isinstance(self.interacting_with.interaction_result, Madlibs):
                self.madlibs = self.interacting_with.interaction_result

            elif (
                isinstance(self.interacting_with.interaction_result, Grave) and
                isinstance(self.pickup, Shovel)
            ):
                self.interacting_with.dig()
                self.interacting_with = None
                self.game_state.complete_task()

            elif (
                isinstance(self.interacting_with.interaction_result, Grave) and
                self.interacting_with.interaction_result.dug and
                isinstance(self.pickup, Flower)
            ):
                self.interacting_with.plant()
                self.interacting_with = None
                self.pickup = None
                self.inventory.clear_icon()
                self.game_state.sabotage_task()
            else:
                self.interacting_with = None

    def stop_interact(self):
        if self.interacting_with == self.nearby_interactable and self.interacting_with is not None:
            if (
                isinstance(self.interacting_with.interaction_result, dict) and all([
                    isinstance(thing, ConversationTree)
                    for thing in self.interacting_with.interaction_result.values()
                ])
            ):
                self.conversation = None

            elif isinstance(self.interacting_with.interaction_result, Madlibs):
                print(self.madlibs.changed_words)
                self.madlibs = None
            self.interacting_with = None
        else:
            self.conversation = None
            self.interacting_with = None
