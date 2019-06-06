import pygame
import sys
import random
import math

pygame.init()
Clock = pygame.time.Clock()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_width, display_height = pygame.display.get_surface().get_size()

background = (0, 0, 0)
font = pygame.font.Font(None, 24)
foreground = (200, 200, 200)

ship_image = pygame.image.load("resources/ship/ship_forward.png").convert()
ship_image = pygame.transform.scale(ship_image,(120,120))
           
ship_image_destroyed = pygame.image.load("resources/ship/ship_forward_dead.png")
ship_image_destroyed = pygame.transform.scale(ship_image_destroyed,(120,120))

bullet_image = pygame.image.load("resources/bullet/bullet_forward.png")
bullet_image = pygame.transform.scale(bullet_image,(12,12))
                
meteor_image = [pygame.image.load("resources/meteor.png"),
                pygame.image.load("resources/meteor2.png"),
                pygame.image.load("resources/meteor3.png")]


shoot_sound = pygame.mixer.Sound("resources/audio/shoot.ogg")
rocket_loop = pygame.mixer.Sound("resources/audio/rocket_loop.ogg")
meteor_destroy = pygame.mixer.Sound("resources/audio/shockwave.ogg")


pygame.mixer.init()
pygame.mixer.music.load("resources/audio/theme.ogg")
pygame.mixer.music.play(-1)
                
class Sprite:
    pass


def display_sprite(sprite):
    window.blit(sprite.image, (sprite.x, sprite.y))
    

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


ship = Sprite()
ship.x = 0
ship.y = 0
ship.angle = 0
ship.red = 0
ship.alpha = 0
ship.originalImage = ship_image
ship.image = ship.originalImage
ship.momentum = [0,0]


lives = 1
score = 75
fuelCost = 0.1
healthCost = 40
bulletSpeed = 22
turningSpeed = 3
maxSpeed = 20
InertialDampener = False
MachineGun = False
ShipHeat = 0
ShipShield = 100
OverHeating = False
Difficulty = 1

momentum = [0,0]

bullets = []
meteors = []
stars = []


frames_until_next_meteor = 0
frames_until_next_star = 0


def take_damage():
    global lives, ShipShield
    if (ShipShield > 99):
        ShipShield = 0
    else:
        lives -= 1


def fire_bullet():
    global ShipHeat
    shoot_sound.play()
    bullet = Sprite()
    radian = math.radians(ship.angle)            
    bullet.momentum = [(math.cos(radian)) * bulletSpeed,(-math.sin(radian)) * bulletSpeed]

    bullet.image = rot_center(bullet_image,ship.angle)
    rect = get_sprite_rectangle(ship)
    
    
    bullet.x = rect.centerx
    bullet.y = rect.centery
    bullet.timer = 0
       
    bullet.used = False    
    bullets.append(bullet)
    ShipHeat += 1


def add_meteor(image, x = 0, y = 0, size = -1, angle = -1):
    meteor = Sprite()
    meteor.momentum = [0,0]
    if (x == 0):
        meteor.x = window.get_width()
    else:
        meteor.x = x
    if (y == 0):
        meteor.y = random.randrange(100, window.get_height() - 100)
    else:
        meteor.y = y
        
    if (size == -1):
        meteor.size = random.randrange(10,200)
    else:
        meteor.size = size

    if (angle == -1):
        meteor.angle = random.randrange(0,360)
    else:
        meteor.angle = angle
    radian = math.radians(meteor.angle)   

    meteor.momentum[0] = math.cos(radian) * (((200 / meteor.size)))
    meteor.momentum[1] = -math.sin(radian) * (((200 / meteor.size)))

    meteor.rotDirection = random.randrange(1,2)
    if meteor.rotDirection > 1:
        meteor.rotDirection = -1
    meteor.originalImage = pygame.transform.scale(image, (meteor.size,meteor.size))
    meteor.image = meteor.originalImage
    meteor.hit = False
    meteors.append(meteor)


def add_star(xPos):
    star = Sprite()
    star.x = xPos
    star.y = random.randrange(10, window.get_height() - 10)
    star_size = random.randrange(1, 4)
    star.image = pygame.Surface((star_size, star_size))
   
    star.image.fill((255, 255, 255))    
    stars.append(star)

def get_sprite_rectangle(sprite):
    return sprite.image.get_rect().move(sprite.x, sprite.y)


for x in range(25):    
    add_star(random.randrange(1,window.get_width()))


