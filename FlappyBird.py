import pygame, sys
from datetime import datetime


def moving_floor():
    screen.blit(floor, (floor_position, 900))
    screen.blit(floor, (floor_position + 576, 900))


pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

# background
date = datetime.now()
if date.hour < 20:
    background = pygame.image.load('assets/background-day.png').convert()
    background = pygame.transform.scale2x(background)
else:
    background = pygame.image.load('assets/background-night.png').convert()
    background = pygame.transform.scale2x(background)

# floor
floor = pygame.image.load('assets/base.png').convert()
floor = pygame.transform.scale2x(floor)
floor_position = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    pygame.display.update()
    clock.tick(120)