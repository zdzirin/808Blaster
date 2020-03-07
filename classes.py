import random





class person(object):
    def __init__(self, x, y, width, height, sound):
        # Character size and position
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.hitbox = (self.x + 28, self.y + 14, 60, 127)
        
        self.isCrouched = False
        self.isHit = False

        # Movement
        # Jumping
        self.isJump = False
        self.jL = 10 #Length/Height of jump
        self.jumpCount = self.jL
        # Walking
        self.left, self.right, self.standing = False, True, True
        self.walkCount = 0
        self.vel = 10
        #Shooting
        self.isShoot = False
        self.shootCount = 0
        #THESE ONES NEED TO BE CHANGED LATER
        self.hasEquipped = True
        self.equipped = sound

    def hit(self):
        self.isHit = True

    def updateHitbox(self):
        if not self.left:
            if not self.isCrouched:
                self.hitbox = (self.x + 28, self.y + 14, 60, 127)
            else:
                self.hitbox = (self.x, self.y + 7, 90, 75)
        else:
            if not self.isCrouched:
                self.hitbox = (self.x, self.y + 14, 60, 127)
            else:
                self.hitbox = (self.x, self.y + 7, 90, 75)

    def draw(self, WIN, charR, charL, crouchR, crouchL, walkR, walkL):
        #Logic for which character image is drawn
        if self.isCrouched:
            if self.right:
                WIN.blit(crouchR, (self.x,self.y))
            else:
                WIN.blit(crouchL, (self.x,self.y))
        
        elif self.standing:
            if self.right:
                WIN.blit(charR, (self.x,self.y))
            else:
                WIN.blit(charL, (self.x,self.y))
        
        else:
            index = 1 if (abs(self.walkCount) > 3) or self.isJump else 0
            if self.right:
                WIN.blit(walkR[index], (self.x,self.y))
            else:
                WIN.blit(walkL[index], (self.x,self.y))





class projectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.w = 140
        self.h = 100
        self.vel = 20 * facing
        self.facing = facing
        if self.facing == 1:
            self.hitbox = (self.x + 100, self.y, 40, 100)
        else:
            self.hitbox = (self.x, self.y, 40, 100)

    def updateHitbox(self):
        if self.facing == 1:
            self.hitbox = (self.x + 100, self.y, 40, 100)
        else:
            self.hitbox = (self.x, self.y, 40, 100)

    def draw(self, WIN, projR, projL):
        if self.facing == 1:
            WIN.blit(projR, (self.x, self.y))
        else:
            WIN.blit(projL, (self.x, self.y))


class enemy(object):
    def __init__(self):
        self.x = 800 
        self.y = random.randint(200, 425)
        self.vel = -1 * random.randint(5,20)
        self.hitbox = (self.x, self.y, 50, 49)
        self.isHit = False

    def updateHitbox(self):
        self.hitbox = (self.x, self.y, 50, 49)

    def hit(self):
        self.isHit = True

    def draw(self, WIN, doomHead):
        WIN.blit(doomHead, (self.x, self.y))

