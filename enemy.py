import random

width = 640
height = 480

class Enemy:

    def __init__(self, word, surface, ms):
        self.word = word
        self.surface = surface
        self.ms = ms
        edge = random.randrange(4)
        if edge == 0:
            self.rect = surface.get_rect(center=(random.randrange(width), -100))
        elif edge == 1:
            self.rect = surface.get_rect(center=(random.randrange(width), height+100))
        elif edge == 2:
            self.rect = surface.get_rect(center=(-100, random.randrange(height)))
        elif edge == 3:
            self.rect = surface.get_rect(center=(width+100, random.randrange(height)))
        
