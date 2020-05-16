import pygame as pg
import random
import math
import time

pg.init()



screen = pg.display.set_mode((800, 600))
pg.display.set_caption('Mission Gamma')
pg.display.set_icon(pg.image.load('bullet.png'))

pX = 370
pY = 480
pXchange = 0
pYchange = 0
alien_dead_count = 0

running = True

b =  'space-ship.png'

def createAlien():
    a_count = random.randint(0,1)
    a = 'alien1.png'
    if a_count == 1:
        a = 'alien1.png'
    else:
        a = 'alien2.png'
    aX = random.randint(25, 706)
    aY = random.randint(100, 300)
    return aX, aY, a

aX, aY, a = createAlien()

bx = 0
bY = 430
aXchange = 0
aYchange = 0
bullet_state = 'ready'

def player(x, y, b):
    screen.blit(pg.image.load(b), (x, y))

def show_score(Score):
    score_s = pg.font.Font('freesansbold.ttf', 32).render("Score : " + str(Score), True, (255, 255, 255))
    screen.blit(score_s, (10, 10))

def show_level(Score):
    score_s = pg.font.Font('freesansbold.ttf', 32).render("Level : " + str(int(Score/20)), True, (255, 255, 255))
    screen.blit(score_s, (10, 52))

def show_life(dead_count):
    score_s = pg.font.Font('freesansbold.ttf', 32).render("Life : " + str(int(3-dead_count)), True, (255, 255, 255))
    screen.blit(score_s, (10, 94))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(pg.image.load('bullet1.png'), (x + 16, y + 10))

def alien(x, y, a):
    screen.blit(pg.image.load(a), (x, y))

# def win():
#     screen.blit(pg.font("You won!"))

def lost():
    # pg.mixer.music.set_volume(0.1)
    screen.blit(pg.font.Font('freesansbold.ttf', 64).render("GAME OVER", True, (255, 255, 255)), (200, 250))
    pg.display.update()
    show_score(score)
    show_level(score)
    pg.display.update()

n_aX, n_aY, n_a = createAlien()

d_count = 0
score = 0

pg.mixer.music.load("background.wav")
pg.mixer.music.play(0)

while running:


    for event in pg.event.get():
        if event.type == pg.QUIT:
            print('score = ', score)
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                pXchange += 15
            elif event.key == pg.K_LEFT:
                pXchange -= 15
            elif event.key == pg.K_SPACE:
                if bullet_state == 'ready':
                    pg.mixer.Sound('laser.wav').play()
                    bX = pX 
                    fire_bullet(bX, pY)
                    if aY <= 410 and pX < aX + 50 and pX > aX - 50:
                        fire_bullet(pX, pY)
                        score += 1
                        aX, aY, a = createAlien()
                        alien(aX, aY, a)
                        pg.mixer.Sound("explosion.wav").play()
                        bullet_state = "ready"
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or pg.K_RIGHT:
                pXchange = 0

    screen.blit(pg.image.load('background.png'), (0,0))

    pX += pXchange

    if pX <= 10:
        pX = 10
    elif pX >= 726:
        pX = 726

    if score/20 >= 1:
        alien(aX, aY, a)

    aX += aXchange

    if bY <= 0:
        bY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bX, bY)
        bY -= 20

    if aX >= 705:
        aXchange = -5
    elif aX <= 25:
        aXchange = 5
    
    for i in range(1000):
        aY += 0.003

    if aY >= 410:
        aX, aY, a = createAlien()
        alien_dead_count += 1

    if alien_dead_count >= 3:
        lost()
        time.sleep(5)
        break
        

    player(pX, pY, b)
    alien(aX, aY, a)
    show_score(score)
    show_level(score)
    show_life(alien_dead_count)

    pg.display.update()
