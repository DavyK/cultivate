from cultivate.loader import get_character
from cultivate.settings import WIDTH, HEIGHT


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = get_character()
        self.pickup = None

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        pygame.draw.rect(surface, (100, 100, 100), (WIDTH / 2 - 100, HEIGHT - 100, 200, 100))



