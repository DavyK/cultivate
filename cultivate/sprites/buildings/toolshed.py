import pygame

from cultivate.loader import (get_bear, get_boxes, get_cage, get_cans,
                              get_carpet, get_tool_sign)
from cultivate.sprites import UpdatableSprite
from cultivate.sprites.buildings import DefaultBuilding


class ToolShed(DefaultBuilding):
    def get_sign(self) -> pygame.Surface:
        return get_tool_sign()

    def draw_items(self, map_background: pygame.Surface):
        cage, cage_x, cage_y = get_cage(), self.rect.x + 150, self.rect.y + 50
        carpet, carpet_x, carpet_y = get_carpet(), self.rect.x + 60, self.rect.y + 95
        boxes, boxes_x, boxes_y = get_boxes(), self.rect.x + 30, self.rect.y + 100
        cans, cans_x, cans_y = get_cans(), self.rect.x + 150, self.rect.y + 100
        bear, bear_x, bear_y = get_bear(), self.rect.x + 100, self.rect.y + 100
        map_background.blit(cage, (cage_x, cage_y))
        map_background.blit(carpet, (carpet_x, carpet_y))
        map_background.blit(boxes, (boxes_x, boxes_y))
        map_background.blit(cans, (cans_x, cans_y))
        map_background.blit(bear, (bear_x, bear_y))
        impassable_boxes = UpdatableSprite(
            pygame.Rect(boxes_x, boxes_y,
                        boxes.get_rect().w, boxes.get_rect().h)
        )
        self.impassables.add(impassable_boxes)
