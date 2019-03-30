import pygame

from cultivate.loader import get_bed, get_bed_sign, get_sideways_bed
from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import DefaultBuilding


class Dorm(DefaultBuilding):
    """Empty dormitory."""

    def get_sign(self) -> pygame.Surface:
        return get_bed_sign()

    def draw_items(self, map_background: pygame.Surface):
        pass


class HorizontalDorm(Dorm):
    """Dormitory with horizontal beds."""

    def draw_items(self, map_background: pygame.Surface):
        bed_left = get_sideways_bed()
        bed_right = pygame.transform.flip(bed_left, True, False)

        map_background.blit(bed_left, (self.rect.x + 8, self.rect.y + 50))
        map_background.blit(bed_right, (self.rect.x + 130, self.rect.y + 50))

        map_background.blit(bed_left, (self.rect.x + 8, self.rect.y + 100))
        map_background.blit(bed_right, (self.rect.x + 130, self.rect.y + 100))

        map_background.blit(bed_left, (self.rect.x + 8, self.rect.y + 150))
        map_background.blit(bed_right, (self.rect.x + 130, self.rect.y + 150))
        impassable_beds = [
            UpdatableSprite(
                pygame.Rect(self.rect.x + 8, self.rect.y + 50,
                    bed_left.get_rect().w, bed_right.get_rect().h
                )
            ),
            UpdatableSprite(
                pygame.Rect(self.rect.x + 130, self.rect.y + 50,
                    bed_right.get_rect().w, bed_right.get_rect().h
                )
            ),
            UpdatableSprite(
                pygame.Rect(self.rect.x + 8, self.rect.y + 100,
                    bed_left.get_rect().w, bed_right.get_rect().h
                )
            ),
            UpdatableSprite(
                pygame.Rect(self.rect.x + 130, self.rect.y + 100,
                    bed_left.get_rect().w, bed_right.get_rect().h
                )
            ),
            UpdatableSprite(
                pygame.Rect(self.rect.x + 8, self.rect.y + 150,
                    bed_left.get_rect().w, bed_right.get_rect().h
                )
            ),
            UpdatableSprite(
                pygame.Rect(self.rect.x + 130, self.rect.y + 150,
                    bed_left.get_rect().w, bed_right.get_rect().h
                )
            ),
        ]

        self.impassables.add(impassable_beds)


class VerticalDorm(Dorm):
    """Dormitory with vertical beds."""

    def draw_items(self, map_background: pygame.Surface):
        bed = get_bed()

        map_background.blit(bed, (self.rect.x + 25, self.rect.y + 50))
        map_background.blit(bed, (self.rect.x + 145, self.rect.y + 50))

        impassable_beds = [
            UpdatableSprite(
                pygame.Rect(self.rect.x + 25, self.rect.y + 50,
                    bed.get_rect().w, bed.get_rect().h
                )
            ),
            UpdatableSprite(
                pygame.Rect(self.rect.x + 145, self.rect.y + 50,
                    bed.get_rect().w, bed.get_rect().h
                )
            ),
        ]

        self.impassables.add(impassable_beds)
