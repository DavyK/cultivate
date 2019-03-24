from cultivate.loader import get_character


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = get_character()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
