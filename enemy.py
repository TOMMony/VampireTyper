import random
import pygame
import requests
import string

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()

width = 640
height = 480
bat_surface = pygame.transform.scale(pygame.image.load("src/bat.png"), (50,50))
mudman_surface = pygame.transform.scale(pygame.image.load("src/mudman.png"), (80,80))
blinder_surface = pygame.transform.scale(pygame.image.load("src/blinder.png"), (200,200))
venus_surface = pygame.transform.scale(pygame.image.load("src/venus.png"), (100,100))
fire_surface = pygame.transform.scale(pygame.image.load("src/fire.png"), (10,10))

class Enemy:

    def __init__(self, word="type", ms=1, lives=1, type=None, dest=None, caster=None):
        self.dest = None
        self.caster = None
        self.type = type
        self.word = word
        if not type:
            self.ms = ms
            self.lives = lives
        elif type == "Bat":
            self.surface = bat_surface
            self.ms = 3
            self.lives = 1
            self.wordtype = [2,3]
            self.word = getWord(self.wordtype)
        elif type == "Green Mudman":
            self.surface = mudman_surface
            self.ms = 1
            self.lives = 1
            self.wordtype = [[2,3], [5,6,7,8]]
            self.word = getWord(self.wordtype)
        elif type == "Blinder":
            self.surface = blinder_surface
            self.ms = 1
            self.lives = 5
            self.wordtype = [range(5,9), range(5,8), range(5,9), range(2,10), range(5,8), range(1,10)]
            self.word = "YOU WILL SUCCUMB TO THE WRATH OF DEATH ITSELF"
        elif type == "Venus":
            self.surface = venus_surface
            self.ms = 1
            self.lives = 3
            self.wordtype = [range(5,9), range(5,8), range(5,9), range(2,10), range(5,8), range(1,10), range(8,9), range(4,7)]
            self.word = getWord(self.wordtype)
        elif type == "Projectile":
            if getattr(caster, "surface") == blinder_surface:
                self.surface = blinder_surface
                self.ms = 4
                self.lives = 120
            elif getattr(caster, "surface") == venus_surface:
                self.surface = fire_surface
                self.lives = 60
                self.ms = 1
            self.wordtype = [1]
            self.word = getWord([1])
            self.dest = dest
                
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

            
def getWord(n):
    if n == 1:
        return random.choice(string.ascii_letters)
    if isinstance(n, int):
        n = [n]
    if not isinstance(n[0], int):
        sentence = []
        for list in n:
            result = random.choice(WORDS)
            result = str(result)
            result = result[2:len(result) - 1]
            while len(result) not in list:
                result = result = random.choice(WORDS)
                result = str(result)
                result = result[2:len(result) - 1]
            sentence.append(result)
        result = " ".join(sentence)
    else:
        result = random.choice(WORDS)
        result = str(result)
        result = result[2:len(result) - 1]
        while len(result) not in n:
            result = result = random.choice(WORDS)
            result = str(result)
            result = result[2:len(result) - 1]
        result = str(result)
    return result