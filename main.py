import pygame
import time
import requests
import random
import copy
import numpy as np
import sys
import string
from enemy import Enemy

def bossRush():
    if frames == 0:
        enemies.append(Enemy(type="Blinder"))
def spawnEnemy(enemies):
    if frames == 0:
        bossRush()
    if frames % 60 == 0:
        enemies.append(Enemy(word=getWord([1]), type="Projectile", dest=copy.deepcopy(player_rect.center), caster=enemies[0]))
    if frames > 3600:
        if frames % 60000  == 0:
            enemies.append(Enemy(word=getWord([2, 3]), type="Bat"))
        if frames % 1200000 == 0:
            sentence = " ".join([getWord([2,3]), getWord([5,6,7,8])])
            enemies.append(Enemy(word=sentence, type="Green Mudman"))
        if frames % 1200000 == 0:
            enemies.append(Enemy(type="Blinder"))
    elif frames > 3600 and frames < 7200:
        if frames % 300 == 0:
            sentence = " ".join([getWord([2,3]), getWord([5,6,7,8])])
            enemies.append(Enemy(word=sentence, type="Green Mudman"))

def getWord(n):
    if n == 1:
        return random.choice(string.ascii_letters)
    if isinstance(n, int):
        n = [n]
    result = random.choice(WORDS)
    result = str(result)
    result = result[2:len(result) - 1]
    while len(result) not in n:
        result = result = random.choice(WORDS)
        result = str(result)
        result = result[2:len(result) - 1]
    result = str(result)
    return result

def displayElements():
    for enemy in enemies:
        type_surface = typeFont.render(getattr(enemy, "word"), False, "white")
        screen.blit(getattr(enemy, "surface"), getattr(enemy, "rect"))
        
        #creating text border, background and display typing text (also makes sure text is visible always)
        global width, height
        x,y = getattr(enemy, "rect").midbottom
        if x > width:
            x = width - getattr(enemy, "rect").width/2
        elif x < 0:
            x = 0
        if y > height:
            y = height - getattr(enemy, "rect").height
        elif y < 0: 
            y = 0
        tempDisplayRect = type_surface.get_rect(midtop=(x,y))
        tempBorderRect = copy.deepcopy(tempDisplayRect); tempBorderRect.width += 3; tempBorderRect.height += 3
        tempBorderRect.center = tempDisplayRect.center
        pygame.draw.rect(screen, "yellow", tempBorderRect)
        pygame.draw.rect(screen, "black", tempDisplayRect)
        screen.blit(type_surface, tempDisplayRect)  

    screen.blit(player_surface, player_rect)
    screen.blit(text_surface, (width/2 - pygame.Surface.get_width(text_surface)/2,
                               100))
    pygame.draw.line(screen, "white", player_rect.center, pygame.mouse.get_pos())
    pygame.draw.rect(screen, "black", pygame.Rect(player_rect.bottomleft, (100,10)))
    pygame.draw.rect(screen, "red", pygame.Rect(player_rect.bottomleft, (hp,10)))

def checkEdge(x, y):
    if x <= -100:
        x = width
    elif x >= width + 100:
        x = - pygame.Surface.get_width(player_surface)
    if y <= -100:
        y = height
    elif y >= height + 100:
        y = - pygame.Surface.get_height(player_surface)
    return x,y

def checkCamera():
    global cameraX, cameraY
    screen.blit(background, (0 - cameraX, 0 - cameraY))
    screen.blit(background, (width - cameraX, 0 - cameraY))
    screen.blit(background, (-width - cameraX, 0 - cameraY))
    screen.blit(background, (0 - cameraX, height - cameraY))
    screen.blit(background, (0 - cameraX, -height - cameraY))
    screen.blit(background, (width - cameraX, height - cameraY))
    screen.blit(background, (-width - cameraX, height - cameraY))
    screen.blit(background, (width - cameraX, -height - cameraY))
    screen.blit(background, (-width - cameraX, -height - cameraY))
    if cameraY > height:
        cameraY = 0
    elif cameraY < 0:
        cameraY = height
    if cameraX > width:
        cameraX = 0
    elif cameraX < 0:
        cameraX = width
    
#Takes in player rect, but full enemy class as first argument
def moveTowards(enemy, destination, ms):
    fromRect = getattr(enemy, "rect")
    if getattr(enemy, "dest") is not None:
        destination = getattr(enemy, "dest")
    if fromRect.centerx > destination[0]:
        fromRect.centerx -= ms
    elif fromRect.centerx < destination[0]:
        fromRect.centerx += ms
    if fromRect.centery > destination[1]:
        fromRect.centery -= ms
    elif fromRect.centery < destination[1]:
        fromRect.centery += ms

