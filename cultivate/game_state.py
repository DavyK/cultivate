
from collections import namedtuple
from cultivate.npc import Susan, NpcFollower, NpcQuester, Pentagram
from cultivate.tasks import task_conversations
from cultivate.transition import Fader
from cultivate.settings import WIDTH, HEIGHT
from cultivate.sprites.grave import Grave
from cultivate.sprites.desk import Desk
from cultivate.sprites import pickups as pickupables

from pygame.sprite import Group

TaskStatus = namedtuple('TaskStatus', 'completed sabotaged')

class GameState:
    def __init__(self, day=0):
        self.day = day
        tasks_todo = list(task_conversations.keys())
        self.current_task = tasks_todo[day]
        self.tasks_todo = tasks_todo[day+1:]
        self.task_status = [TaskStatus(False, False)] * 6
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
            # show the newcomers around
            npc_sprites = Group([
                NpcFollower(WIDTH * 3/2-50, HEIGHT *3/2-50),
                NpcFollower(WIDTH * 3/2-70, HEIGHT *3/2-70),
                NpcFollower(WIDTH * 3/2-55, HEIGHT *3/2-100),
                NpcFollower(WIDTH * 3/2-100, HEIGHT *3/2-60),
                NpcFollower(WIDTH * 3/2+25, HEIGHT *3/2+55),
                NpcFollower(WIDTH * 3/2+50, HEIGHT *3/2+100)
            ])

        if self.day == 1:
            # dig the grave
            npc_sprites = Group([NpcQuester()])
            pickups = Group([
                pickupables.Shovel(1770, 480),
                *[pickupables.Flower(3000 + (i * 100), 700) for i in range(6)],
            ])

        if self.day == 2:
            # make lemonade
            npc_sprites = Group([Susan(), NpcQuester()])
            pickups = Group([
                pickupables.Lemon(1860, 1650),
                pickupables.EmptyBucket(2000, 590),
                pickupables.Sugar(1850, 1555),
                pickupables.RatPoison(1922, 1545),
            ])

        if self.day == 3:
            # do laundry
            npc_sprites = Group([NpcQuester()])
            pickups = Group([
                pickupables.EmptyBucket(2000, 590),
                pickupables.Soap(2000, 525),
                pickupables.RedSock(1900, 500),
                pickupables.DirtyRobes(1900, 500),
            ])

        if self.day == 4:
            # make candles
            npc_sprites = Group([NpcQuester()])
            pickups = Group([
                pickupables.EmptyBucket(2000, 590),
                pickupables.BeesWax(1890, 510),
                pickupables.BlackDye(1930, 515),
                pickupables.EssenceOfCinnamon(1970, 510),
            ])

        if self.day == 5:
            # edit prayer sheet
            npc_sprites = Group([NpcQuester()])

        if self.day == 6:
            # summoning ritual
            npc_sprites = Group([Pentagram()])

        return npc_sprites, pickups

    def is_day_done(self):
        return self.task_status[self.day].completed or self.task_status[self.day].sabotaged

    def update_task_status(self, pickups, static_interactables):
        if self.day == 0:
            pass
        elif self.day == 1:
            for item in static_interactables:
                if isinstance(item, Grave):
                    if item.dug:
                        self.complete_task()
                    if item.planted:
                        self.sabotage_task()

        elif self.day == 2:
            has_lemonade = False
            has_empty_ratpoison = False
            for item in pickups:
                if isinstance(item, pickupables.Lemonade):
                    has_lemonade = True
                elif isinstance(item, pickupables.EmptyBottle):
                    has_empty_ratpoison = True
            if has_lemonade:
                self.complete_task()
            elif has_lemonade and has_empty_ratpoison:
                self.sabotage_task()

        elif self.day == 3:
            for item in pickups:
                if isinstance(item, pickupables.WhiteRobes):
                    self.complete_task()
                elif isinstance(item, pickupables.PinkRobes):
                    self.sabotage_task()

        elif self.day == 4:
            for item in pickups:
                if isinstance(item, pickupables.BlackCandles):
                    self.complete_task()
                elif isinstance(item, pickupables.ScentedBlackCandles):
                    self.sabotage_task()

        elif self.day == 5:
            for item in static_interactables:
                if isinstance(item, Desk):
                    madlibs = item.madlibs
                    if madlibs.edited and madlibs.correct:
                        self.complete_task()
                    elif madlibs.edited and not madlibs.correct:
                        self.sabotage_task()

        # print(self.tasks_completed, self.tasks_sabotaged)

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
