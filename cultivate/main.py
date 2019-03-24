#!/usr/bin/env python3
import pygame
import sys

from cultivate.settings import WIDTH, HEIGHT
from cultivate.map import Map
from cultivate.player import Player


def main():
    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # init objects
    player = Player(WIDTH // 2, HEIGHT // 2)
    npc = Npc([(300, 300), (300, 400), (400, 400), (400, 300)])
    game_map = Map()

    # main game loop
    while True:
        for event in pygame.event.get():
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                    or (event.type == pygame.QUIT)):
                sys.exit(0)

        game_map.update_map_view(pygame.key.get_pressed())
        game_map.draw(screen)
        npc.update()

        player.draw(screen)
        m.update_map_view(pygame.key.get_pressed())
        npc.draw(screen, m.get_viewport())

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
