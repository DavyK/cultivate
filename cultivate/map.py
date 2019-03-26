import random

import pygame

from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings.test_building import TestBuilding
from cultivate.sprites.river import River
from cultivate.player import Player
from cultivate.loader import get_grass, get_weed, get_forest, get_sound
from cultivate.settings import HEIGHT, MAP_HEIGHT, MAP_WIDTH, WIDTH
from cultivate import settings


class Map:
    def __init__(self, player: Player):
        self.player = player
        self.image = self.compose_image()
        self.map_view_x = WIDTH
        self.map_view_y = HEIGHT
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        # TODO: Get the forest and bridge areas better
        top_forest = UpdatableSprite(pygame.Rect(0, 0, MAP_WIDTH, HEIGHT//2))
        left_forest = UpdatableSprite(pygame.Rect(0, 0, WIDTH//2, MAP_HEIGHT))
        right_forest = UpdatableSprite(pygame.Rect(MAP_WIDTH - WIDTH//2, 0, WIDTH//2, MAP_HEIGHT))
        bottom_forest = UpdatableSprite(pygame.Rect(0, MAP_HEIGHT - HEIGHT//2, MAP_WIDTH, MAP_HEIGHT//2))
        bridge1 = UpdatableSprite(pygame.Rect((MAP_WIDTH // 2), (MAP_HEIGHT * 2 // 3), 64, 64))
        self.move_amount = 10
        self.moved_last_tick = False
        self.footstep = get_sound("footstep-medium.ogg")
        self.footstep.set_volume(0.4)
        self.river = River(self.image)
        self.impassables = pygame.sprite.Group(top_forest, left_forest, right_forest, bottom_forest, self.river)
        self.passables = pygame.sprite.Group(bridge1)
        self.buildings = {"test building": TestBuilding(self.image)}

    def compose_image(self) -> pygame.Surface:
        image = get_grass(MAP_WIDTH, MAP_HEIGHT)
        self.generate_random_weeds(image)
        self.generate_border_forest(image)
        return image

    @staticmethod
    def generate_random_weeds(surface: pygame.Surface, count=100):
        """Randomly blit weeds onto {surface}."""
        weed = get_weed()
        locations = [(random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT)) for _ in range(count)]
        for x, y in locations:
            surface.blit(weed, (x, y))

    @staticmethod
    def generate_border_forest(surface: pygame.Surface):
        surface.blit(get_forest(MAP_WIDTH, MAP_HEIGHT), (0, 0))

    def update_map_view(self, key_pressed):
        if self.player.conversation:
            self.moved_last_tick = False
            return

        self.passables.update(self.get_viewport())
        self.impassables.update(self.get_viewport())

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

    def get_viewport(self):
        return pygame.Rect(self.map_view_x, self.map_view_y,
                           WIDTH, HEIGHT)

    def can_move(self, dx: int, dy: int) -> bool:
        """Check if the player can move by {dx}, {dy}.

        :return True if the player would hit a {self.passable} OR would not hit a {self.impassable}.
        """
        # the ghost of a player moves ahead of them to check collision
        ghost = pygame.sprite.Sprite()
        ghost.rect = pygame.Rect(self.player.x + dx, self.player.y + dy,
                                 self.player.rect.w, self.player.rect.h)
        return pygame.sprite.spritecollide(ghost, self.passables, False) or not pygame.sprite.spritecollide(ghost, self.impassables, False)

    def draw(self, surface: pygame.Surface):
        """Draw the viewable area of the map to the surface."""
        surface.blit(self.image, (0, 0), area=(self.map_view_x, self.map_view_y,
                                               self.map_view_x+WIDTH, self.map_view_y+HEIGHT))
        if settings.DEBUG:
            # draw collision boxes
            self.impassables.draw(surface)
            self.passables.draw(surface)

        for building in self.buildings.values():
            # draw building roofs
            building.draw(surface, self.get_viewport())