def move(player_rect, position, ms):
    global cameraX, cameraY, player_surface
    if player_rect.collidepoint(pygame.mouse.get_pos()):
        return
    if position[0] > player_rect.centerx:
        cameraX += ms
        player_surface = pygame.transform.scale(pygame.image.load("src/reddeath1.png").convert_alpha(),
                                      (100,100))
        for enemy in enemies:
            getattr(enemy, "rect").centerx -= ms
            if getattr(enemy, "dest") is not None: setattr(enemy, "dest", (getattr(enemy, "dest")[0]-ms,getattr(enemy, "dest")[1])) 
    elif position[0] < player_rect.centerx:
        cameraX -= ms
        player_surface = pygame.transform.scale(pygame.image.load("src/reddeath.png").convert_alpha(),
                                      (100,100)) 
        for enemy in enemies:
            getattr(enemy, "rect").centerx += ms
            if getattr(enemy, "dest") is not None: setattr(enemy, "dest", (getattr(enemy, "dest")[0]+ms,getattr(enemy, "dest")[1])) 
    if position[1] > player_rect.centery:
        cameraY += ms
        for enemy in enemies:
            getattr(enemy, "rect").centery -= ms
            if getattr(enemy, "dest") is not None: setattr(enemy, "dest", (getattr(enemy, "dest")[0],getattr(enemy, "dest")[1]-ms)) 
    elif position[1] < player_rect.centery:
        cameraY -= ms
        for enemy in enemies:
            getattr(enemy, "rect").centery += ms
            if getattr(enemy, "dest") is not None: setattr(enemy, "dest", (getattr(enemy, "dest")[0],getattr(enemy, "dest")[1]+ms)) 
    
def updateEnemies(player_rect):
    global enemies
    for i in range(len(enemies)):
        moveTowards(enemies[i], player_rect.center, getattr(enemies[i], "ms"))
        if getattr(enemies[i], "rect").collidepoint(player_rect.center):
            global hp
            hp -= 1
        if getattr(enemies[i], "dest") is not None and getattr(enemies[i], "rect").collidepoint(getattr(enemies[i], "dest")):
            setattr(enemies[i], "lives", getattr(enemies[i], "lives") - 1)
            if getattr(enemies[i], "lives") <= 0:
                enemies[i] = None
    enemies = [i for i in enemies if i is not None]
    

def checkEvent():
    global event, enemies, hp, lifesteal
    if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(1)
    if event.type == pygame.KEYDOWN:
        for i in range(len(enemies)):
            if getattr(enemies[i], "word")[0] == " ":
                cmd = "pygame.K_SPACE"
            else:
                cmd = "pygame.K_" + getattr(enemies[i], "word")[0].lower()
            if len(enemies) > 0 and len(getattr(enemies[i], "word")) > 0 and event.key == eval(cmd):
                #kill enemies
                if len(getattr(enemies[i], "word")) > 1:
                    current = getattr(enemies[i], "word")
                    setattr(enemies[i], "word", current[1:])
                else:
                    if getattr(enemies[i], "type") == "Projectile":
                        setattr(enemies[i], "lives", getattr(enemies[i], "lives") - 9999999)
                    else:
                        setattr(enemies[i], "lives", getattr(enemies[i], "lives") - 1)
                    if getattr(enemies[i], "lives") > 0:
                        #FIND WAY TO CHECK N DIMENSION ARRAY DIFF SIZE
                        if isinstance(getattr(enemies[i], "wordtype")[0], int):
                            setattr(enemies[i], "word", getWord(getattr(enemies[i], "wordtype")))
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0]
                        elif isinstance(getattr(enemies[i], "wordtype")[0], list):
                            setattr(enemies[i], "word", " ".join([getWord(i) for i in getattr(enemies[i], "wordtype")]))
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0][0]
                    else:
                        if isinstance(getattr(enemies[i], "wordtype")[0], int):
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0]
                        elif isinstance(getattr(enemies[i], "wordtype")[0], list):
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0][0]
                        enemies[i] = None
        enemies = [i for i in enemies if i is not None]      

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()

frames = 0; width = 640; height = 480
pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vampire Typers")
clock = pygame.time.Clock()
timerFont = pygame.font.Font(None, 50)
typeFont = pygame.font.Font(None, 25)
background = pygame.transform.scale(pygame.image.load("src/background.png").convert(),
                                    (width, height))
player_surface = pygame.transform.scale(pygame.image.load("src/reddeath.png").convert_alpha(),
                                      (100,100))
player_rect = player_surface.get_rect(center = (width/2,height/2))
text_surface = timerFont.render(str(round(frames/60)), False, "white")

enemies = []

hp = 100; playerMS = 2; lifesteal = True; maxhp = 100

cameraX = 0; cameraY = 0; x,y = player_rect.topleft

time.sleep(1)

while True:
    if hp < 0:
        pygame.quit()
        sys.exit(1)
    elif hp > maxhp:
        hp = maxhp
    spawnEnemy(enemies)
    text_surface = timerFont.render(str(round(frames/60)), False, "white")
    for event in pygame.event.get():
        checkEvent()
    checkCamera()
    displayElements()
    updateEnemies(player_rect)
    move(player_rect, pygame.mouse.get_pos(), playerMS)
    pygame.display.update()
    clock.tick(60)
    frames += 1

    player_rect.left,player_rect.top = checkEdge(player_rect.left,
                                                 player_rect.top)


