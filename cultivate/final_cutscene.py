import pygame

from cultivate.conversation_tree import ConversationTree
from cultivate.dialogue import Dialogue
from cultivate.npc import NpcSacrifice

K_QUIT_INTERACTION = pygame.K_q


END_DIALOGUE = [
    [
        { 'text': "Ah, You're here. Now we can begin the ceremony",
          'responses': [(1, "What is it?")]},
        { 'text': "You've been here for years. It's the time where we summon our saviour, of course",
          'responses': [(2, "That sounds dubious")]},
        { 'text': "Well let's get on with it. Sacrifices, come forth!",
          'responses': []}
    ],
    [
        { 'text': "See, look at their beautiful pristine pure white robes. Excellent",
          'responses': [(1, "That's important?")]},
        { 'text': "Of course! Our saviour can't have an off white sacrifice!",
          'responses': [(2, "Right.")]},
        { 'text': "To the next stage. Roger. Get the candles!",
          'responses': []}
    ],

]


class FinalCutscene:
    is_complete = False

    def __init__(self, npc_sprites):
        self.npc_sprites = npc_sprites

        self.dialogue = END_DIALOGUE
        self.current_conversation = None
        self.state = 0
        self.setup_state()


        self.sacrifices = [
            NpcSacrifice([(2410, 1100), (2765, 1300), (2765, 1300)]),
            NpcSacrifice([(2420, 1110), (2865, 1400), (2865, 1400)]),
            NpcSacrifice([(2410, 1120), (2815, 1500), (2815, 1500)]),
            NpcSacrifice([(2420, 1130), (2715, 1500), (2715, 1500)]),
            NpcSacrifice([(2410, 1140), (2665, 1400), (2665, 1400)]),
            NpcSacrifice([(2420, 1150), (2765, 1400), (2765, 1400)])
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
            print([npc.at_end_location() for npc in self.sacrifices])
            if all([npc.at_end_location() for npc in self.sacrifices]):
                self.state += 1
                self.setup_state()

    def key_press(self, key):
        if key == K_QUIT_INTERACTION:
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
            self.current_conversation = ConversationTree(
                npc_name="Cult Leader",
                conversation_data=self.dialogue.pop(0))
