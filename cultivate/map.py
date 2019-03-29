import collections
import random

import pygame

from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings.test_building import TestBuilding
from cultivate.sprites.buildings.toolshed import ToolShed
from cultivate.sprites.buildings.church import Church
from cultivate.sprites.buildings.library import Library
from cultivate.sprites.river import River
from cultivate.sprites.bed import Bed
from cultivate.sprites.desk import Desk
from cultivate.sprites.grave import Grave
from cultivate.madlibs import Madlibs
from cultivate.sprites.fire import Fire
from cultivate.player import Player
from cultivate.loader import get_garden, get_dirt, get_grass, get_weed, get_forest, get_sound, get_grave
from cultivate.loader import get_gravestone1, get_gravestone2, get_gravestone3, get_gravestone4, get_gravestone5
from cultivate.settings import HEIGHT, MAP_HEIGHT, MAP_WIDTH, WIDTH
from cultivate import settings
from cultivate.tasks import task_conversations


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

    def next_day(self):
        self.day += 1
        if self.tasks_todo:
            self.current_task = self.tasks_todo[0]
            self.tasks_todo = self.tasks_todo[1:]


class Map:
    def __init__(self, player: Player):
        self.player = player

        # I don't like this. - Davy
        self.player.map = self

        self.image = self.compose_image()
        self.map_view_x = WIDTH
        self.map_view_y = HEIGHT
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.move_amount = 10
        self.moved_last_tick = False
        self.footstep = get_sound("footstep-medium.ogg")
        self.footstep.set_volume(0.4)

        # create permanent sprites
        # TODO: Make the forest border out of proper sprites (that own blitting themselves onto the map)
        top_forest = UpdatableSprite(pygame.Rect(0, 0, MAP_WIDTH, HEIGHT//2))
        left_forest = UpdatableSprite(pygame.Rect(0, 0, WIDTH//2, MAP_HEIGHT))
        right_forest = UpdatableSprite(pygame.Rect(MAP_WIDTH - WIDTH//2, 0, WIDTH//2, MAP_HEIGHT))
        bottom_forest = UpdatableSprite(pygame.Rect(0, MAP_HEIGHT - HEIGHT//2, MAP_WIDTH, MAP_HEIGHT//2))
        self.river = River(self.image)
        self.fire = Fire(800, 800)
        self.buildings = {
            "test building": TestBuilding(800, 1200, self.image),
            # "church": Church(self.image),
            "toolshed": ToolShed(1300, 1000, self.image),
            # "library": Library(self.image)
            }

        self.bed = Bed(900, 900, self.image)
        self.desk = Desk(800, 600, self.image, self.make_madlibs())
        self.grave = Grave(1000, 900)
        # create collision groups
        self.impassables = pygame.sprite.Group(
            top_forest, left_forest, right_forest, bottom_forest,
            self.river, self.bed, self.fire, self.desk, self.grave
        )
        self.passables = pygame.sprite.Group(self.river.bridges)
        for building in self.buildings.values():
            self.impassables.add(building.impassables)
            self.passables.add(building.passables)

    def compose_image(self) -> pygame.Surface:
        image = get_grass(MAP_WIDTH, MAP_HEIGHT)
        self.generate_random_weeds(image)
        self.generate_border_forest(image)
        self.generate_garden(image)
        self.generate_dirt(image)
        return image

    @staticmethod
    def make_madlibs():
        return Madlibs(
            "Dear {your_name},\n"
            "\n"
            "Have you seen {missing_person} anywhere? No one has seen him since {day}.\n"
            "\n"
            "Thanks, K Byeeeeeee!\n"
            "Uncle {uncle_name}\n"
            "\n"
            "P.S. Have you found the {object} yet?",
            collections.OrderedDict([
                ("your_name", "Steve"),
                ("missing_person", "Greg"),
                ("day", "yesterday"),
                ("uncle_name", "Davy"),
                ("object", "lemon")
            ])
        )

    @staticmethod
    def generate_random_weeds(surface: pygame.Surface, count=100):
        """Randomly blit weeds onto {surface}."""
        weed = get_weed()
        locations = [(random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT)) for _ in range(count)]
        for x, y in locations:
            surface.blit(weed, (x, y))

    @staticmethod
    def generate_dirt(surface: pygame.Surface):
        surface.blit(get_dirt(600, 600), (3000, 800))
        graves = [
            get_gravestone1(),
            get_gravestone2(),
            get_gravestone3(),
            get_gravestone5()
            ]
        for i in range(30, 560, 70):
            surface.blit(random.choice(graves), (3000+i, 820))
            surface.blit(random.choice(graves), (3020+i, 860))

    @staticmethod
    def generate_border_forest(surface: pygame.Surface):
        surface.blit(get_forest(MAP_WIDTH, MAP_HEIGHT), (0, 0))

    @staticmethod
    def generate_garden(surface: pygame.Surface):
        surface.blit(get_garden(500, 500), (1100, 400))

    def update_map_view(self, key_pressed):
        if self.player.interacting_with:
            self.moved_last_tick = False
            return

        moved = True
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            if self.can_move(0, self.move_amount):
                self.map_view_y += self.move_amount
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            if self.can_move(0, -self.move_amount):
                self.map_view_y -= self.move_amount
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            if self.can_move(self.move_amount, 0):
                self.map_view_x += self.move_amount
        elif key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            if self.can_move(-self.move_amount, 0):
                self.map_view_x -= self.move_amount
        else:
            moved = False

        if not self.moved_last_tick and moved:
            # started moving
            self.footstep.play(-1)
        if self.moved_last_tick and not moved:
            # stopped moving
            self.footstep.stop()

        self.moved_last_tick = moved

        # update other sprites
        if moved:
            for building in self.buildings.values():
                building.update(self.get_viewport())
            self.passables.update(self.get_viewport())
            self.impassables.update(self.get_viewport())

    def get_viewport(self):
        return pygame.Rect(self.map_view_x, self.map_view_y,
                           WIDTH, HEIGHT)

    def can_move(self, dx: int, dy: int) -> bool:
        """Check if the player can move by {dx}, {dy}.

        :return True if the player would hit a {self.passable} OR would not hit a {self.impassable}.
        """
        # the ghost of a player moves ahead of them to check collision
        ghost = pygame.sprite.Sprite()
        # collision {ghost.rect} covers is player's feet
        ghost.rect = pygame.Rect(self.player.rect.x + dx, self.player.rect.bottom + dy,
                                 self.player.rect.w, 1)
        return pygame.sprite.spritecollide(ghost, self.passables, False) or not pygame.sprite.spritecollide(ghost, self.impassables, False)

    def draw(self, surface: pygame.Surface):
        """Draw the viewable area of the map to the surface."""
        surface.blit(self.image, (0, 0), area=(self.map_view_x, self.map_view_y,
                                               self.map_view_x+WIDTH, self.map_view_y+HEIGHT))
        if settings.DEBUG:
            self.impassables.draw(surface)
            self.passables.draw(surface)

        self.fire.draw(surface)
        self.grave.draw(surface)
