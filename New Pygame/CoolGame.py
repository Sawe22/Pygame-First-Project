

import os #Used to help define path to images used
import pygame

PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
BULLET_VELOCITY = 50
VELOCITY = 30 #Chsnged how fast you wsnt the plsyer to move in pixles per frame
Width, Height = 1200, 700
pygame.display.set_caption("Horses v. Pirates") #This is the caption on the top of the screen
WIN = pygame.display.set_mode((Width, Height)) #Naming conventions has constants in all Caps
HORSE_MONSTER_IMAGE = pygame.image.load(os.path.join("assets", "horse_monster.png" ))
HORSE_MONSTER = pygame.transform.rotate(pygame.transform.scale(HORSE_MONSTER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0) #Sets dimensions to the horse monster image. A 55, 44 version of horse. It is rotated also
PIRATE_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "Pirate_Ship.png" ))
PIRATE_SHIP = pygame.transform.rotate(pygame.transform.scale(PIRATE_SHIP_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0) #Sets dimensions to the horse monster image
BORDER_WIDTH = 10
BORDER = pygame.Rect(0, Height/2 - 5, Width, 10) #Makes a rectangle, start top of screen, middle of screen. Double '//' to ensure it isn't a float, as that causes errors. 
BULLET_WIDTH = 10
BULLET_HEIGHT = 5
MAX_BULLETS = 3
BLUE = 0, 255, 255 #A tuple which will later be used the fill function for the window
BLACK = 0,0,1
GREEN = 0,255,0
RANDOM_COLOR = 0, 23, 43
PIRATE_HIT = pygame.USEREVENT + 1 #These are custom user events, the number is what differentiates the event, give them an id
HORSE_HIT = pygame.USEREVENT + 2
BEACH = pygame.transform.scale(pygame.image.load(os.path.join("assets", "beach.jpeg")), (Width, Height)) 
CANNON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Pingu.webp")), (30, 30)) 
EGG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Egg.jpeg")), (30, 30))


FPS = 60 #This is the game's framerate

def pirate_Movement(keys_pressed, pirate):
        if keys_pressed[pygame.K_a] and pirate.x > 0 :#left key
            pirate.x -= VELOCITY#x value goes down
        if keys_pressed[pygame.K_d] and pirate.x + VELOCITY + pirate.width < Width:#right key. Making sure the velocity subtraction can't place a player off the screen.
            pirate.x += VELOCITY #x value goes up
        if keys_pressed[pygame.K_w] and pirate.y - VELOCITY > BORDER.y:#up key.Making sure the velocity addtion can't place a player off the screen, comparing to borders x position. width is a rectangle property
            pirate.y -= VELOCITY #y value goes down
        if keys_pressed[pygame.K_s] and pirate.y + VELOCITY + pirate.height < Height:#down key. Makes sure ships y position can't go under the screen
            pirate.y += VELOCITY #y value goes up

def horse_Movement(keys_pressed, horse):
        if keys_pressed[pygame.K_LEFT] and horse.x - VELOCITY > 0 :#left key. only allows mivemnent if isn't too close to the right side of the boarder
            horse.x -= VELOCITY#x value goes down
        if keys_pressed[pygame.K_RIGHT] and horse.x + VELOCITY + horse.width < Width:#right key. Making sure the velocity subtraction can't place a player off the width of the screen.
            horse.x += VELOCITY #x value goes up
        if keys_pressed[pygame.K_UP] and horse.y - VELOCITY > 0:#up key.Making sure the velocity addtion can't place a player off the screen, comparing to borders x position. width is a rectangle property
            horse.y -= VELOCITY #y value goes down
        if keys_pressed[pygame.K_DOWN] and horse.y + VELOCITY + horse.height < Height/2:#down key. Makes sure ships y position can't go under the screen
            horse.y += VELOCITY #y value goes up

def handle_bullets(horse_bullets, pirate_bullets, horse, pirate): #Moves bullets, deals with bullet collision and removing bullets in the case of collision
    for bullet in pirate_bullets:
        bullet.y += BULLET_VELOCITY #The rectangle is updated to a position to the left
        if pirate.colliderect(bullet):#In built pygame function, it can check for collision of rectanlge with the coliding entitiy being used as an argument (Only works for 3 rectangles)
            pygame.event.post(pygame.event.Event(PIRATE_HIT)) #POSTS the pirate_hiot event which was defined above, wwhich means that the user was hit
            pirate_bullets.remove(bullet)#Removes the pirate bullet
        elif bullet.y > Height:
            pirate_bullets.remove(bullet)
    for bullet in horse_bullets:
        bullet.y -= BULLET_VELOCITY #The rectangle is updated to a position to the right
        if horse.colliderect(bullet):#In built pygame function, it cazn check for collision of rectanlge with the coliding entitiy being used as an argument (Only works for 3 rectangles)
            pygame.event.post(pygame.event.Event(HORSE_HIT)) #POSTS the horse_hiot event which was defined above, wwhich means that the user was hit
            horse_bullets.remove(bullet)#Removes the horse bullet
            print(bullet.x)
        elif bullet.y < 0:
            horse_bullets.remove(bullet)




def draw_window(horse, pirate, horse_bullets, pirate_bullets): #A function which colours in the window
    #WIN.fill(BLUE) #Fills the window made above with a specified colour. Colours are passed in as RGB, in the form of a Tuple
    WIN.blit(BEACH, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER )#Draws the border rectangle, coloured black as set above, in the window
    WIN.blit(HORSE_MONSTER, (horse.x, horse.y))#blit used when drawing a surface onto the screen, such as image. The second term is the position on screen, Coordinates work like in CS (Top left is 0,0). This take the x and y coordonates of the horse rectangle, which are modified my user input, which moves the horse
    WIN.blit(PIRATE_SHIP, (pirate.x, pirate.y))#blit used when drawing a surface onto the screen, such as image. The second term is the position on screen, Coordinates work like in CS (Top left is 0,0)
    pygame.display.update() #Updates the screen

    for bullet in horse_bullets:
        pygame.draw.rect(WIN, RANDOM_COLOR, bullet )
        WIN.blit(EGG, (bullet.x - 5, bullet.y - 5))

    for bullet in pirate_bullets:
        pygame.draw.rect(WIN, GREEN, bullet )
        WIN.blit(CANNON, (bullet.x, bullet.y))

    pygame.display.update() #Updates the screen

def main():

    horse_bullets = []
    pirate_bullets = []

    horse = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT) #Represents horse player. Arguments are x coordonate, y coordonate, width and height
    pirate = pygame.Rect(400, 400, PLAYER_WIDTH, PLAYER_HEIGHT) #Represents horse player. Arguments are x coordonate, y coordonate, width and height
    clock = pygame.time.Clock()
    run = True
    while run: #Game loop, closes when game ends
        clock.tick(FPS) #Runs this while loop only 60 times per second
        for event in pygame.event.get():

            """Gets a list of all the events which happen in pygame. Events 
             one can check for are if the user quit the window"""

            if event.type == pygame.QUIT: #If the user wants to quit the game. Run becomes false, and the while loop ends. The QUIT event is clicking the X
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(horse_bullets) < MAX_BULLETS:#Bullets can only fire if there's less than max on the screen at once. Bullets on screen is seem=n by the bullets in the list of bullets
                    bullet = pygame.Rect(pirate.x + pirate.width, pirate.y + pirate.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT) #Creates rectangle at potition where one wants to fire from (From x y position of pirateship)
                    horse_bullets.append(bullet)
                if event.key == pygame.K_p and len(pirate_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(horse.x, horse.y + horse.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT) #Creates rectangle at potition where one wants to fire from (From x y position of pirateship). Double // required to ensure a float isn't created
                    pirate_bullets.append(bullet)
            keys_pressed = pygame.key.get_pressed()#tells whats Keys are currently being pressed
            pirate_Movement(keys_pressed, pirate)
            horse_Movement(keys_pressed, horse)
            handle_bullets(horse_bullets, pirate_bullets, horse, pirate)
            draw_window(horse, pirate, horse_bullets, pirate_bullets)


            
 

    pygame.quit()#If while loop ends, the window is closed and the game ends


if __name__ == "__main__": #This is a fail safe for if this python module is imported elsewhere (The functions are just run if the module is imported, so this makes it run only if this specific module is being run)
    main()
