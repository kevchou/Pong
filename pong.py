"""
Simple pong game created in python using pygame.

Press N for a new game.

Player1: 
    W - move up
    S - move down
    
Player2:
    UP - move up
    DOWN - move down
"""


# import modules
import random
import pygame

# some resource related warnings
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# initializations
pygame.init()

# Constants
WHITE = pygame.Color(255, 255, 255)
FONT  = pygame.font.Font(pygame.font.match_font('timesnewroman'), 32)

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2


# Initial paddle position / velocity
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2

paddle1_vel = 0
paddle2_vel = 0

# Initial ball position and velocity
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]

# Scores
score1 = 0
score2 = 0


# a bit similar to CodeSkulptor frame creation -- we'll call the window the canvas
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")



def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    
    score1 = 0
    score2 = 0
    
    right = random.randint(0,1)
    ball_init(right)

def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    if right:
        balldir = 1
    else:
        balldir = -1
        
    ball_vel = [balldir*random.randrange(120,240)/60, -1*random.randrange(60,180)/60]


def draw_handler(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
 
   # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel > HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel < HEIGHT-HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel 
    if paddle2_pos + paddle2_vel > HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel < HEIGHT-HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel 
    

    
    # Fills background as black
    c.fill((0, 0, 0))
    
    # Mid line and gutters
    pygame.draw.line(c, WHITE, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(c, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(c, WHITE, [WIDTH - PAD_WIDTH, 0], 
                     [WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(c, WHITE, [WIDTH / 2, HEIGHT/2], 75, 1)
     
     
    # Draws the paddles 
    pygame.draw.polygon(c, WHITE, 
                        [(0, paddle1_pos-HALF_PAD_HEIGHT), 
                         (PAD_WIDTH, paddle1_pos-HALF_PAD_HEIGHT),
                         (PAD_WIDTH, paddle1_pos+HALF_PAD_HEIGHT), 
                         (0, paddle1_pos+HALF_PAD_HEIGHT)], 
                         0)
                    
    pygame.draw.polygon(c, WHITE,
                        [(WIDTH-PAD_WIDTH, paddle2_pos-HALF_PAD_HEIGHT),
                         (WIDTH, paddle2_pos-HALF_PAD_HEIGHT),
                         (WIDTH, paddle2_pos+HALF_PAD_HEIGHT), 
                         (WIDTH-PAD_WIDTH, paddle2_pos+HALF_PAD_HEIGHT)], 
                        0)

    
    # ball bounces off top and bottom
    if ball_pos[1] > HEIGHT - BALL_RADIUS or ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
            
    # ball touches either gutter or paddles
    if ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] < paddle1_pos+HALF_PAD_HEIGHT and ball_pos[1] > paddle1_pos-HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            ball_init(1)
            score2 += 1
        
    if ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] < paddle2_pos+HALF_PAD_HEIGHT and ball_pos[1] > paddle2_pos-HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            ball_init(0)
            score1 += 1
            

    #update scores
    label1 = FONT.render(str(score1), 1, WHITE)
    canvas.blit(label1, (WIDTH/4, 20))
 
    label2 = FONT.render(str(score2), 1, WHITE)
    canvas.blit(label2, (WIDTH * 3/4, 20))  
    
    # update ball position
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])
    
    # Draws ball
    pygame.draw.circle(c, WHITE, ball_pos, BALL_RADIUS, 0) 
    
    # update the display
    pygame.display.update()


  
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    acc = 5
    
    if event.key == K_w:
        paddle1_vel -= acc
    elif event.key == K_s:
        paddle1_vel += acc
        
    if event.key == K_UP:
        paddle2_vel -= acc
    elif event.key == K_DOWN:
        paddle2_vel += acc
        
    if event.key == K_n:
        new_game()
    
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    acc = 5
    
    if event.key == K_w:
        paddle1_vel += acc
    elif event.key == K_s:
        paddle1_vel -= acc
        
    if event.key == K_UP:
        paddle2_vel += acc
    elif event.key == K_DOWN:
        paddle2_vel -= acc
    

# Method to start the game
def main():
    
    new_game()
    # initialize loop until quit variable
    running = True
    clock = pygame.time.Clock()
        
    # doing the infinte loop until quit -- the game is running
    while running:
        
        # Call draw handler. Call it 60 times per second
        draw_handler(canvas)
        
        for event in pygame.event.get():
            
            # Quits game when Window is closed
            if event.type == pygame.QUIT:
                running = False

            # Input events
            elif event.type == KEYDOWN:
                keydown(event)
            
            elif event.type == KEYUP:
                keyup(event)
                

        # Sets FPS to 60
        clock.tick(60)
        
    # Quits game
    pygame.quit()

if __name__ == '__main__': 
    main() 
