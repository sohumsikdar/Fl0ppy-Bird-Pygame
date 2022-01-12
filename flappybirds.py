import pygame as pg
import sys
import random

pg.init()
pg.display.set_caption('Flappy Birds')
screen = pg.display.set_mode((288,512))
clock = pg.time.Clock()
game_active = True

bg_surface = pg.image.load('Python/FlappyBird/sprites/background-day.png').convert()
floor_surface_1 = pg.image.load('Python/FlappyBird/sprites/base.png').convert()

floorposition_1 = 0
bird_upflap = pg.image.load('Python/FlappyBird/sprites/bluebird-upflap.png').convert_alpha()
bird_midflap = pg.image.load('Python/FlappyBird/sprites/bluebird-midflap.png').convert_alpha()
bird_downflap = pg.image.load('Python/FlappyBird/sprites/bluebird-downflap.png').convert_alpha()
bird_index = 0
bird_frames = [bird_downflap, bird_midflap, bird_upflap, bird_midflap]
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 250))
bird_movement = 0
gravity = 0.25

pipe_surface = pg.image.load('Python/FlappyBird/sprites/pipe-green.png').convert()
flipped_pipe_surface = pg.transform.flip(pipe_surface, False, True).convert()
height_list = [i for i in range(150, 401, 25)]
pipe_list = []

score = 0
highscore = 0


SPAWNPIPE = pg.USEREVENT
pg.time.set_timer(SPAWNPIPE, 900) 

BIRDFLAP = pg.USEREVENT+1
pg.time.set_timer(BIRDFLAP, 100)


def seemless_floor(floorposition_1):
    if floorposition_1 == -45:
        floorposition_1 = 0
    return floorposition_1


def create_pipe():
    randomY = random.choice(height_list)
    pipe_bottom = pipe_surface.get_rect(midtop = (350, randomY))
    pipe_top = flipped_pipe_surface.get_rect(midbottom = (350, randomY - 125))
    return(pipe_top, pipe_bottom)


def move_pipes(pipe_list):
    for pipe_top, pipe_bottom in pipe_list:  
        pipe_top.right -= 3
        pipe_bottom.right -= 3

    if len(pipe_list) > 10:
        pipe_list.pop(0)
    return pipe_list


def check_collision(pipe_list):
    global game_active
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            game_active = False
        
        if bird_rect.bottom >= 450:
            game_active = False


def rotate_bird(bird_surface):
    new_bird = pg.transform.rotozoom(bird_surface, -bird_movement*6, 1)
    return new_bird 


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

 
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_SPACE:
                if bird_rect.top >= 6:
                    bird_movement = 0
                    bird_movement -= 6
                elif(bird_rect.top > 0):
                    bird_movement -= bird_rect.top

            if not game_active and event.key == pg.K_SPACE:
                pipe_list.clear()
                bird_rect.center = (50, 250)
                bird_movement = 0
                game_active = True

        if event.type == SPAWNPIPE:
            pipe_list.append(create_pipe())

        if event.type == BIRDFLAP:
            bird_index = (1 + bird_index)%4
            bird_surface, bird_rect = bird_animation()

    check_collision(pipe_list)
    
    screen.blit(bg_surface, (0,0))
    
    #bird    
    if game_active == True:    
        bird_movement += gravity
        rotatedbird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotatedbird, bird_rect)

    #pipe
        pipe_list = move_pipes(pipe_list)

    for pipe in pipe_list:
        screen.blit(pipe_surface, pipe[1])
        screen.blit(flipped_pipe_surface, pipe[0])

    #floor  
    if game_active:
        floorposition_1 -= 1.5
    floorposition_1 = seemless_floor(floorposition_1)
    screen.blit((floor_surface_1), (floorposition_1,450))

    pg.display.update()
    clock.tick(120)
