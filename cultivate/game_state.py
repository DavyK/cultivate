from cultivate.npc import Susan, NpcFollower
from cultivate.tasks import task_conversations
from cultivate.transition import Fader
from cultivate.settings import WIDTH, HEIGHT

from cultivate.sprites.pickups import (
    BasePickUp, Lemon, EmptyBucket, Sugar,
    Soap, RedSock, DirtyRobes,
)

from pygame.sprite import Group, spritecollide

class GameState:
    def __init__(self):
        self.day = 0
        tasks_todo = list(task_conversations.keys())
        self.current_task = tasks_todo[0]
        self.tasks_todo = tasks_todo[1:]
        self.tasks_completed = []
        self.tasks_sabotaged = []
        self.tasks_ignored = []

        self.playthroughs = 0

        self.fader = Fader()



    def next_day(self):
        self.day += 1
        if self.tasks_todo:
            self.current_task = self.tasks_todo[0]
            self.tasks_todo = self.tasks_todo[1:]
        self.fader.start()

    def get_day_items(self):
        npc_sprites = Group()
        pickups = Group()

        if self.day == 0:
            npc_sprites = Group([
                NpcFollower(WIDTH * 3/2-50, HEIGHT *3/2-50),
                NpcFollower(WIDTH * 3/2-70, HEIGHT *3/2-70),
                NpcFollower(WIDTH * 3/2-55, HEIGHT *3/2-100),
                NpcFollower(WIDTH * 3/2-100, HEIGHT *3/2-60),
                NpcFollower(WIDTH * 3/2+25, HEIGHT *3/2+55),
                NpcFollower(WIDTH * 3/2+50, HEIGHT *3/2+100)
            ])

        if self.day == 1:
            npc_sprites = Group(Susan())
            pickups = Group([
                Lemon(750, 750),
                EmptyBucket(1000, 1000),
                Sugar(1500, 1000)
            ])

        if self.day == 2:
            pickups = Group([
                Soap(2000, 900),
                RedSock(1750, 1500),
                DirtyRobes(1400, 1150)
            ])

        return (npc_sprites, pickups)
