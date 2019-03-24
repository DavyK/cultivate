class Scene:
    font_color = "black"
    background_color = "black"

    def __init__(self):
        self.finished = False

    def key_pressed(self, key):
        return False

    def mouse_pressed(self, pos):
        return False

    def draw(self, surface):
        pass

    def update(self):
        pass

    def is_finished(self):
        return self.finished

    def finish(self):
        self.finished = True
