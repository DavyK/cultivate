from collections import namedtuple
import logging
import time

import pygame

from cultivate.conversation_tree import ConversationTree
from cultivate.dialogue import Dialogue
from cultivate.npc import NpcSacrifice, NpcPathAndStop
from cultivate.sprites.pickups import BlackCandles

from cultivate.sprites.demon import Demon
from cultivate.sprites.fire import DemonFire

K_QUIT_INTERACTION = pygame.K_q

GRAVE_DAY = 1
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
    TaskSpeech( # Robe comments to candles
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
    TaskSpeech( # Candles to lemonade
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
    TaskSpeech( # lemonade to madlib
        [
            { 'text': "Excellent. I can smell the poison from here. Hopefully the lemonade makes it taste a little better for them...",
              'responses': [(1, "Poison?!")]},
            { 'text': "Of course! How would we sacrifice them without it, silly! You made it!",
              'responses': [(2, "Erm.")]},
            { 'text': "To the next stage. Roger! Give us all the ritual sheets! The time is upon us!",
              'responses': []}
        ],
        [
            { 'text': "Funny. It doesn't smell much like the poison. I hope it works, or we will be in trouble!",
              'responses': [(1, "That's important?")]},
            { 'text': "Well if our sacrifices don't die, we can hardly call them sacrifices!",
              'responses': [(2, "Right.")]},
            { 'text': "To the next stage. Roger! Give us all the ritual sheets! The time is upon us!",
              'responses': []},
        ],
    ),
    TaskSpeech(  # madlib to grave
        [
            { 'text': "Excellent. Good job on those corrections. They're perfect! We can always count on you",
              'responses': [(1, "This wasn't what I thought it would be for..")]},
            { 'text': "Well what else do we read from except ritual sheets?",
              'responses': [(2, "Erm.")]},
            { 'text': "To the next stage. Everyone over your graves and prepare for the coming!",
              'responses': []}
        ],
        [
            { 'text': "That's not quite how I remember the summoning, But it will probably not cause any issues...",
              'responses': [(1, "That's important?")]},
            { 'text': "Well if the words are off we won't be able to bind or saviour to do our bidding, silly!",
              'responses': [(2, "Right.")]},
            { 'text': "To the next stage. Everyone over your graves and prepare for the coming!",
              'responses': []},
        ],
    ),
    TaskSpeech(  # grave to coming
        [
            { 'text': "Those graves look perfect! No contaminants. Our saviour will be content",
              'responses': [(1, "They were for graves?! I thought it was for .. Flowers?")]},
            { 'text': "I asked you to dig 6ft deep holes. And you thought they were for flowers?",
              'responses': [(2, "Erm.")]},
            { 'text': "Well that's it. Now the saviour should come forth.. Unless anything has been sabotaged...",
              'responses': []}
        ],
        [
            { 'text': "Are the flowers supposed to be there? I don't recall...",
              'responses': [(1, "That's important?")]},
            { 'text': "Well if anything is out of place..",
              'responses': [(2, "Right.")]},
            { 'text': "Well that's it. Now the saviour should come forth.. Unless anything has been sabotaged...",
              'responses': []},
        ],
    ),

]

def get_sacrifice_positions(x_offset=0):
    return [
        (3184 + x_offset, 930),
        (3427 + x_offset, 973),
        (3480 + x_offset, 1186),
        (3278 + x_offset, 1344),
        (3057 + x_offset, 1155),
        (3287 + x_offset, 1115)
    ]

START_POS = (3600, 800)
FIRE_POS = (2790, 625)

class FinalCutscene:
    is_complete = False

    def __init__(self, npc_sprites, pickups, game_state):
        self.npc_sprites = npc_sprites
        self.pickups = pickups
        self.game_state = game_state

        self.dialogue = END_DIALOGUE
        self.current_conversation = None
        self.state = 0

        self.demon_fire = None
        self.demon = None
        self.end_time = None

        sabotaged = game_state.is_day_sabotaged(ROBE_DAY)
        self.sacrifices = [
            NpcSacrifice(START_POS, pos, sabotaged) for pos in get_sacrifice_positions()
        ]

        self.rogers = None
        self.setup_state()

    def reset_rogers(self, x_offset=0):
        positions = [START_POS] + get_sacrifice_positions(x_offset=x_offset) + [START_POS]
        self.rogers = [NpcPathAndStop(start_pos, end_pos) for (start_pos, end_pos) in
                       zip(positions, positions[1:])]


    def draw(self, surface):
        if self.current_conversation:
            d = Dialogue()
            d.set_data(
                "Cult Leader",
                self.current_conversation.current['text'],
                self.current_conversation.current['responses']
            )
            d.draw(surface)
        if self.demon:
            surface.blit(self.demon.image, (0, 0))

    def update(self, viewport):
        if self.state == 1:
            if all([npc.at_end_location() for npc in self.sacrifices]):
                self.state += 1
                self.setup_state()

        elif self.state == 3:
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

        elif self.state == 5:
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

        elif self.state == 7:
            if self.rogers[0].at_end_location():
                self.npc_sprites.remove(self.rogers.pop(0))
                if self.rogers:
                    self.npc_sprites.add(self.rogers[0])
                else:
                    self.state += 1
                    self.setup_state()

        elif self.state == 8: # Read in turns
            if self.madlib_chunks:
                # Check previous person has finished
                if not self.sacrifices[self.reader-1].dialogue:
                    next_part = self.madlib_chunks.pop(0)
                    self.sacrifices[self.reader].draw_text_in(next_part, seconds=0)
                    self.reader = (self.reader + 1) % 6
            else:
                self.state += 1
                self.setup_state()

        elif self.state == 11:
            if time.time() > self.end_time:
                if self.game_state.tasks_sabotaged == 5:
                    raise RuntimeError("Sabotage complete")
                else:
                    raise RuntimeError("Demon summoned!")

    def key_press(self, key):
        if key == K_QUIT_INTERACTION:
            if self.current_conversation:
                self.current_conversation = None
                self.state += 1
                self.setup_state()
        elif self.current_conversation:
            self.current_conversation.progress(key)

    def do_dialogue(self, sabotage_day):
        conversation = self.dialogue.pop(0)
        if sabotage_day is None:
            self.current_conversation = ConversationTree(
                npc_name="Cult Leader",
                conversation_data=conversation)
        else:
            if self.game_state.is_day_sabotaged(sabotage_day):
                self.current_conversation = ConversationTree(
                    npc_name="Cult Leader",
                    conversation_data=conversation.sabotaged)
            else:
                self.current_conversation = ConversationTree(
                    npc_name="Cult Leader",
                    conversation_data=conversation.completed)

    def setup_state(self):
        if self.state == 0:
            self.do_dialogue(None)

        elif self.state == 1:  # Place sacrifices
            self.npc_sprites.add(self.sacrifices)
            self.current_conversation = None

        elif self.state == 2:
            self.do_dialogue(ROBE_DAY)

        elif self.state == 3:  # Place candles
            self.reset_rogers(x_offset=20)
            self.npc_sprites.add(self.rogers[0])

        elif self.state == 4:
            self.do_dialogue(CANDLE_DAY)

        elif self.state == 5: # Give lemonade
            self.reset_rogers(x_offset=0)
            self.npc_sprites.add(self.rogers[0])

        elif self.state == 6:
            self.do_dialogue(LEMONADE_DAY)

        elif self.state == 7:  # madlib give
            self.reset_rogers(x_offset=0)
            self.npc_sprites.add(self.rogers[0])

        elif self.state == 8:  # madlib read
            self.reader = 0
            self.madlib_chunks = [x for x in self.game_state.madlib_text.split('\n') if x]

        elif self.state == 9:
            self.do_dialogue(MADLIB_DAY)

        elif self.state == 10:
            self.do_dialogue(GRAVE_DAY)

        elif self.state == 11:
            if not self.game_state.tasks_sabotaged == 5:
                self.npc_sprites.add(DemonFire(*FIRE_POS))
            else:
                self.demon = Demon(0, 0)
            self.end_time = time.time() + 5
