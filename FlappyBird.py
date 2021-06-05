import pygame, sys
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



pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

gravity = 0.15
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

#bird
bird_downflap = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_moves = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_moves[bird_index]
bird_rectangle = bird_surface.get_rect(center = (50,256))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    if game_on:
        # Bird
        bird_movement += gravity
        rotated_bird = rotation(bird_surface)
        bird_rectangle.centery += bird_movement
        screen.blit(rotated_bird, bird_rectangle)

    # Floor
    floor_position -= 1
    moving_floor()
    if floor_position <= -288:
        floor_position = 0

    pygame.display.update()
    clock.tick(120)
    