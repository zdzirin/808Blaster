import pygame
from classes import person, projectile, enemy
pygame.init()

#Initializing Game
winSize = width, height = 800, 500
WIN = pygame.display.set_mode(winSize)
pygame.display.set_caption("808 BLASTER >:)")
clock = pygame.time.Clock()
fps = 30
difficulty = 15
score = 0
lives = 3

#Assets
    #Images
bg = pygame.image.load('808Blaster/Images/background.jpg')

walkR = [pygame.image.load('808Blaster/Images/runcycle/F2.png'), pygame.image.load('808Blaster/Images/runcycle/F1.png')]
walkL = [pygame.transform.flip(walkR[0], True, False), pygame.transform.flip(walkR[1], True, False)]
charR = pygame.image.load('808Blaster/Images/character.png') # 100 X 140
charL = pygame.transform.flip(charR, True, False)
crouchR = pygame.image.load('808Blaster/Images/crouch.png') # 100 x 75
crouchL = pygame.transform.flip(crouchR, True, False)

projR = pygame.image.load('808Blaster/Images/808.png') # 70 x 50
projR = pygame.transform.scale(projR, (140, 100))
projL = pygame.transform.flip(projR, True, False)

doomHead = pygame.image.load('808Blaster/Images/doom.png') # 50 X 75

    #Sounds
santeria = pygame.mixer.Sound('808Blaster/Sounds/Santeria.wav')

    #Fonts
ghoust = pygame.font.Font('808Blaster/Font/Ghoust.otf', 32)
zigzag = pygame.font.Font('808Blaster/Font/ZigZag.otf', 64)

#Initializing user
user = person(50,height - 140,100,140,santeria)


#Drawing screen helper function
def redrawGameWindow():
    WIN.blit(bg, (0,0))
    global user, score

    pygame.draw.rect(WIN, (0,0,0), (0,0, 150, 80), 0)
    scoreText = ghoust.render('Score: ' + str(score), 1, (255,255,255))
    livesText = ghoust.render('Lives: ' + str(lives), 1, (255,255,255))
    WIN.blit(scoreText, (5,5))
    WIN.blit(livesText, (5,40))

    user.draw(WIN, charR, charL, crouchR, crouchL, walkR, walkL)
    #pygame.draw.rect(WIN, (255,0,0), user.hitbox, 1)
    for doom in dooms:
        doom.draw(WIN, doomHead)
        #pygame.draw.rect(WIN, (255,0,0), doom.hitbox, 1)
    for shot in shots:
        shot.draw(WIN, projR, projL)
        #pygame.draw.rect(WIN, (255,0,0), shot.hitbox, 1)
    pygame.display.update()

def drawGameOverWindow():
    WIN.fill((0,0,0))
    gameOverText = zigzag.render("GAME OVER!", 1, (255,255,255))
    scoreText = ghoust.render("You scored " + str(score), 1, (255,255,255))
    WIN.blit(gameOverText, (230,200))
    WIN.blit(scoreText, (310,300))
    pygame.display.update()


#Handling keys helper function
def handleKeyPress(keys):
    
    #walking
    if keys[pygame.K_a]:
        user.left = True
        user.right = False
        user.standing = False    
        user.walkCount -= 1
        pos = user.x - user.vel
        user.x = pos if pos > 0 else 0
        user.updateHitbox()
    elif keys[pygame.K_d]:
        user.right = True
        user.left = False
        user.standing = False
        user.walkCount += 1
        pos = user.x + user.vel
        user.x = pos if pos < (width - user.w) else (width - user.w)
        user.updateHitbox()
    else:
        user.walkCount = 0
        user.standing = True
    
    #crouching
    if keys[pygame.K_s]:
        if not user.isCrouched:
            user.isCrouched = True
            user.y += 65
            user.updateHitbox()
    else:
        if user.isCrouched:
            user.isCrouched = False
            user.y -= 65
            user.updateHitbox()

    #shooting
    if not user.isShoot:
        if keys[pygame.K_w] and user.hasEquipped:
            face = 1 if user.right else -1
            x = round(user.x + user.w // 2)
            x = x if face == 1 else x - 140
            y = user.y + 20
            user.equipped.play()
            shots.append(projectile(x, y, face))            
            user.isShoot = True
    else:
        user.shootCount += 1
        if user.shootCount > 10:
            user.shootCount = 0
            user.isShoot = False

    #jumping
    if not user.isJump:
        if keys[pygame.K_SPACE]:
            user.isJump = True
    else:
        if user.jumpCount >= -user.jL:
            userH = 75 if user.isCrouched else 140
            temp = user.y
            temp -= ((user.jumpCount ** 2) / 2) if (user.jumpCount > 1) else -((user.jumpCount ** 2) / 2)
            user.y = temp if temp < (height - userH) else (height - userH)
            user.jumpCount -= 1
            user.updateHitbox()
        else:
            user.isJump = False
            user.jumpCount = user.jL


shots = []
dooms = []
doomCount = 0
hitTimer = 0
gameOver = False
#Main Loop
run = True
while run:
    clock.tick(fps)
    # Exits game when user does
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if not gameOver:
        doomCount += 1
        if doomCount % difficulty == 0:
            dooms.append(enemy())

        if user.isHit:
            hitTimer += 1
        if hitTimer >= 30:
            hitTimer = 0
            user.isHit = False

        for shot in shots:
            if shot.x < (width - shot.w) and shot.x > 0:
                shot.x += shot.vel
                shot.updateHitbox()
            else:
                shots.pop(shots.index(shot))
        for doom in dooms:
            
            if (user.hitbox[0] < doom.hitbox[0] + doom.hitbox[2] and
                user.hitbox[0] + user.hitbox[2] > doom.hitbox[0] and
                user.hitbox[1] < doom.hitbox[1] + doom.hitbox[3] and
                user.hitbox[1] + user.hitbox[3] > doom.hitbox[1]
                and not user.isHit
                and doom.hitbox[1] < 500):
                    print(user.hitbox)
                    print(doom.hitbox)
                    lives -= 1
                    if lives <= 0:
                        gameOver = True
                    user.hit()
                    dooms.pop(dooms.index(doom))
                    continue
            
            for shot in shots:
                if (shot.hitbox[0] < doom.hitbox[0] + doom.hitbox[2] and
                    shot.hitbox[0] + shot.hitbox[2] > doom.hitbox[0] and
                    shot.hitbox[1] < doom.hitbox[1] + doom.hitbox[3] and
                    shot.hitbox[1] + shot.hitbox[3] > doom.hitbox[1] and
                    not doom.isHit):
                    score += 1
                    doom.hit()
                    shots.pop(shots.index(shot))

            if doom.isHit and (doom.y < 500):
                doom.y -= doom.vel
                doom.updateHitbox()
            elif (doom.x > 0):
                doom.x += doom.vel
                doom.updateHitbox()
            else:
                dooms.pop(dooms.index(doom))
        
        keys = pygame.key.get_pressed()
        handleKeyPress(keys)
        redrawGameWindow()
    
    else:
    
        drawGameOverWindow()


pygame.quit()
