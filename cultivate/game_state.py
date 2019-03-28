from cultivate.npc import Susan
from cultivate.tasks import task_conversations
from cultivate.transition import Fader

from cultivate.sprites.pickups import (
    Lemon, EmptyBucket, Sugar,
    Soap, RedSock, DirtyRobes, Shovel
)

from pygame.sprite import Group


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
        if self.fader.fading:
            return
        self.day += 1
        if self.tasks_todo:
            self.current_task = self.tasks_todo[0]
            self.tasks_todo = self.tasks_todo[1:]
        self.fader.start()

    def get_day_items(self):
        npc_sprites = Group()
        pickups = Group()

        if self.day == 1:
            pickups = Group([
                Shovel(1000, 1000),
            ])

        if self.day == 2:
            npc_sprites = Group(Susan())
            pickups = Group([
                Lemon(750, 750),
                EmptyBucket(1000, 1000),
                Sugar(1500, 1000)
            ])

        if self.day == 3:
            pickups = Group([
                Soap(2000, 900),
                RedSock(1750, 1500),
                DirtyRobes(1400, 1150)
            ])

        return (npc_sprites, pickups)
