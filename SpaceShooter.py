import pygame
import sys
import random
import math

pygame.init()
Clock = pygame.time.Clock()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

background = (0, 0, 0)
font = pygame.font.Font(None, 24)
foreground = (200, 200, 200)

ship_image = [pygame.image.load("resources/ship/ship_up.png"),
            pygame.image.load("resources/ship/ship_forward.png"),
            pygame.image.load("resources/ship/ship_down.png"),
            pygame.image.load("resources/ship/ship_back.png")]
ship_image_destroyed = [pygame.image.load("resources/ship/ship_up_dead.png"),
            pygame.image.load("resources/ship/ship_forward_dead.png"),
            pygame.image.load("resources/ship/ship_down_dead.png"),
            pygame.image.load("resources/ship/ship_back_dead.png")]
bullet_image = [pygame.image.load("resources/bullet/bullet_up.png"),
                pygame.image.load("resources/bullet/bullet_forward.png"),
                pygame.image.load("resources/bullet/bullet_down.png"),
                pygame.image.load("resources/bullet/bullet_back.png")]
meteor_image = [pygame.image.load("resources/meteor.png"),
                pygame.image.load("resources/meteor2.png"),
                pygame.image.load("resources/meteor3.png")]

shoot_sound = pygame.mixer.Sound("resources/audio/shoot.ogg")
rocket_loop = pygame.mixer.Sound("resources/audio/rocket_loop.ogg")


pygame.mixer.init()
pygame.mixer.music.load("resources/audio/theme.ogg")
pygame.mixer.music.play(-1)
                



class Sprite:
    pass

def display_sprite(sprite):
    window.blit(sprite.image, (sprite.x, sprite.y))

ship = Sprite()
ship.x = 0
ship.y = 0
ship.direction = 1
ship.red = 0
ship.alpha = 0
ship.image = ship_image[1]
ship.momentum = [0,0]


lives = 3
score = 75
fuelCost = 0.5
healthCost = 25
bulletSpeed = 13

momentum = [0,0]

bullets = []
meteors = []
stars = []


frames_until_next_meteor = 0
frames_until_next_star = 0

def fire_bullet():
    shoot_sound.play()
    bullet = Sprite()
    bullet.momentum = [0,0]
    
    #bullet.momentum[0] = ship.momentum[0]
    #bullet.momentum[1] = ship.momentum[1]

    if (ship.direction == 0):
        bullet.momentum[1] += -13
        bullet.x = ship.x + 62
        bullet.y = ship.y
        
    elif (ship.direction == 1):
        bullet.momentum[0] += 13        
        bullet.x = ship.x + 160
        bullet.y = ship.y + 62
        
    elif (ship.direction == 2):
        bullet.momentum[1] += 13
        bullet.x = ship.x + 62
        bullet.y = ship.y + 160
    elif (ship.direction == 3):
        bullet.momentum[0] += -13
        bullet.x = ship.x
        bullet.y = ship.y + 62
    bullet.image = bullet_image[ship.direction]
    bullet.used = False    
    bullets.append(bullet)


def add_meteor():
    meteor = Sprite()
    meteor.x = window.get_width()
    meteor.y = random.randrange(100, window.get_height() - 100)
    meteor.size = random.randrange(10,200)
    meteor.angle = random.randrange(0,360)
    meteor.rotDirection = random.randrange(1,2)
    if meteor.rotDirection > 1:
        meteor.rotDirection = -1
    meteor.originalImage = pygame.transform.scale(random.choice(meteor_image), (meteor.size,meteor.size))
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


#Setup
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
            
                

        pressed_keys = pygame.key.get_pressed()


    if (lives > 0 and score > 0):
        if pressed_keys[pygame.K_UP]:            
            ship.direction = 0            

        if pressed_keys[pygame.K_DOWN]:            
            ship.direction = 2           

        if pressed_keys[pygame.K_LEFT]:          
            ship.direction = 3            

        if pressed_keys[pygame.K_RIGHT]:            
            ship.direction = 1          

    if (score > 0):
        if pressed_keys[pygame.K_LSHIFT]:
            rocket_loop.play(-1)

            if (ship.direction == 0):
                ship.momentum[1] -= 0.5
            elif (ship.direction == 1):
                ship.momentum[0] += 0.5
            elif (ship.direction == 2):
                ship.momentum[1] += 0.5
            elif (ship.direction == 3):
                ship.momentum[0] -= 0.5            
            score -= fuelCost                    
        



    if (ship.momentum[0] > 10):
        ship.momentum[0] = 10
    if (ship.momentum[0] < -10):
        ship.momentum[0] = - 10

    if (ship.momentum[1] > 10):
        ship.momentum[1] = 10
    if (ship.momentum[1] < -10):
        ship.momentum[1] = - 10

    ship.x = ship.x + (ship.momentum[0] / 2)
    ship.y = ship.y + (ship.momentum[1] / 2)

    if ship.y < 0:
        ship.y = 0
        ship.momentum[1] = -ship.momentum[1] / 2
        

    if ship.y > window.get_height() - ship.image.get_height():
        ship.y = window.get_height() - ship.image.get_height()
        ship.momentum[1] = -ship.momentum[1] / 2

    if ship.x < 0:
        ship.x = 0
        ship.momentum[0] = -ship.momentum[0] / 2

    if ship.x > window.get_width() - ship.image.get_width():
        ship.x = window.get_width() - ship.image.get_width()
        ship.momentum[0] = -ship.momentum[0] / 2

    for bullet in bullets:
        bullet.x += bullet.momentum[0]
        bullet.y += bullet.momentum[1]
        bullets = [bullet for bullet in bullets if bullet.x < window.get_width() and not bullet.used]


    frames_until_next_meteor = frames_until_next_meteor - 1
    if frames_until_next_meteor <= 0:
        frames_until_next_meteor = random.randrange(25, 100)
        add_meteor()

    for meteor in meteors:        
        meteor.x = meteor.x - 3


    meteors = [meteor for meteor in meteors if meteor.x > - meteor.image.get_width() and not meteor.hit]


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

        orig_rect = meteor.image.get_rect()
        rot_image = pygame.transform.rotate(meteor.originalImage, meteor.angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        meteor.image = rot_image.subsurface(rot_rect).copy()

        meteor.angle += ((200 / meteor.size)) * meteor.rotDirection
        if meteor.angle > 360:
            meteor.angle -= 360
        elif meteor.angle < 0:
            meteor.angle += 360

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
                meteor.hit = True
                bullet.used = True
                score += (math.sqrt(meteor.size) / 2) + 1
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

    ship.image = ship_image[ship.direction]
    if lives == 0:
        tmp = pygame.Surface(ship_image_destroyed[ship.direction].get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (255, 255, 255, ship.alpha) )
        tmp.blit(ship_image_destroyed[ship.direction], (0,0), ship_image_destroyed[ship.direction].get_rect(), pygame.BLEND_RGBA_MULT)
        ship.image = tmp
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
    

    pygame.display.flip()

    clock.tick(60)