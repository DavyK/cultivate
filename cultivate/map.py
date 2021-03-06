import collections
import random

import pygame

from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings.toolshed import ToolShed
from cultivate.sprites.buildings.church import Church
from cultivate.sprites.buildings.library import Library
from cultivate.sprites.buildings.kitchen import Kitchen
from cultivate.sprites.buildings.dorm import HorizontalDorm, VerticalDorm
from cultivate.sprites.buildings.stores import Stores
from cultivate.sprites.river import River
from cultivate.sprites.bed import Bed
from cultivate.sprites.desk import Desk
from cultivate.sprites.grave import Grave
from cultivate.sprites.clothes_line import ClothesLine
from cultivate.madlibs import Madlibs
from cultivate.sprites.fire import Fire, DemonFire
from cultivate.sprites.demon import Demon
from cultivate.player import Player
from cultivate.loader import get_pentagram, get_garden, get_dirt, get_grass, get_weed, get_forest, get_sound, get_grave
from cultivate.loader import get_plant1, get_plant2, get_plant3, get_plant4, get_plant5, get_plant6, get_plant7
from cultivate.loader import get_gravestone1, get_gravestone2, get_gravestone3, get_gravestone4, get_gravestone5
from cultivate.settings import HEIGHT, MAP_HEIGHT, MAP_WIDTH, WIDTH
from cultivate import settings
from cultivate.game_state import GameState

from cultivate.conversation_tree import ConversationTree
from cultivate.tasks import day_0_conversations


