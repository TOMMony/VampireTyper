
class Enemy:

    def __init__(self, word, surface, ms):
        self.word = word
        self.surface = surface
        self.rect = surface.get_rect()
        self.ms = ms
