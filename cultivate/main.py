#!/usr/bin/env python3
import pygame
import sys

from cultivate.settings import WIDTH, HEIGHT
from cultivate.map import Map
from cultivate.player import Player
from cultivate.npc import Npc

def main():
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
        for event in pygame.event.get():
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                    or (event.type == pygame.QUIT)):
                sys.exit(0)

        game_map.update_map_view(pygame.key.get_pressed())
        npc.update()

        game_map.draw(screen)
        player.draw(screen)
        npc.draw(screen, game_map.get_viewport())

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
