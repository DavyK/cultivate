#!/usr/bin/env python3
import contextlib
import logging
import sys

from itertools import chain

# don't print pygame welcome
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.sprite import Group

from cultivate import settings
from cultivate.loader import get_music
from cultivate.map import Map
from cultivate.npc import Susan
from cultivate.game_state import GameState
from cultivate.sprites.pickups import BasePickUp
from cultivate.player import Player
from cultivate.tooltip import Tooltip, InventoryBox, InfoBox

K_INTERACT = pygame.K_x
K_QUIT_INTERACTION = pygame.K_q


def main(argv=sys.argv[1:]):
    # configure logging
    logging_config = {"level": logging.INFO,
                      "format": "%(levelname)-8s %(asctime)15s [%(filename)s@%(lineno)-3s] %(message)s"}
    # check for debug parameter
    if "--debug" in argv:
        settings.DEBUG = True
        logging_config["level"] = logging.DEBUG
    logging.basicConfig(**logging_config)

    # init pygame
    # stop sound effect delay (see https://stackoverflow.com/q/18273722)
    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(22050, -16, 2, 1024)
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    pygame.mixer.init()
    bgm = get_music("beeball.ogg")
    bgm.play(-1)

    # init objects
    game_state = GameState()
    player = Player(settings.WIDTH // 2, settings.HEIGHT // 2, game_state)
    game_map = Map(player)

    npc_sprites = Group()
    npc_sprites.add(Susan())

    current_day = game_state.day
    npc_sprites, pickups = game_state.get_day_items()

    static_interactables = Group()
    static_interactables.add(game_map.bed)
    static_interactables.add(game_map.river)
    static_interactables.add(game_map.desk)
    static_interactables.add(game_map.fire)
    static_interactables.add(game_map.grave)

    tooltip_bar = Tooltip()
    inventory = InventoryBox()
    info_box = InfoBox(game_state)

    # main game loop
    while True:
        # check for user exit, ignore all other events
        logging.debug("Check for events")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                # Dropped
                if event.key == pygame.K_z and player.pickup:
                    logging.debug("Dropping: ", player.pickup)
                    player.pickup.x = player.x + game_map.map_view_x
                    player.pickup.y = player.y + game_map.map_view_y
                    pickups.add(player.pickup)
                    player.pickup = None
                    inventory.clear_icon()
                # Interact - possibly pick up
                elif event.key == K_INTERACT:
                    picked_up = False
                    if not player.pickup:
                        boundary = player.tooltip_boundary(game_map.get_viewport())
                        for item in pickups:
                            if boundary.colliderect(item.rect):
                                logging.debug("Interacting with ", item)
                                # Found the item we're picking up
                                pickups.remove(item)
                                player.pickup = item
                                picked_up = True
                                inventory.set_icon(item)
                                break

                    if not picked_up and not player.interacting_with and \
                       not isinstance(player.nearby_interactable, BasePickUp):
                        logging.debug("Starting conversation with:", player.nearby_interactable)
                        player.start_interact()
                # stop interaction
                elif event.key == K_QUIT_INTERACTION:
                    player.stop_interact()
                # combine
                elif event.key == pygame.K_c and player.pickup:
                    logging.debug("Trying to combine on:", player.pickup)
                    boundary = player.tooltip_boundary(game_map.get_viewport())
                    for item in chain(pickups, static_interactables):
                        if boundary.colliderect(item.rect):
                            if player.pickup.combine(item):
                                # We can create a new item
                                new_item, reusable = player.pickup.combine(item)
                                new_item.x = item.x
                                new_item.y = item.y
                                logging.debug("Created:", new_item)
                                if item in static_interactables:
                                    # If it's static, use the players x/y
                                    new_item.x = player.x + game_map.map_view_x
                                    new_item.y = player.y + game_map.map_view_y
                                else:
                                    # If it isn't static, item should be deleted
                                    pickups.remove(item)

                                player.pickup = reusable
                                pickups.add(new_item)
                                inventory.set_icon(reusable)
                                # Break just incase we are in the vicinity of mutliple objects
                                break

                elif event.type == pygame.KEYDOWN:
                    player.key_press(event.key)

        if game_state.day != current_day and game_state.fader.black:
            (npc_sprites, pickups) = game_state.get_day_items()
            current_day = game_state.day

        logging.debug("Update object positions")

        game_map.update_map_view(pygame.key.get_pressed())

        npc_sprites.update(game_map.get_viewport())
        pickups.update(game_map.get_viewport())
        static_interactables.update(game_map.get_viewport())
        player.update()
        player.set_nearby(None)

        interactions = []
        tooltip_bar.clear_tooltip()
        for item in chain(npc_sprites, static_interactables, pickups):
            tooltip_rect = player.tooltip_boundary(game_map.get_viewport())
            if tooltip_rect.colliderect(item.rect):
                if player.pickup and player.pickup.can_combine(item):
                    tooltip_bar.set_tooltip("Press c to combine")
                else:
                    if isinstance(item, BasePickUp) and player.pickup:
                        pass
                    elif item.help_text:
                        tooltip_bar.set_tooltip(f"press x to {item.help_text}")

                player.set_nearby(item)
                break
        if player.pickup and tooltip_bar.empty:
            tooltip_bar.set_tooltip("press z to drop")

        # draw objects at their updated positions
        logging.debug("Draw to buffer")
        game_map.draw(screen)
        pickups.draw(screen)
        for npc in npc_sprites:
            npc.draw(screen)
        # draw building roofs
        for building in game_map.buildings.values():
            building.draw(screen, game_map.get_viewport())
        player.draw(screen, pygame.key.get_pressed())
        if not player.conversation:
            tooltip_bar.draw(screen)

        inventory.draw(screen)
        info_box.draw(screen)

        # display FPS
        if settings.DEBUG:
            fps_str = f"FPS: {clock.get_fps():.2f}"
            fps_surface = settings.SM_FONT.render(fps_str, True, pygame.Color("black"))
            screen.blit(fps_surface, (50, 50))

        if game_state.fader.fading:
            game_state.fader.draw(screen)

        # display new draws
        logging.debug("Display buffer")
        pygame.display.flip()

        logging.debug("Wait for next frame")
        clock.tick(settings.FPS)


if __name__ == "__main__":
    main()
