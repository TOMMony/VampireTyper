import pygame
import time
import copy
import numpy as np
import sys
from enemy import Enemy, getWord

def bossRush(enemies):
    if frames == 0:
        enemies.append(Enemy(type="Blinder"))
    if frames % 60 == 0 and getattr(enemies[0], "type") == "Blinder":
        enemies.append(Enemy(type="Bat"))
def firstStage(enemies):
    seconds = frames / 60
    if seconds < 60 and seconds != 0 :
        if seconds % 2 == 0:
            enemies.append(Enemy(type="Bat"))
        if seconds % 10 == 0:
            enemies.append(Enemy(type="Green Mudman"))
        if seconds % 20 == 0:
            for i in range(2):
                enemies.append(Enemy(type="Bat"))
    elif seconds == 60:
        enemies.append(Enemy(type="Venus"))
        for i in range(10):
            enemies.append(Enemy(type="Green Mudman"))
    elif seconds < 120 and seconds != 0:
        if seconds % 40 == 0:
            for i in range(3):
                enemies.append(Enemy(type="Green Mudman"))
        elif seconds > 80:
            if not enemies:
                enemies.append(Enemy(type="Green Mudman"))
    elif seconds < 180 and seconds != 0:
        if len(enemies) == 0:
            enemies.append(Enemy(type="Green Mudman"))
    elif seconds == 180:
        for i in range(5):
            enemies.append(Enemy(type="Ghost"))
        enemies.append(Enemy(type="Mantichana"))
    elif seconds < 230 and seconds != 0:
        if seconds % 2 == 0:
            for i in range(3):
                enemies.append(Enemy(type="Ghost"))
    elif seconds == 240:
        bossRush(enemies)
def spawnEnemy(enemies):
    firstStage(enemies)
def spawnProjectile():
    for i in range(len(enemies)):
        if getattr(enemies[i], "type") == "Blinder":
            if frames % 60 == 0:
                enemies.append(Enemy(type="Projectile", dest=copy.deepcopy(player_rect.center), caster=enemies[i]))
        elif getattr(enemies[i], "type") == "Venus":
            if frames % 60 == 0:
                enemies.append(Enemy(type="Projectile", dest=copy.deepcopy(player_rect.center), caster=enemies[i]))
def displayElements():
    screen.blit(player_surface, player_rect)
    pygame.draw.rect(screen, "purple", pygame.Rect((0,0), ((experience/((level+1)*10 + level*10))*width,5)))
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
    screen.blit(text_surface, (width/2 - pygame.Surface.get_width(text_surface)/2,
                               100))
    pygame.draw.line(screen, "white", player_rect.center, pygame.mouse.get_pos())
    maxhpRect = pygame.Rect(player_rect.bottomleft, (maxhp,10))
    maxhpRect.midtop = player_rect.midbottom
    pygame.draw.rect(screen, "black", maxhpRect)
    pygame.draw.rect(screen, "red", pygame.Rect(maxhpRect.topleft, (hp,10)))
def levelUpScreen():
    screen.blit(maxHpChoice, hpRect)
    screen.blit(lifestealChoice, lifestealRect)
    screen.blit(msChoice, msRect)
    hpType = descriptFont.render("Blessing of Gus: Increases Max HP.", False, "white")
    lfType = descriptFont.render("Vampire's Blessing: Lifesteal Up!", False, "white")
    msType = descriptFont.render("Boots of Swiftness: Increases Movement Speed!!!", False, "white")
    screen.blit(hpType, hpRect)
    screen.blit(lfType, lifestealRect)
    screen.blit(msType, msRect)
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
#Unable to take decimal ms as center only supports int
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
    #if close enough to target then snap, prevents jiggling 
    if abs(fromRect.centerx - destination[0]) < ms:
            fromRect.centerx = destination[0]
    if abs(fromRect.centery - destination[1]) < ms:
            fromRect.centery = destination[1]
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
def knockback(enemy):
    position = getattr(enemy, "rect").center
    if position[0] > width/2:
        #push right
        getattr(enemy, "rect").centerx += knock 
    elif position[0] < width/2:
        #push left
        getattr(enemy, "rect").centerx -= knock
    if position[1] > height/2:
        getattr(enemy, "rect").centery += knock 
    elif position[1] < height/2:
        getattr(enemy, "rect").centery -= knock 
