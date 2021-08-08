import pygame
import math
import random
from pygame import mixer

#Intialize the pygame
pygame.init()

# Background
background= pygame.image.load("background.png")

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#create the screen
screen= pygame.display.set_mode((800,600))

#Caption and icon
pygame.display.set_caption("Space Invaders")
icon= pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerImg= pygame.image.load("spaceship.png")
playerX= 370
playerY= 480
playerX_change=0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg =pygame.image.load("bullet.png")
bulletX= 0
bulletY=480
bulletX_change= 0
bulletY_change= 10
bullet_state = "ready"

#Font
score_value = 0
font= pygame.font.Font("timesnewarial.ttf", 32)
textX= 10
textY= 10

#Game over font
over_font = pygame.font.Font("timesnewarial.ttf", 64)

def show_score(x,y):
    score =font.render("Score : " + str(score_value), True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    over_text =over_font.render("GAME OVER ", True,(255,255,255))
    screen.blit(over_text,(200,250))
  
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y,))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance< 27:
        return True
    else:
        return False

#Game Loop
running=True
while running:
    #RGB =Red ,Green, Blue
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running:False

    # IF keystorke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_LEFT:
                playerX_change= -6
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if bullet_state=="ready":
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
    
        if event.type== pygame.KEYUP:
            if event.key== pygame.K_LEFT or event.key== pygame.K_RIGHT:
                playerX_change= 0        
        
    #Checking for boundaries so it doesn't go
    playerX+= playerX_change

    if playerX <= 0:
        playerX=0
    elif playerX>= 736:
        playerX=736

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
           for j in range(num_of_enemies):
                enemyY[j] = 2000
           game_over()
           break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]= 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]=-5
            enemyY[i] += enemyY_change[i]

    
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY) 
        if collision:
            explosion_sound=mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i]= random.randint(0,800)
            enemyY[i]= random.randint(50,100)

        enemy(enemyX[i],enemyY[i],i)
            
    #bullet  movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()

