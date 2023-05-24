import pygame
import time

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

def moveTowards(fromRect, destination, ms):
    if fromRect.centerx > destination[0]:
        fromRect.centerx -= ms
    elif fromRect.centerx < destination[0]:
        fromRect.centerx += ms
    if fromRect.centery > destination[1]:
        fromRect.centery -= ms
    elif fromRect.centery < destination[1]:
        fromRect.centery += ms

def updateEnemies(player_rect):
    for enemy, enemyRect in zip(enemies_surface, enemies_rect):
        moveTowards(enemyRect, player_rect.center, 1)
        if enemyRect.collidepoint(player_rect.center):
            print("game over loser")

frames = 0
pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vampire Typers")
clock = pygame.time.Clock()
timerFont = pygame.font.Font(None, 50)
typeFont = pygame.font.Font(None, 25)
words = []
enemies_surface = []
enemies_rect = []

background = pygame.transform.scale(pygame.image.load("src/background.jpg").convert(),
                                    (width, height))
player_surface = pygame.transform.scale(pygame.image.load("src/reddeath.png").convert_alpha(),
                                      (100,100))
player_rect = player_surface.get_rect(center = (width/2,height/2))
text_surface = timerFont.render(str(round(frames/60)), False, "white")
bat_surface = pygame.transform.scale(pygame.image.load("src/bat.png").convert_alpha(),
                                     (50,50))
bat_rect = bat_surface.get_rect(topleft = (0, 0))
ms = 2
x,y = player_rect.topleft
time.sleep(5)

while True:
    if frames % 120 == 0:
        enemies_surface.append(bat_surface)
        enemies_rect.append(bat_surface.get_rect(topleft=(0,0)))
        words.append("type")
    text_surface = timerFont.render(str(round(frames/60)), False, "white")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            for i in range(len(words)):
                if len(words) > 0 and len(words[i]) > 0 and event.key == eval("pygame.K_" + words[i][0]):
                    #kill bats
                    if len(words[i]) > 1:
                        words[i] = words[i][1:]
                    else:
                        enemies_surface[i] = None
                        enemies_rect[i] = None
                        words[i] = None
            words = [i for i in words if i is not None]
            enemies_surface = [i for i in enemies_surface if i is not None]
            enemies_rect = [i for i in enemies_rect if i is not None]       

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.left -= ms
    if keys[pygame.K_RIGHT]:
        player_rect.right += ms
    if keys[pygame.K_UP]:
        player_rect.top -= ms
    if keys[pygame.K_DOWN]:
        player_rect.bottom += ms
    
    moveTowards(player_rect, pygame.mouse.get_pos(), 4)
    screen.blit(background, (0,0))
    for enemy, i, enemyRect in zip(enemies_surface, range(len(words)), enemies_rect):
        type_surface = typeFont.render(words[i], False, "white")
        screen.blit(enemy, enemyRect)
        screen.blit(type_surface, enemyRect.bottomleft)
        type_surface = typeFont.render(words[i], False, "white")
    screen.blit(player_surface, player_rect)
    screen.blit(text_surface, (width/2 - pygame.Surface.get_width(text_surface)/2,
                               100))
    updateEnemies(player_rect)
    pygame.display.update()
    clock.tick(60)
    frames += 1

    player_rect.left,player_rect.top = checkEdge(player_rect.left,
                                                 player_rect.top)


