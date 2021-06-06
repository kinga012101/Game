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
    new_bird = pygame.transform.rotozoom(bird,-bird_movement *  3, 1)
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

def collision(pipes):
    global achieve
    for i in pipes:
        if bird_rectangle.colliderect(i):
            dead.play()
            achieve = True 
            return False

    if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 450:
        achieve = True
        return False

    return True

def score_display(status):
    if status == 'start':
        score_surface = subtitles.render(str(int(score)), True, (255,255,255))
        score_rectangle = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rectangle)
    if status == 'end':
        score_surface = subtitles.render(f'Score:{(int(score))}', True, (255,255,255))
        score_rectangle = score_surface.get_rect(center = (144,100))
       # score.blit(score_surface,score_rectangle)
        high_score_surface = subtitles.render(f'High score:{int(high_score)}', True, (255,255,255))
        high_score_rectangle = high_score_surface.get_rect(center = (144, 400))
        screen.blit(high_score_surface,high_score_rectangle)

def update(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def check():
    global score, achieve
    if pipes :
        for i in pipes:
            if 45 < i.centerx <55 and achieve:
                score += 1
                point.play()
                achieve = False
            if i.centerx < 0:
                achieve = False


pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
subtitles = pygame.font.Font('04B_19.TTF',20)

gravity = 0.12
bird_movement = 0
game_on = True
achieve = True
score = 0
high_score = 0

# Sounds
flap = pygame.mixer.Sound('sounds/sound_sfx_wing.wav')
point = pygame.mixer.Sound('sounds/sound_sfx_point.wav')
dead = pygame.mixer.Sound('sounds/sound_sfx_hit.wav')

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

FLAP = pygame.USEREVENT
pygame.time.set_timer(FLAP, 150)

# pipes 
if date.hour < 20 :
    pip_surface = pygame.image.load('assets/pipe-green.png').convert()
else:
    pip_surface = pygame.image.load('assets/pipe-red.png').convert()
pipes = []
SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN, 1000)
pipe_height = [200,300,400]
space_between = [150,100,125]

# game over
game_over = pygame.image.load('assets/message.png').convert_alpha()
game_over_rectangle = game_over.get_rect(center = (144,256))

# Points
SCORE = pygame.USEREVENT + 2
pygame.time.set_timer(SCORE,100)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_on:
                bird_movement = 0 
                bird_movement -= 5
                flap.play()
            if event.key == pygame.K_SPACE and game_on == False:
                    game_on = True
                    pipes.clear()
                    bird_rectangle.center = (50,256)
                    bird_movement = 0
                    score = 0

        if event.type == SPAWN:
            pipes.extend(cretation())

        if event.type == FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rectangle  = bird_animation()
        

    screen.blit(background, (0, 0))

    if game_on:
        # Bird
        bird_movement += gravity
        rotated_bird = rotation(bird_surface)
        bird_rectangle.centery += bird_movement
        screen.blit(rotated_bird, bird_rectangle)
        game_on = collision(pipes)

        # Pipes 
        pipes = moving_pipes(pipes)
        showing_pipes(pipes)

        # Score
        check()
        score_display('start')

    else:
        screen.blit(game_over,game_over_rectangle)
        high_score = update(score,high_score)
        score_display('end')


    # Floor
    floor_position -= 1
    moving_floor()
    if floor_position <= -288:
        floor_position = 0

    pygame.display.update()
    clock.tick(120)
