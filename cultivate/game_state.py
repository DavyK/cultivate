from collections import namedtuple
from cultivate.npc import Susan, NpcFollower, NpcQuester
from cultivate.tasks import task_conversations
from cultivate.transition import Fader
from cultivate.settings import WIDTH, HEIGHT

from cultivate.sprites.pickups import (
    Lemon, EmptyBucket, Sugar,
    Soap, RedSock, DirtyRobes, Shovel, Flower
)

from pygame.sprite import Group

TaskStatus = namedtuple('TaskStatus', 'completed sabotaged')

class GameState:
    def __init__(self, day=0):
        self.day = day
        tasks_todo = list(task_conversations.keys())
        self.current_task = tasks_todo[day]
        self.tasks_todo = tasks_todo[day+1:]
        self.task_status = [TaskStatus(None, None)] * 6
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
            print("Quester")
            npc_sprites = Group([NpcQuester()])
            pickups = Group([
                Shovel(1000, 1000),
                Flower(1750, 750),
            ])

        if self.day == 2:
            npc_sprites = Group([Susan(), NpcQuester()])
            pickups = Group([
                Lemon(750, 750),
                EmptyBucket(1000, 1000),
                Sugar(1500, 1000)
            ])

        if self.day == 3:
            npc_sprites = Group([NpcQuester()])
            pickups = Group([
                EmptyBucket(1000, 1000),
                Soap(2000, 900),
                RedSock(1750, 1500),
                DirtyRobes(1400, 1150)
            ])

        return (npc_sprites, pickups)

    def is_day_done(self):
        return self.task_status[self.day].completed or self.task_status[self.day].sabotaged

    def complete_task(self):
        self.task_status[self.day] = TaskStatus(True, self.task_status[self.day].sabotaged)

    @property
    def tasks_completed(self):
        return sum([status.completed and not status.sabotaged for status in self.task_status])

    def sabotage_task(self):
        self.task_status[self.day] = TaskStatus(self.task_status[self.day].completed, True)

    @property
    def tasks_sabotaged(self):
        return sum([status.sabotaged for status in self.task_status])
