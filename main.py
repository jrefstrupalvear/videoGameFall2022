# Pong Video Game Project
# content from kids can code: http://kidscancode.org/blog/

# sources: Dad - helped figure out how things should bounce of walls
# Andrew Perevoztchikov helped me with player friction and with figuring out why my collision were not working (adding each thing to a group)
# everything else is from class notes which we got from kidscancode.org

#  design
'''
Innovation:
innovating from player and mob classes to make pong, with simple math and feeback

Goals: First to 5 wins 
Rules: the ball bounces around with increasing speed, the goal is to get it past the other player
Feedback: when the ball bounces of the other player's wall you get a point
Freedom!!!: Movement!

'''

# import libraries and modules
# from platform import platform

import pygame as pg

from pygame.sprite import Sprite


vec = pg.math.Vector2


# game settings 
WIDTH = 1440
HEIGHT = 720
FPS = 60


# player settings
PLAYER_FRIC = 0.1
SCORE = 0
SCORE2 = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# creating our draw text function, alowing us to customize the text, size,color and position
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)


# sprites...
class Player(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        #dimensions, color, and position (position can be changed when class is instansiated) of the sprite
        self.image = pg.Surface((100, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(x, y)
        # initial velocity and acceleration
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        #defining movement controls
    def controls(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_a]:
            self.acc.x = -2.5
        
        if keys[pg.K_d]:
            self.acc.x = 2.5
    #defining the controls for movement
    def update(self): 
        self.acc = vec(0,0)
        self.controls()
        # friction- the acc of x is the velocity times -0.3and the acc of y is the velocity times -0.1
        self.acc.x += self.vel.x * -0.3
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        #acceleration
        self.pos += self.vel+0.5 * self.acc
      #   the middle of the bottom of the rectangle is where is position is constantly updated from
        self.rect.midbottom = self.pos
        #
      

#exact same class as before just with different controls

class Player2(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        #dimensions, color, and position (position can be changed when class is instansiated) of the sprite
        self.image = pg.Surface((100, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(x, y)
        #inital velocity and acceleration
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    #defining the controls for movement
    def controls(self):
        keys = pg.key.get_pressed()
     
        if keys[pg.K_LEFT]:
            self.acc.x = -2.5
       
        if keys[pg.K_RIGHT]:
            self.acc.x = 2.5
        
#andrew helped me with the friction
    def update(self): 
        self.acc = vec(0,0)
        self.controls()
        # friction - the acc of x is the velocity times -0.3and the acc of y is the velocity times -0.1
        self.acc.x += self.vel.x * -0.3
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
       # the middle of the bottom of the rectangle is where is position is constantly updated from
        self.rect.midbottom = self.pos
        #accleration 
        self.pos += self.vel+0.5 * self.acc

# platforms

# defining the ball class
class Ball(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        #dimensions, color, velocity
        self.image = pg.Surface((50,50))
        
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2
        self.y_vel = -4
        self.x_vel = 2
        
    def update(self):
        #everytime the window updates, which in this case in 60 times a second, the rectangle's x
        #position will increase by the previously defined x and y velocity
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
      # checks to see if the ball is off the screen to the right or left and bounches it off
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1
        

# init pygame and create a window
pg.init()
pg.mixer.init()
#using the previously defined width and height variables as dimensions for the screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
#name of the game in the window
pg.display.set_caption("PONG")
clock = pg.time.Clock()
  
# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
player_1 =pg.sprite.Group()
player_2 = pg.sprite.Group()

# instantiate classes
player = Player(WIDTH/2,HEIGHT-2)
player2 = Player2(WIDTH/2,30)
ball = Ball()

player_1.add(player)
player_2.add(player2)



    # print(m)

# add players and the ball to all sprites group
all_sprites.add(player)
all_sprites.add(ball)
all_sprites.add(player2)
all_sprites.add (player_1,player_2)

# Game loop
running = True
game_over = True
while running:
    
    # keep the loop running using clock
    clock.tick(FPS)

   
    #if the ball collides with either player then the x velocity will increase by 1.0099
    # and the y velocity will increase by 1.00099 and will flip
    if pg.sprite.spritecollide(ball,player_1,False) or pg.sprite.spritecollide(ball,player_2,False):
        ball.x_vel =  ball.x_vel *1.0099
        ball.y_vel = - ball.y_vel *1.00099
        
    #if the ball gets past a player the it will rebound and add a point to the player who hit it and set the velocity to 4
    if ball.rect.y <= 0:
        SCORE += 1
        ball.y_vel = 4       

    if ball.rect.y >= HEIGHT:
        SCORE2 += 1
        ball.y_vel = -4       


    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
       
        
        
    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # draw the background screen
  
    screen.fill(BLACK)

    # draw text

#instructions at the beggining of the game
    if SCORE ==0 and SCORE2 == 0:
        draw_text("Welcome to Two Player Pong! First to 5 Wins! Arrows and WASD to Move", 48, WHITE, WIDTH / 2, HEIGHT /2)
    # the game is first to five so for whoever wins it prints that they win in the midde of the screen
    # it also resets the ball and hides it from view (by making it black)
    if SCORE == 5:
        ball.rect.x = WIDTH/2 -40
        ball.rect.y = HEIGHT/2- 40
        ball.y_vel = 0
        ball.x_vel =0
        ball.image.fill(BLACK)
        draw_text("Game Over: Player 1 Wins", 48, RED, WIDTH / 2, HEIGHT /2)
    if SCORE2 == 5:
        ball.rect.x = WIDTH/2 -40
        ball.rect.y = HEIGHT/2 -40
        ball.y_vel = 0
        ball.x_vel =0
        ball.image.fill(BLACK)

      
        draw_text("Game Over: Player 2 Wins", 48, RED, WIDTH / 2, HEIGHT /2)
    #displays the points and objective during the game
    draw_text("PLAYER1: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    draw_text("PLAYER 2: " + str(SCORE2), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    

    # draws all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()