def updateEnemies(player_rect):
    global enemies
    for i in range(len(enemies)):
        moveTowards(enemies[i], player_rect.center, getattr(enemies[i], "ms"))
        if getattr(enemies[i], "rect").collidepoint(player_rect.center):
            knockback(enemies[i])
            global hp, armor
            #reduce difficulty by halving speedy monster damage
            if getattr(enemies[i], "ms") <= playerMS:
                hp -= 1/armor
            else:
                hp -= .5/armor
        if getattr(enemies[i], "dest") is not None and getattr(enemies[i], "rect").collidepoint(getattr(enemies[i], "dest")):
            setattr(enemies[i], "lives", getattr(enemies[i], "lives") - 1)
            if getattr(enemies[i], "lives") <= 0:
                enemies[i] = None
    enemies = [i for i in enemies if i is not None]
def checkEvent():
    global event, enemies, hp, lifesteal, experience
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
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0] * lifesteal
                        elif not isinstance(getattr(enemies[i], "wordtype")[0], int):
                            setattr(enemies[i], "word", getWord(getattr(enemies[i], "wordtype")))
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0][0] * lifesteal
                    elif getattr(enemies[i], "type") != "Projectile":
                        if isinstance(getattr(enemies[i], "wordtype")[0], int):
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0] * lifesteal
                            experience += getattr(enemies[i], "wordtype")[0]
                        elif isinstance(getattr(enemies[i], "wordtype")[0], list):
                            if lifesteal: hp+=getattr(enemies[i], "wordtype")[0][0] * lifesteal
                            experience += max(getattr(enemies[i], "wordtype")[0])
                        enemies[i] = None
                    else:
                        enemies[i] = None
        enemies = [i for i in enemies if i is not None]      
def checkEventLevel():
    global maxhp, levelUp, lifesteal, playerMS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hpRect.collidepoint(event.pos):
                maxhp += 50
                levelUp = False
            elif lifestealRect.collidepoint(event.pos):
                lifesteal += .5
                levelUp = False
            elif msRect.collidepoint(event.pos):
                playerMS += .2
                levelUp = False
        
    

frames = 0; width = 640; height = 480
pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vampire Typers")

maxHpChoice = pygame.Surface((width/2, height/5))
hpRect = maxHpChoice.get_rect(midtop=(width/2, height/8))
pygame.Surface.fill(maxHpChoice, "gray")
lifestealChoice = pygame.Surface((width/2, height/5))
lifestealRect = lifestealChoice.get_rect(center = (width/2, height/2))
pygame.Surface.fill(lifestealChoice, "gray")
msChoice = pygame.Surface((width/2, height/5))
msRect = msChoice.get_rect(midbottom = (width/2, height - height/8))
pygame.Surface.fill(msChoice, "gray")

clock = pygame.time.Clock()
timerFont = pygame.font.Font(None, 50)
typeFont = pygame.font.Font(None, 30)
descriptFont = pygame.font.Font(None, 20)
background = pygame.transform.scale(pygame.image.load("src/background.png").convert(),
                                    (width, height))
player_surface = pygame.transform.scale(pygame.image.load("src/reddeath.png").convert_alpha(),
                                      (100,100))
levelUp = False
player_rect = player_surface.get_rect(center = (width/2,height/2))
text_surface = timerFont.render(str(round(frames/60)), False, "white")

enemies = []

hp = 100; playerMS = 2; lifesteal = 0; maxhp = 100; knock = 2; armor = 1; experience = 0; level = 1

cameraX = 0; cameraY = 0; x,y = player_rect.topleft

time.sleep(1)

while True:
    pygame.display.update()
    if not levelUp:
        spawnProjectile()
        if hp < 0:
            pygame.display.quit()
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
        clock.tick(60)
        frames += 1
        player_rect.left,player_rect.top = checkEdge(player_rect.left,
                                                    player_rect.top)
        if experience >= (level + 1) * 10 + level * 10:
            level += 1
            levelUp = True 
    else:
        levelUpScreen()
        checkEventLevel()




