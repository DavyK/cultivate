#!/usr/bin/env python3
import contextlib
import sys

from cultivate.map import Map
from cultivate.npc import Npc
from cultivate.player import Player
from cultivate import settings
from cultivate.settings import FPS, HEIGHT, WIDTH, SM_FONT

with contextlib.redirect_stdout(None):
    import pygame


def main(argv=sys.argv[1:]):
    # check for debug parameter
    if "--debug" in argv:
        settings.DEBUG = True

    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # init objects
    player = Player(WIDTH // 2, HEIGHT // 2)
    game_map = Map()
    npc = Npc([(1000, 1000), (1000, 1200), (1200, 1200), (1200, 1000)])

    # main game loop
    while True:
        # check for user exit, ignore all other events
        for event in pygame.event.get():
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                    or (event.type == pygame.QUIT)):
                sys.exit(0)

        # update object positions
        game_map.update_map_view(pygame.key.get_pressed())
        npc.update()

        # draw objects at their updated positions
        game_map.draw(screen)
        player.draw(screen)
        npc.draw(screen, game_map.get_viewport())

        # display FPS
        if settings.DEBUG:
            fps_str = f"FPS: {clock.get_fps():.2f}"
            fps_surface = SM_FONT.render(fps_str, True, pygame.Color("black"))
            screen.blit(fps_surface, (50, 50))

        # display new draws
        pygame.display.flip()

        # wait for next frame
        clock.tick(FPS)


if __name__ == "__main__":
    main()