while True:  

    FPS = Clock.get_fps() + 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
       
            if event.key == pygame.K_SPACE:
                if (not MachineGun and score >= 1 and lives > 0 and not OverHeating):
                    score -= 1
                    fire_bullet()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_UP:
                rocket_loop.stop()
            if event.key == pygame.K_LCTRL:
                InertialDampener = not InertialDampener
                rocket_loop.stop()
            if event.key == pygame.K_LALT:
                MachineGun = not MachineGun             

    pressed_keys = pygame.key.get_pressed()

    if (lives > 0 and score > 0 and not OverHeating):  
        if pressed_keys[pygame.K_LEFT]:          
            ship.angle += turningSpeed 
            ShipHeat += (fuelCost)   

        if pressed_keys[pygame.K_RIGHT]:        
            ship.angle -= turningSpeed
            ShipHeat += (fuelCost) 
                 
         
        max(ship.angle,0,360)

    if (lives > 0 and score > 0 and not OverHeating):
        if pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_UP]:
                        
            rocket_loop.play(-1)
            radian = math.radians(ship.angle)
            ship.momentum[0] += (math.cos(radian))
            ship.momentum[1] -= (math.sin(radian))           
                  
            score -= fuelCost        
            ShipHeat += (fuelCost * 8)            
        

        elif (InertialDampener):
            if (lives > 0 and score > 0 and abs(ship.momentum[0]) > 0.01 or abs(ship.momentum[1]) > 0.01):
                rocket_loop.play(2)
                radian = math.radians(ship.angle)
                ship.momentum[0] += -(ship.momentum[0] / 100)
                ship.momentum[1] += -(ship.momentum[1] / 100)   
                           
                score -= fuelCost * ((abs(ship.momentum[0]/10) + abs(ship.momentum[1]/10)))
                ShipHeat += (fuelCost * 2)    
            else:
                rocket_loop.stop()

    if pressed_keys[pygame.K_SPACE]:
        if (MachineGun and score >= 1 and lives > 0 and not OverHeating):
            score -= 1
            fire_bullet()

        



    if (ship.momentum[0] > maxSpeed):
        ship.momentum[0] = maxSpeed
    if (ship.momentum[0] < -maxSpeed):
        ship.momentum[0] = -maxSpeed

    if (ship.momentum[1] > maxSpeed):
        ship.momentum[1] = maxSpeed
    if (ship.momentum[1] < -maxSpeed):
        ship.momentum[1] = -maxSpeed

    ship.x = ship.x + (ship.momentum[0] / 2)
    ship.y = ship.y + (ship.momentum[1] / 2)

    if ship.y < 0:
        ship.y = window.get_height() - ship.image.get_height()        
        

    if ship.y > window.get_height() - ship.image.get_height():
        ship.y = 0
     

    if ship.x < 0:
        ship.x = window.get_width() - ship.image.get_width()

    if ship.x > window.get_width() - ship.image.get_width():
        ship.x = 0

    if (ShipHeat > 0):
        ShipHeat -= 0.15

    if (ShipShield < 100):
        ShipShield += 0.05

    if (ShipHeat > 100):
        OverHeating = True
    elif (ShipHeat < 1):
        OverHeating = False


    for bullet in bullets:
        bullet.x += bullet.momentum[0]
        bullet.y += bullet.momentum[1]
        
        if bullet.y < 0:
            bullet.y = window.get_height() - bullet.image.get_height()        
        

        if bullet.y > window.get_height() - bullet.image.get_height():
            bullet.y = 0
        

        if bullet.x < 0:
            bullet.x = window.get_width() - bullet.image.get_width()

        if bullet.x > window.get_width() - bullet.image.get_width():
            bullet.x = 0     

        bullet.timer += 1
        bullets = [bullet for bullet in bullets if not bullet.used and bullet.timer < ((100 * Difficulty) / len(bullets))]


    frames_until_next_meteor = frames_until_next_meteor - 1
    if frames_until_next_meteor <= 0:
        if (len(meteors) < Difficulty):
            frames_until_next_meteor = random.randrange(25, 100)
            add_meteor(random.choice(meteor_image))
        else:
            frames_until_next_meteor = 30

    for meteor in meteors:    
        if meteor.y < 0:
            meteor.y += abs(meteor.momentum[1])
            meteor.momentum[1] = -meteor.momentum[1]
        

        if meteor.y > window.get_height() - meteor.image.get_height():
            meteor.y += -abs(meteor.momentum[1])
            meteor.momentum[1] = -meteor.momentum[1]

        if meteor.x < 0:
            meteor.x += abs(meteor.momentum[0])
            meteor.momentum[0] = -meteor.momentum[0]

        if meteor.x > window.get_width() - meteor.image.get_width():
            meteor.x += -abs(meteor.momentum[0])
            meteor.momentum[0] = -meteor.momentum[0]


        meteor.x += meteor.momentum[0]
        meteor.y += meteor.momentum[1]
      


    meteors = [meteor for meteor in meteors if not meteor.hit]


    frames_until_next_star = frames_until_next_star - 1
    if frames_until_next_star <= 0:
        frames_until_next_star = random.randrange(10, 30)
        add_star(window.get_width())

    for star in stars:
        star.x = star.x - 2

    stars = [star for star in stars if star.x > - 10]

    
        
    ship.red = max(0, ship.red - 50)
    ship.alpha = max(0, ship.alpha - 2)
    ship_rect = get_sprite_rectangle(ship)
    

    for bullet in bullets:
        if (bullet.timer > 5):
            bullet_rect = get_sprite_rectangle(bullet)
            if bullet_rect.colliderect(ship_rect) and lives > 0:
                bullet.used = True
                take_damage()
                if lives == 0:
                    ship.alpha = 255
                else:
                    ship.red = 255


    for meteor in meteors:      
        meteor.image = rot_center(meteor.originalImage,meteor.angle)

        meteor.angle += ((200 / meteor.size)) * meteor.rotDirection
        max(meteor.angle,0,360)

        meteor_rect = get_sprite_rectangle(meteor)
        if meteor_rect.colliderect(ship_rect) and lives > 0:
            meteor.hit = True
            meteor.x = meteor.x - 6
            meteor.y = meteor.y - 6
            take_damage()
            if lives == 0:
                ship.alpha = 255
            else:
                ship.red = 255
            continue
                  
        for bullet in bullets:            
            if meteor_rect.colliderect(get_sprite_rectangle(bullet)):
                if (not bullet.used):
                    meteor_destroy.play()              
                    meteor.hit = True
                    bullet.used = True

                    radian = math.acos(bullet.momentum[0] / bulletSpeed)
                    angle = math.degrees(radian)
                    if ((meteor.size / 2) > 30):
                        add_meteor(meteor.originalImage,meteor.x,meteor.y,meteor.size / 2,angle + 10)
                        add_meteor(meteor.originalImage,meteor.x,meteor.y,meteor.size / 2,angle - 10)
             
                    score += (math.sqrt(meteor.size) / 2) + 1
                    Difficulty += 0.1
                continue
        
    if (score > 80 + healthCost):
        lives += 1
        score -= healthCost

    if (score < 5 and lives > 1):
        score += healthCost - 5
        take_damage()   

    
    window.fill(background)

    for star in stars:
        display_sprite(star)
    
    ship.image = rot_center(ship.originalImage,ship.angle)
    if lives == 0:
        tmp = pygame.Surface(ship_image_destroyed.get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (255, 255, 255, ship.alpha) )       
        tmp.blit(ship_image_destroyed, (0,0), ship_image_destroyed.get_rect(), pygame.BLEND_RGBA_MULT)
        ship.image = rot_center(tmp, ship.angle)
    if ship.red > 0:
        tmp = pygame.Surface(ship.image.get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (255, 255 - ship.red, 255 - ship.red, 255) )
        tmp.blit(ship.image, (0,0), ship.image.get_rect(), pygame.BLEND_RGBA_MULT)
        ship.image = tmp
     
   
    display_sprite(ship)    

    for bullet in bullets:
        display_sprite(bullet)

    for meteor in meteors:
        display_sprite(meteor)

    if (lives <= 0):
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf = font.render("Game Over...", True, (255,0,0))
        TextRect = TextSurf.get_rect()
        TextRect.center = ((display_width/2),(display_height/2))
        window.blit(TextSurf, TextRect)
    else:
        score_text = font.render("FUEL: " + str(int(score)), 1, foreground)
        score_text_pos = score_text.get_rect()
        score_text_pos.right = window.get_width() - 4
        score_text_pos.top = 10
        window.blit(score_text, score_text_pos)

        lives_text = font.render("LIVES: " + str(lives), 1, foreground)
        lives_text_pos = lives_text.get_rect()
        lives_text_pos.right = window.get_width() - 4
        lives_text_pos.top = 30
        window.blit(lives_text, lives_text_pos)

        shield_text = font.render("SHIELD: " + '%03d' % ShipShield + "%", 1, foreground)
        shield_text_pos = shield_text.get_rect()
        shield_text_pos.right = window.get_width() - 4
        shield_text_pos.top = 50
        window.blit(shield_text, shield_text_pos)

        heat_text = font.render("HEAT: " + '%03d' % ShipHeat + "/100", 1, foreground)
        heat_text_pos = heat_text.get_rect()
        heat_text_pos.right = window.get_width() - 4
        heat_text_pos.top = 70
        window.blit(heat_text, heat_text_pos)

        id_text = font.render("INERTIAL DAMPENERS: " + str(InertialDampener).upper(), 1, foreground)
        id_text_pos = id_text.get_rect()
        id_text_pos.right = window.get_width() - 4
        id_text_pos.top = 90
        window.blit(id_text, id_text_pos)

        mg_text = font.render("MACHINE GUN: " + str(MachineGun).upper(), 1, foreground)
        mg_text_pos = mg_text.get_rect()
        mg_text_pos.right = window.get_width() - 4
        mg_text_pos.top = 110
        window.blit(mg_text, mg_text_pos)
    
    

    pygame.display.flip()

    Clock.tick(60)