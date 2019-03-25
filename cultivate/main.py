#!/usr/bin/env python3
import contextlib
import logging
import sys

from cultivate import settings
from cultivate.loader import get_music
from cultivate.map import Map
from cultivate.npc import Npc
from cultivate.pickups import Lemon
from cultivate.player import Player
from cultivate.settings import FPS, HEIGHT, SM_FONT, WIDTH

with contextlib.redirect_stdout(None):
    import pygame
    from pygame.sprite import Group, spritecollide


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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.mixer.init()
    bgm = get_music("beeball.ogg")
    bgm.play(-1)

    # init objects
    player = Player(WIDTH // 2, HEIGHT // 2)
    game_map = Map()
    npc = Npc([(1000, 1000), (1000, 1200), (1200, 1200), (1200, 1000)])

    pickups = Group(Lemon(WIDTH // 2 + 50, HEIGHT // 2 + 50))

    # main game loop
    while True:
        # check for user exit, ignore all other events
        logging.debug("Check for events")
        for event in pygame.event.get():
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                    or (event.type == pygame.QUIT)):
                sys.exit(0)

        logging.debug("Update object positions")
        game_map.update_map_view(pygame.key.get_pressed())
        npc.update()
        pickups.update(game_map.get_viewport())
        player.update()
        picked_up = spritecollide(player, pickups, True)
        if picked_up:
            player.pickup = picked_up.pop()

        # draw objects at their updated positions
        logging.debug("Draw to buffer")
        game_map.draw(screen)
        pickups.draw(screen)
        player.draw(screen)
        npc.draw(screen, game_map.get_viewport())

        # display FPS
        if settings.DEBUG:
            fps_str = f"FPS: {clock.get_fps():.2f}"
            fps_surface = SM_FONT.render(fps_str, True, pygame.Color("black"))
            screen.blit(fps_surface, (50, 50))

        # display new draws
        logging.debug("Display buffer")
        pygame.display.flip()

        logging.debug("Wait for next frame")
        clock.tick(FPS)


if __name__ == "__main__":
    main()
