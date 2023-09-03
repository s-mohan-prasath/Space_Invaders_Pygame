import pygame
from pygame import mixer
import random
from math import sqrt

pygame.init()
ssTup = (800, 600)
icon = pygame.image.load("assets/icons/space-shuttle_32.png")
bg = pygame.image.load("assets/images/bg.jpg")
font = pygame.font.Font("freesansbold.ttf", 24)
over_text = pygame.font.Font("freesansbold.ttf", 65)

# Playing background music
mixer.music.load('assets/audios/bg-music.mp3')
mixer.music.play(-1)

# Player

pimg = pygame.image.load("assets/icons/space-shuttle_64.png")
pX = ssTup[0]/2 - 32
pY = ssTup[1] - 128
pChange = 0

# Enemy

eimg = pygame.image.load("assets/icons/alien-shuttle_64.png")
eX = random.randint(64, 736)
eY = 64
eChangeX = 0.2
eChangeY = 32

# Bullet

bimg = pygame.image.load("assets/icons/bullet.png")
bChangeY = 0.8
bX = pX
bY = 480
b_state = "ready"  # "ready", "fire"

screen = pygame.display.set_mode(ssTup)
pygame.display.set_icon(icon)
pygame.display.set_caption("My First PyGame")

# Score

score_val = 0


# Functions

def show_score(x, y):
    score = font.render("Score : " + str(score_val), True,
                        (255, 255, 255), (0, 0, 0))
    screen.blit(score, (x, y))


def game_over():
    final_text = over_text.render("GAME OVER", True, (255, 255, 255))
    screen.blit(final_text, (200, 280))


def player(x, y):
    screen.blit(pimg, (x, y))


def enemy(x, y):
    screen.blit(eimg, (x, y))


def fire_bullet(x, y):
    global b_state
    b_state = "fire"
    screen.blit(bimg, (x, y))


def isCollision(x1, y1, x2, y2):
    d = sqrt((x2-x1)**2 + (y2-y1)**2)
    if d <= 32:
        return True
    else:
        return False


done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pChange = -0.5
            if event.key == pygame.K_RIGHT:
                pChange = 0.5
            if event.key == pygame.K_SPACE:
                if b_state == 'ready':
                    bX = pX + 16
                    b_sound = mixer.Sound("assets/audios/laser.wav")
                    b_sound.play()
                    fire_bullet(bX, bY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pChange = 0
    screen.fill((0, 0, 0))
    # Changing Background
    screen.blit(bg, (0, 0))

    pX += pChange
    eX += eChangeX

    # PLAYER MOVEMENT MECHANICS

    if pX >= 734:
        pX = 734
    elif pX <= 0:
        pX = 0

    # ENEMY MOVEMENT MECHANICS

    if eX >= 734:
        eX = 734
        eChangeX = -0.3
        eY += eChangeY
    elif eX <= 0:
        eX = 0
        eChangeX = 0.3
        eY += eChangeY
    elif eY >= 420:
        eY = 2000
        game_over()

    # BULLET MOVEMENT MECHANICS

    if b_state == 'fire':
        fire_bullet(bX, bY)
        bY -= bChangeY
    if bY <= 0:
        b_state = 'ready'
        bY = 480

    collision = isCollision(bX, bY, eX, eY)
    if collision:
        b_state = 'ready'
        collision_sound = mixer.Sound("assets/audios/explosion.wav")
        collision_sound.play()
        bY = 480
        score_val += 1
        eX = random.randint(64, 736)
        eY = 64

    player(pX, pY)
    enemy(eX, eY)
    show_score(10, 10)
    pygame.display.update()