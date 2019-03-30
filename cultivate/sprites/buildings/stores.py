import pygame

from cultivate.loader import get_boxes, get_cans, get_stores_sign
from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import DefaultBuilding


class Stores(DefaultBuilding):
    def get_sign(self) -> pygame.Surface:
        return get_stores_sign()

    def draw_items(self, map_background: pygame.Surface):
        boxes, boxes_x, boxes_y = get_boxes(), self.rect.x + 30, self.rect.y + 100
        cans, cans_x, cans_y = get_cans(), self.rect.x + 150, self.rect.y + 100

        map_background.blit(boxes, (boxes_x, boxes_y))
        map_background.blit(cans, (cans_x, cans_y))
        impassable_boxes = UpdatableSprite(
            pygame.Rect(boxes_x, boxes_y,
                        boxes.get_rect().w, boxes.get_rect().h)
        )
        self.impassables.add(impassable_boxes)
