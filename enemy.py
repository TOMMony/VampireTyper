import random
import pygame

width = 640
height = 480
bat_surface = pygame.transform.scale(pygame.image.load("src/bat.png"), (50,50))
mudman_surface = pygame.transform.scale(pygame.image.load("src/mudman.png"), (80,80))

class Enemy:

    def __init__(self, word="type", ms=1, lives=1, type=None):
        self.word = word
        if not type:
            self.ms = ms
            self.lives = lives
        elif type == "Bat":
            self.surface = bat_surface
            self.ms = 3
            self.lives = 2
            self.wordtype = [2,3]
        elif type == "Green Mudman":
            self.surface = mudman_surface
            self.ms = 1
            self.lives = 2
            self.wordtype = [[2,3], [5,6,7,8]]

        edge = random.randrange(4)
        if edge == 0:
            self.rect = self.surface.get_rect(center=(random.randrange(width), -100))
        elif edge == 1:
            self.rect = self.surface.get_rect(center=(random.randrange(width), height+100))
        elif edge == 2:
            self.rect = self.surface.get_rect(center=(-100, random.randrange(height)))
        elif edge == 3:
            self.rect = self.surface.get_rect(center=(width+100, random.randrange(height)))
            
