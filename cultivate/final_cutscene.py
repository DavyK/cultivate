from collections import namedtuple
import pygame

from cultivate.conversation_tree import ConversationTree
from cultivate.dialogue import Dialogue
from cultivate.npc import NpcSacrifice
from cultivate.sprites.pickups import BlackCandles

K_QUIT_INTERACTION = pygame.K_q

LEMONADE_DAY = 2
ROBE_DAY = 3
CANDLE_DAY = 4
MADLIB_DAY = 5

TaskSpeech = namedtuple("TaskSpeech", ["completed", "sabotaged"])

END_DIALOGUE = [
    [
        { 'text': "Ah, You're here. Now we can begin the ceremony",
          'responses': [(1, "What is it?")]},
        { 'text': "You've been here for years. It's the time where we summon our saviour, of course",
          'responses': [(2, "That sounds dubious")]},
        { 'text': "Well let's get on with it. Sacrifices, come forth!",
          'responses': []}
    ],
    TaskSpeech(
        [
            { 'text': "See, look at their beautiful pristine pure white robes. Excellent",
              'responses': [(1, "That's important?")]},
            { 'text': "Of course! Our saviour can't have an off white sacrifice!",
              'responses': [(2, "Right.")]},
            { 'text': "To the next stage. Roger. Get the candles!",
              'responses': []},
        ],
        [
            { 'text': "Wait.. Are their robes pink?! Oh no. That Damn sock. The ceremony must continue!",
              'responses': [(1, "That's important?")]},
            { 'text': "Of course! Our saviour can't have an off white sacrifice!",
              'responses': [(2, "Right.")]},
            { 'text': "To the next stage. Roger. Get the candles!",
              'responses': []}
        ]
    ),
    TaskSpeech(
        [
            { 'text': "Look at them glowing in their black gloriousness and neutral aroma. Our saviour will be most pleased!",
              'responses': [(1, "That's important?")]},
            { 'text': "Of course! Any discrepancies and we may get the wrath of our saviour",
              'responses': [(2, "Right.")]},
            { 'text': "To the next stage. Roger. Get the sacrificial lemonade!",
              'responses': []}
        ],
        [
            { 'text': "Ah. Perfect. Wait, is that cinnamon I smell?",
              'responses': [(1, "That's important?")]},
            { 'text': "Our saviour detests cinnamon! But.. We need to continue!",
              'responses': [(2, "Right.")]},
            { 'text': "To the next stage. Roger. Get the sacrificial lemonade!",
              'responses': []},
        ],
    ),

]


class FinalCutscene:
    is_complete = False

    def __init__(self, npc_sprites, pickups, game_state):
        self.npc_sprites = npc_sprites
        self.pickups = pickups
        self.game_state = game_state

        self.dialogue = END_DIALOGUE
        self.current_conversation = None
        self.state = 0


        self.sacrifices = [
            NpcSacrifice((2410, 1100), (2765, 1300)),
            NpcSacrifice((2420, 1110), (2865, 1400)),
            NpcSacrifice((2410, 1120), (2815, 1500)),
            NpcSacrifice((2420, 1130), (2715, 1500)),
            NpcSacrifice((2410, 1140), (2665, 1400)),
            NpcSacrifice((2420, 1150), (2765, 1400))
        ]

        self.rogers = None
        self.setup_state()

    def reset_rogers(self, x_offset=0):
        self.rogers = [
            NpcSacrifice((2410, 1100), (2765 + x_offset, 1300)),
            NpcSacrifice((2765 + x_offset, 1300), (2865 + x_offset, 1400)),
            NpcSacrifice((2865 + x_offset, 1400), (2815 + x_offset, 1500)),
            NpcSacrifice((2815 + x_offset, 1500), (2715 + x_offset, 1500)),
            NpcSacrifice((2715 + x_offset, 1500), (2665 + x_offset, 1400)),
            NpcSacrifice((2665 + x_offset, 1400), (2765 + x_offset, 1400)),
            NpcSacrifice((2765 + x_offset, 1400), (2765 + x_offset, 1100))
        ]

    def draw(self, surface):
        if self.current_conversation:
            d = Dialogue()
            d.set_data(
                "Cult Leader",
                self.current_conversation.current['text'],
                self.current_conversation.current['responses']
            )
            d.draw(surface)

    def update(self, viewport):
        if self.state == 1:
            if all([npc.at_end_location() for npc in self.sacrifices]):
                self.state += 1
                self.setup_state()

        if self.state == 3:
            if self.rogers[0].at_end_location():
                self.pickups.add(BlackCandles(self.rogers[0].x, self.rogers[0].y))
                self.npc_sprites.remove(self.rogers.pop(0))
                if self.rogers:
                    if self.game_state.is_day_sabotaged(CANDLE_DAY):
                        self.sacrifices[6-len(self.rogers)].draw_text_in("Mmm. Cinnamon!", seconds=1)
                    else:
                        self.sacrifices[6-len(self.rogers)].draw_text_in("Smells bland. Lame.", seconds=1)
                    self.npc_sprites.add(self.rogers[0])
                else:
                    self.state += 1
                    self.setup_state()

        if self.state == 5:
            if self.rogers[0].at_end_location():
                self.npc_sprites.remove(self.rogers.pop(0))
                if self.rogers:
                    if self.game_state.is_day_sabotaged(LEMONADE_DAY):
                        self.sacrifices[6-len(self.rogers)].draw_text_in("Looks delicious!", seconds=1)
                    else:
                        self.sacrifices[6-len(self.rogers)].draw_text_in("Looks horrible!", seconds=1)
                    self.npc_sprites.add(self.rogers[0])
                else:
                    self.state += 1
                    self.setup_state()

    def key_press(self, key):
        if key == K_QUIT_INTERACTION:
            if self.current_conversation:
                self.current_conversation = None
                self.state += 1
                self.setup_state()
        elif self.current_conversation:
            self.current_conversation.progress(key)

    def setup_state(self):
        if self.state == 0:
            self.current_conversation = ConversationTree(
                npc_name="Cult Leader",
                conversation_data=self.dialogue.pop(0))

        elif self.state == 1:
            self.npc_sprites.add(self.sacrifices)
            self.current_conversation = None

        elif self.state == 2:
            dialogue = self.dialogue.pop(0)
            if self.game_state.is_day_sabotaged(ROBE_DAY):
                self.current_conversation = ConversationTree(
                    npc_name="Cult Leader",
                    conversation_data=dialogue.sabotaged)
            else:
                self.current_conversation = ConversationTree(
                    npc_name="Cult Leader",
                    conversation_data=dialogue.completed)

        elif self.state == 3:
            self.reset_rogers(x_offset=20)
            self.npc_sprites.add(self.rogers[0])

        elif self.state == 4:
            dialogue = self.dialogue.pop(0)
            if self.game_state.is_day_sabotaged(CANDLE_DAY):
                self.current_conversation = ConversationTree(
                    npc_name="Cult Leader",
                    conversation_data=dialogue.sabotaged)
            else:
                self.current_conversation = ConversationTree(
                    npc_name="Cult Leader",
                    conversation_data=dialogue.completed)

        elif self.state == 5:
            self.reset_rogers(x_offset=0)
            self.npc_sprites.add(self.rogers[0])

        elif self.state == 6:
            pass
