# Corona Invaders
# Written by Emanuele 

import pygame
import random
import math
from pygame import mixer

# Initial setup

pygame.init()
pygame.display.set_caption('Corona Invaders') # title
screen = pygame.display.set_mode((1000, 587)) # Screen
icon = pygame.image.load('mask.png') # Icon
pygame.display.set_icon(icon) # display the icon
bg = pygame.image.load('colosseum.png') # Background imagine
mixer.music.load('retro.wav') # music
mixer.music.play(-1)

#fps
fps = 60 
clock = pygame.time.Clock()

# Game over
end_text = pygame.font.Font('freesansbold.ttf', 50) # Game over text
    
# Making the flag
flag_cord_X = 460 # Flag X coordinate
flag_cord_Y = 510 # Flag Y coordinate
flag_movementX = 0 # Flag movement on X axis
flag_imagine = pygame.image.load('italy.png').convert_alpha() # Flag picture

# Making the syringe(bullet)
syringe_cord_X = 0 # syringe X coordinate
syringe_cord_Y = 510 # Syringe X coordinate
syringe_loaded = 0 # If 0 the syringe is not loaded
syringe_imagine = pygame.image.load('vaccine.png').convert_alpha() # syringe picture

# Making Coronavirus
virus = 6 # Number of enemies
virus_cord_X = [] # # Corona X coordinate
virus_cord_Y = [] # Corona Y coordinate
virus_movement_X = [] # Corona movement on X axis
virus_movement_Y = [] # Corona movement on Y axis
corona_imagine = [] # Corona picture
for x in range(virus):
    corona_imagine.append(pygame.image.load('coronavirus.png'))
    virus_cord_X.append(random.randint(0, 1000))
    virus_cord_Y.append(random.randint(20, 100))
    virus_movement_X.append(4)
    virus_movement_Y.append(20)

# Keeping count of destroyed enemies
counter = 0
counter_X = 830
counter_Y = 550
score = pygame.font.Font('freesansbold.ttf', 25)

# Display the flag
def flag(Xcordinate, Ycordinate):
    
    screen.blit(flag_imagine, (Xcordinate, Ycordinate))

# Fire the syringe
def syringe(Xcordinate, Ycordinate):
    global syringe_loaded
    syringe_loaded = 1 # syringe loaded
    screen.blit(syringe_imagine, (Xcordinate + 15, Ycordinate + 10)) # the syringe will be shot from the center of the flag 

def strike(virus_cord_X, virus_cord_Y, syringe_cord_X, syringe_cord_Y):
    two_points_distance = math.sqrt(math.pow(virus_cord_X - syringe_cord_X, 2) + (math.pow(virus_cord_Y - syringe_cord_Y, 2))) # Checking for collision
    if two_points_distance < 26:
        return True
    else:
        return False

def game_over():
    text = end_text.render('GAME OVER!', True, (255, 255, 255)) # Display the game over text
    screen.blit(text, (340, 260))

# Showing the score
def destroyed(Xcordinate, Ycordinate):
    destroyed = score.render(f'destroyed: {str(counter)}', True, (255, 255, 255))
    screen.blit(destroyed, (Xcordinate, Ycordinate))    
        
# Display the corona    
def corona(Xcordinate, Ycordinate, x):
    screen.blit(corona_imagine[x], (Xcordinate, Ycordinate))    

# Coronavirus movements
def corona_movement():
    global syringe_cord_Y, syringe_loaded, virus_movement_X
    global counter
         
    for x in range(virus):
        virus_cord_X[x] += virus_movement_X[x]
        
        # If Corona touches you, you lose 
        if virus_cord_Y[x] > 465:
            for y in range(virus):
                virus_cord_Y[y] = 1500
            game_over()
            break   
            
        # Corona boundaries     
        if virus_cord_X[x] <= 0:
            virus_movement_X[x] = 5
            virus_cord_Y[x] += virus_movement_Y[x] 
        elif virus_cord_X[x] >= 936:
            virus_movement_X[x] = -5    
            virus_cord_Y[x] += virus_movement_Y[x]
                
        making_strike = strike(virus_cord_X[x], virus_cord_Y[x], syringe_cord_X, syringe_cord_Y)
        if making_strike:
            
            # If the strike occurs the virus spawns randomly on the screen
            syringe_cord_Y = 510
            syringe_loaded = 0
            virus_cord_X[x] = random.randint(0, 936)
            virus_cord_Y[x] = random.randint(20, 100)
            counter += 1
            hit = mixer.Sound('bip.wav')
            hit.play()
            
            corona(virus_cord_X[x], virus_cord_Y[x], x)
            
        corona(virus_cord_X[x], virus_cord_Y[x], x)    
        
# Boundaries    
def boundaries(): 
    global flag_cord_X
    
    if flag_cord_X < 0:
        flag_cord_X = 0
    elif flag_cord_X >= 936:
        flag_cord_X = 936       
   
# The game function does contain the flag and corona movements
def game():    
    start = True 
    global syringe_cord_X, syringe_cord_Y, syringe_loaded
    global flag_cord_X, flag_cord_Y, flag_movementX 
    while start:

        screen.fill((255, 255, 255))
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
        if pressed[pygame.K_RIGHT]:
            flag_cord_X += 3
        if pressed[pygame.K_LEFT]:
            flag_cord_X -= 3      
        if pressed[pygame.K_SPACE]:
            if syringe_loaded == 0:
                syringe_cord_X = flag_cord_X    
                syringe(flag_cord_X, syringe_cord_Y)
                syringe_shot = mixer.Sound('laser.wav')
                syringe_shot.play()

        if syringe_cord_Y <= 0:
            syringe_cord_Y = flag_cord_Y
            syringe_loaded = 0
        elif syringe_loaded == 1:
            syringe(syringe_cord_X, syringe_cord_Y)
            syringe_cord_Y -= 9            


        flag(flag_cord_X, flag_cord_Y)
        corona_movement()
        boundaries()
        destroyed(counter_X, counter_Y)
        pygame.display.update()   
        
        if __name__ == '__main__':
            game()
    
