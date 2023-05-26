import random
import pygame

width = 640
height = 480
bat_surface = pygame.transform.scale(pygame.image.load("src/bat.png"), (50,50))
mudman_surface = pygame.transform.scale(pygame.image.load("src/mudman.png"), (80,80))
blinder_surface = pygame.transform.scale(pygame.image.load("src/blinder.png"), (200,200))

class Enemy:

    def __init__(self, word="type", ms=1, lives=1, type=None, dest=None, caster=None):
        self.word = word
        self.dest = None
        self.caster = None
        self.type = type
        if not type:
            self.ms = ms
            self.lives = lives
        elif type == "Bat":
            self.surface = bat_surface
            self.ms = 3
            self.lives = 1
            self.wordtype = [2,3]
        elif type == "Green Mudman":
            self.surface = mudman_surface
            self.ms = .5
            self.lives = 1
            self.wordtype = [[2,3], [5,6,7,8]]
        elif type == "Blinder":
            self.surface = blinder_surface
            self.ms = 1
            self.lives = 5
            self.wordtype = [range(5,9), range(5,8), range(5,9), range(2,10), range(5,8), range(1,10)]
            self.word = "YOU WILL SUCCUMB TO THE WRATH OF DEATH ITSELF"
        elif type == "Projectile":
            self.surface = blinder_surface
            self.ms = 2
            self.lives = 1
            self.wordtype = [1]
            self.dest = dest
            if getattr(caster, "surface") == blinder_surface:
                self.ms = 4
                self.lives = 120
        edge = random.randrange(4)
        if not type == "Projectile":
            if edge == 0:
                self.rect = self.surface.get_rect(center=(random.randrange(width), -100))
            elif edge == 1:
                self.rect = self.surface.get_rect(center=(random.randrange(width), height+100))
            elif edge == 2:
                self.rect = self.surface.get_rect(center=(-100, random.randrange(height)))
            elif edge == 3:
                self.rect = self.surface.get_rect(center=(width+100, random.randrange(height)))
        else:
            self.rect = self.surface.get_rect(center=getattr(caster, "rect").center)
            