class Map:
    def __init__(self, player: Player, game_state: GameState):
        self.player = player

        # I don't like this. - Davy
        self.player.map = self

        self.game_state = game_state
        self.image = self.compose_image()
        self.map_view_x = WIDTH
        self.map_view_y = HEIGHT
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.move_amount = 10
        self.moved_last_tick = False
        self.footstep = get_sound("footstep-medium.ogg")
        self.footstep.set_volume(0.2)

        # create permanent sprites
        # TODO: Make the forest border out of proper sprites (that own blitting themselves onto the map)
        top_forest = UpdatableSprite(pygame.Rect(0, 0, MAP_WIDTH, HEIGHT//2))
        left_forest = UpdatableSprite(pygame.Rect(0, 0, WIDTH//2, MAP_HEIGHT))
        right_forest = UpdatableSprite(pygame.Rect(MAP_WIDTH - WIDTH//2, 0, WIDTH//2, MAP_HEIGHT))
        bottom_forest = UpdatableSprite(pygame.Rect(0, MAP_HEIGHT - HEIGHT//2, MAP_WIDTH, MAP_HEIGHT//2))
        self.river = River(self.image)
        self.fire = Fire(1700, 1650)
        self.buildings = {
            "toolshed": ToolShed(1650, 450, self.image),
            "library": Library(2500, 450, self.image),
            "kitchen": Kitchen(1800, 1500, self.image),
            "dorm1": HorizontalDorm(750, 1600, self.image),
            "dorm2": VerticalDorm(1250, 1600, self.image),
            "dorm3": HorizontalDorm(750, 2100, self.image),
            "dorm4": HorizontalDorm(1250, 2100, self.image),
            "stores": Stores(1875, 450, self.image),
            "church": Church(self.image)
        }

        self.bed = Bed(1340, 1650, self.image)
        self.desk = Desk(2500, 550, self.image, self.make_madlibs())
        self.graves = [
            Grave(3260, 1100, 0),
            Grave(3150, 900, 300),
            Grave(3390, 940, 40),
            Grave(3025, 1125, 20),
            Grave(3465, 1160, 340),
            Grave(3260, 1300, 270),
        ]
        self.clothes_line = ClothesLine(1950, 800)
        # how to make demon-y stuff appear
        # self.demon_fire = DemonFire(2000, 800)
        # self.demon = Demon(2000,800)

        # create collision groups
        self.impassables = pygame.sprite.Group(
            top_forest, left_forest, right_forest, bottom_forest,
            self.river, self.bed, self.fire, self.desk, *self.graves, self.clothes_line,
        )
        self.passables = pygame.sprite.Group(self.river.bridges)
        for building in self.buildings.values():
            self.impassables.add(building.impassables)
            self.passables.add(building.passables)

        self.day0 = [
            (None, 'welcome the newcomers'),
            ('kitchen', 'kitchen description'),
            ('toolshed', 'toolshed description'),
            ('library', 'library description'),
            ('church', 'church description'),
            (None, 'end day 0')
        ]

    def compose_image(self) -> pygame.Surface:
        image = get_grass(MAP_WIDTH, MAP_HEIGHT)
        self.generate_random_weeds(image)
        self.generate_border_forest(image)
        self.generate_garden(image)
        self.generate_dirt(image)
        return image

    @staticmethod
    def make_madlibs():
        replacements = collections.OrderedDict([
                ("verb1", "beeseech"),
                ("verb2", "bless"),
                ("adj1", "prood"),
                ("adj2", "church"),
                ("verb3", "follow"),
                ("noun1", "bath"),
                ("verb4", "pray"),
                ("verb5", "lif"),
                ("verb6", "dice"),
                ("verb7", "summon"),
                ("verb8", "come"),
            ])
        expected = collections.OrderedDict([
                ("verb1", "beseech"),
                ("verb2", "bless"),
                ("adj1", "proud"),
                ("adj2", "church"),
                ("verb3", "follow"),
                ("noun1", "path"),
                ("verb4", "pray"),
                ("verb5", "live"),
                ("verb6", "die"),
                ("verb7", "summon"),
                ("verb8", "come"),
            ])
        return Madlibs(
            "Lord of Light\n"
            "\n"
            "We {verb1} you to {verb2} these six new {adj1} members of our {adj2}\n"
            "\n"
            "We {verb3} the {noun1} that you have set out for us\n"
            "We {verb4} in your name\n"
            "We {verb5} in your name\n"
            "We {verb6} in your name\n"
            "We {verb7} you\n"
            "{verb8} before us\n",
            replacements,
            expected
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
        surface.blit(get_garden(500, 500), (550, 400))

        for i in range(50, 500, 60):
            surface.blit(get_plant1(), (1150+random.randint(0, 20), 400+i))
            surface.blit(get_plant2(), (1200+random.randint(0, 20), 400+i))
            surface.blit(get_plant3(), (1250+random.randint(0, 20), 400+i))
            surface.blit(get_plant4(), (1300+random.randint(0, 20), 400+i))
            surface.blit(get_plant5(), (1350+random.randint(0, 20), 400+i))
            surface.blit(get_plant6(), (1400+random.randint(0, 20), 400+i))
            surface.blit(get_plant7(), (1450+random.randint(0, 20), 400+i))

        for i in range(50, 500, 60):
            surface.blit(get_plant1(), (600+random.randint(0, 20), 400+i))
            surface.blit(get_plant2(), (650+random.randint(0, 20), 400+i))
            surface.blit(get_plant3(), (700+random.randint(0, 20), 400+i))
            surface.blit(get_plant4(), (750+random.randint(0, 20), 400+i))
            surface.blit(get_plant5(), (800+random.randint(0, 20), 400+i))
            surface.blit(get_plant6(), (850+random.randint(0, 20), 400+i))
            surface.blit(get_plant7(), (900+random.randint(0, 20), 400+i))

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

        if self.game_state.day == 0 and self.day0:
            # If there is no building associated, display the text
            if self.day0[0][0] is None:
                item, text = self.day0.pop(0)
                self.player.interacting_with = self
                self.player.nearby_interactable = self
                self.player.conversation = ConversationTree(
                    npc_name='You', conversation_data=day_0_conversations[text])
            else:
                # See which buildings we are colliding with
                for (building_name, building) in self.buildings.items():
                    if building.rect.colliderect(pygame.Rect(
                            WIDTH//2 - 50,
                            HEIGHT//2 - 50,
                            100,
                            100)) and building_name == self.day0[0][0]:
                        self.footstep.stop()
                        item, text = self.day0.pop(0)
                        self.player.interacting_with = self
                        self.player.nearby_interactable = self
                        self.player.conversation = ConversationTree(
                            npc_name='You', conversation_data=day_0_conversations[text])
                        break
            if not self.day0:
                self.game_state.complete_task()

        # update other sprites
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
        # self.demon_fire.draw(surface)
        # self.demon.draw(surface)
        for grave in self.graves:
            grave.draw(surface)
        self.clothes_line.draw(surface)
