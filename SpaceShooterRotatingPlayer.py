import pygame
import sys
import random
import math

pygame.init()
Clock = pygame.time.Clock()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

background = (0, 0, 0)
font = pygame.font.Font(None, 24)
foreground = (200, 200, 200)

ship_image = pygame.image.load("resources/ship/ship_forward.png").convert()
ship_image = pygame.transform.scale(ship_image,(120,120))
           
ship_image_destroyed = pygame.image.load("resources/ship/ship_forward_dead.png")
           
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


lives = 10
score = 75
fuelCost = 0.1
healthCost = 40
bulletSpeed = 22
turningSpeed = 3
maxSpeed = 20
InertialDampener = False
MachineGun = False
Difficulty = 1

momentum = [0,0]

bullets = []
meteors = []
stars = []


frames_until_next_meteor = 0
frames_until_next_star = 0

def fire_bullet():
    shoot_sound.play()
    bullet = Sprite()
    radian = math.radians(ship.angle)            
    bullet.momentum = [(math.cos(radian)) * bulletSpeed,(-math.sin(radian)) * bulletSpeed]

    bullet.image = rot_center(bullet_image,ship.angle)
    rect = get_sprite_rectangle(ship)
    
    
    bullet.x = rect.centerx
    bullet.y = rect.centery
       
    bullet.used = False    
    bullets.append(bullet)


def add_meteor(image, x = 0, y = 0, size = -1):
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

    meteor.angle = random.randrange(0,360)
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
                if (score >= 1 and lives > 0):
                    score -= 1
                    fire_bullet()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                rocket_loop.stop()
            if event.key == pygame.K_LCTRL:
                InertialDampener = not InertialDampener
                rocket_loop.stop()
            
                

        pressed_keys = pygame.key.get_pressed()


    if (lives > 0 and score > 0):      

        if pressed_keys[pygame.K_LEFT]:          
            ship.angle += turningSpeed   

        if pressed_keys[pygame.K_RIGHT]:        
            ship.angle -= turningSpeed
                 
        max(ship.angle,0,360)

    if (lives > 0 and score > 0):
        if pressed_keys[pygame.K_LSHIFT]:
                        
            rocket_loop.play(-1)
            radian = math.radians(ship.angle)
            ship.momentum[0] += (math.cos(radian))
            ship.momentum[1] -= (math.sin(radian))           
                  
            score -= fuelCost                    
        

        elif (InertialDampener):
            if (lives > 0 and score > 0 and abs(ship.momentum[0] > 0) or abs(ship.momentum[1] > 0)):
                rocket_loop.play(-1)
                radian = math.radians(ship.angle)
                ship.momentum[0] += -(ship.momentum[0] / 10)
                ship.momentum[1] += -(ship.momentum[1] / 10)   
                           
                score -= fuelCost * ((abs(ship.momentum[0] + abs(ship.momentum[1])/10)))  
            else:
                rocket_loop.stop()

        



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

    for bullet in bullets:
        bullet.x += bullet.momentum[0]
        bullet.y += bullet.momentum[1]
        bullets = [bullet for bullet in bullets if bullet.x < window.get_width() and not bullet.used]


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
      


    #meteors = [meteor for meteor in meteors if meteor.x > - meteor.image.get_width() and not meteor.hit]
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
    

    for meteor in meteors:      
        meteor.image = rot_center(meteor.originalImage,meteor.angle)

        meteor.angle += ((200 / meteor.size)) * meteor.rotDirection
        max(meteor.angle,0,360)

        meteor_rect = get_sprite_rectangle(meteor)
        if meteor_rect.colliderect(ship_rect) and lives > 0:
            meteor.hit = True
            meteor.x = meteor.x - 6
            meteor.y = meteor.y - 6
            lives = lives - 1
            if lives == 0:
                ship.x = ship.x - 50
                ship.alpha = 255
            else:
                ship.red = 255
            ship.red = 255
            continue
                  
        for bullet in bullets:            
            if meteor_rect.colliderect(get_sprite_rectangle(bullet)):
                if (not bullet.used):
                    meteor_destroy.play()              
                    meteor.hit = True
                    bullet.used = True

                    if ((meteor.size / 2) > 15):
                        add_meteor(meteor.originalImage,meteor.x,meteor.y,meteor.size / 2)
                        add_meteor(meteor.originalImage,meteor.x,meteor.y,meteor.size / 2)

               

                    score += (math.sqrt(meteor.size) / 2) + 1
                    Difficulty += 0.1
                continue
        
    if (score > 100 + healthCost):
        lives += 1
        score -= healthCost

    if (score < 5 and lives > 1):
        score += healthCost - 5
        lives -= 1   

    
    window.fill(background)

    for star in stars:
        display_sprite(star)
    
           
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


   
    ship.image = rot_center(ship.originalImage,ship.angle)
   
   
    display_sprite(ship)
  
    

    for bullet in bullets:
        display_sprite(bullet)

    for meteor in meteors:
        display_sprite(meteor)

    score_text = font.render("FUEL: " + str(int(score)), 1, foreground)
    score_text_pos = score_text.get_rect()
    score_text_pos.right = window.get_width() - 4
    score_text_pos.top = 10
    window.blit(score_text, score_text_pos)

    lives_text = font.render("LIVES: " + str(lives), 1, foreground)
    lives_text_pos = score_text.get_rect()
    lives_text_pos.right = window.get_width() - 4
    lives_text_pos.top = 30
    window.blit(lives_text, lives_text_pos)

    id_text = font.render("INERTIAL DAMPENERS: " + str(InertialDampener).upper(), 1, foreground)
    id_text_pos = score_text.get_rect()
    id_text_pos.right = window.get_width() - 185
    id_text_pos.top = 50
    window.blit(id_text, id_text_pos)
    

    pygame.display.flip()

    Clock.tick(60)