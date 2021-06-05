import pygame, sys, random 
from datetime import datetime


def moving_floor():
    screen.blit(floor, (floor_position, 450))
    screen.blit(floor, (floor_position + 288, 450))

def bird_animation():
    new_bird = bird_moves[bird_index]
    new_bird_rectagle = new_bird.get_rect(center= (50, bird_rectangle.centery))
    return new_bird, new_bird_rectagle

def rotation(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*2, 1)
    return new_bird

def cretation():
    position= random.choice(pipe_height)
    space = random.choice(space_between)
    bottom_pipe = pip_surface.get_rect(midtop = (300,position))
    top_pipe = pip_surface.get_rect(midbottom = (300, position - space))
    return bottom_pipe, top_pipe

def showing_pipes(pipes):
    for i in pipes:
        if i.bottom >= 512:
            screen.blit(pip_surface,i)
        else:
            flip = pygame.transform.flip(pip_surface, False, True)
            screen.blit(flip,i)

def moving_pipes(pipes):
    for i in pipes: 
        i.centerx -= 2
    current_pipes = [i for i in pipes if i.right >= -50]
    return current_pipes




pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

gravity = 0.1
bird_movement = 0
game_on = True

# background
date = datetime.now()
if date.hour < 20:
    background = pygame.image.load('assets/background-day.png').convert()
else:
    background = pygame.image.load('assets/background-night.png').convert()

# floor
floor = pygame.image.load('assets/base.png').convert()
floor_position = 0

# bird
bird_downflap = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_moves = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_moves[bird_index]
bird_rectangle = bird_surface.get_rect(center = (50,256))

# pipes 
if date.hour < 20 :
    pip_surface = pygame.image.load('assets/pipe-green.png').convert()
else:
    pip_surface = pygame.image.load('assets/pipe-red.png').convert()
pipes = []
SPAWN = pygame.USEREVENT
pygame.time.set_timer(SPAWN, 1000)
pipe_height = [200,300,400]
space_between = [150,100,125]



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWN:
            pipes.extend(cretation())

    screen.blit(background, (0, 0))

    if game_on:
        # Bird
        bird_movement += gravity
        rotated_bird = rotation(bird_surface)
        bird_rectangle.centery += bird_movement
        screen.blit(rotated_bird, bird_rectangle)

        # Pipes 
        pipes = moving_pipes(pipes)
        showing_pipes(pipes)


    # Floor
    floor_position -= 1
    moving_floor()
    if floor_position <= -288:
        floor_position = 0

    pygame.display.update()
    clock.tick(120)
