#! /usr/bin/python

import pygame
from pygame.locals import *
import os
import random
import time as Time

filedir = 'data'

def load_image(filename):
    filepath = os.path.join(filedir, filename)
    image = pygame.image.load(filepath).convert_alpha()
    image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
    return image

def offset(offs, map_length):
    return offs / 3378.0 * map_length

def color_surface(surface, red, green, blue):
    array = pygame.surfarray.pixels3d(surface)
    array[:,:,0] = red
    array[:,:,1] = green
    array[:,:,2] = blue

def main():
    clock = pygame.time.Clock()
    pygame.init()
    window = pygame.display.set_mode((640, 480))

    images = []
    background = load_image('background-2.png')
    platform_top = load_image('platform-top.png')
    platform_brick = load_image('platform-brick.png')
    platform_q = [load_image('platform-q1.png'), load_image('platform-q2.png'), 
                       load_image('platform-q3.png')]
    platform_air = load_image('platform-air.png')
    platform_blue3 = load_image('platform-blue3.png')
    player = [load_image('mario1.png'), load_image('mario2.png'), load_image('mario3.png'),
                  load_image('mario4.png'), load_image('mario5.png'), load_image('mariodie.png')]
    fplayer = [pygame.transform.flip(p, 1, 0) for p in player]
    slub = [load_image('slub1.png'), load_image('slub2.png'), load_image('slub3.png')]
    mushroom = load_image('mushroom-green.png')
    hill = load_image('hill.png')
    hill2 = load_image('hill2.png')
    bush1 = load_image('bush-1.png')
    bush2 = load_image('bush-2.png')
    bush3 = load_image('bush-3.png')
    pipe_green = load_image('pipe_green.png')
    pipe_greenbig = load_image('pipe_greenbig.png')
    clouds = load_image('cloud.png')
    dobbelclouds = load_image('dobbelclouds.png')
    coin = [load_image('coin1.png'), load_image('coin2.png'), load_image('coin3.png'),
                load_image('coin4.png')]

    map_length = platform_top.get_width() * 211

    ground_height = window.get_height()-2*platform_top.get_height()
    count = 0
    px = 0
    py = ground_height-player[0].get_height()
    speed = 140
    cplayer = player[0]
    bias = 0
    up = 0
    down = 0
    jump_speed = 0
    ja = 0
    jump = 0
    dtime = 0
    ctime = 0
    key_up = 0
    first_added = 0
    pipe1x = offset(448, map_length)
    slub1_x = offset(348, map_length)
    slub1_y = ground_height-slub[0].get_height()
    slub1_speed = 2

    slub1_r = slub[0].get_rect(topleft=(slub1_x, slub1_y))
    cslub1 = slub[0]
    slub1_killed = 0
    slub1_dead = 0
    scnt = 0
    player_killed = 0
    player_dead = 0
    pcnt = 0

    rects = []

    player_r = player[0].get_rect(topleft=(px,py))
    pipe1_r = pipe_greenbig.get_rect(topleft=
                  (offset(448, map_length),ground_height-pipe_greenbig.get_height()/2.0))
    pipe2_r = pipe_greenbig.get_rect(topleft=
                  (offset(609, map_length),ground_height-pipe_green.get_height()))
    pipe3_r = pipe_greenbig.get_rect(topleft=
                  (offset(737, map_length),ground_height-pipe_greenbig.get_height()))
    pipe4_r = pipe_greenbig.get_rect(topleft=
                  (offset(912, map_length),ground_height-pipe_greenbig.get_height()))
    pipe5_r = pipe_greenbig.get_rect(topleft=
                  (offset(2608, map_length),ground_height-pipe_greenbig.get_height()/2.0))
    pipe6_r = pipe_greenbig.get_rect(topleft=
                  (offset(2864, map_length),ground_height-pipe_greenbig.get_height()/2.0))
    pform1_r = platform_q[0].get_rect(topleft=
                  (offset(257, map_length),ground_height-pipe_greenbig.get_height()))
    pform2_r = platform_q[0].get_rect(topleft=
                  (offset(320, map_length),ground_height-pipe_greenbig.get_height()))
    pform3_r = platform_q[0].get_rect(topleft=
                  (offset(320, map_length)+platform_q[0].get_width(),ground_height-pipe_greenbig.get_height()))
    pform4_r = platform_q[0].get_rect(topleft=
                  (offset(320, map_length)+platform_q[0].get_width()*2,ground_height-pipe_greenbig.get_height()))
    pform5_r = platform_q[0].get_rect(topleft=
                  (offset(320, map_length)+platform_q[0].get_width()*3,ground_height-pipe_greenbig.get_height()))
    pform6_r = platform_q[0].get_rect(topleft=
                  (offset(320, map_length)+platform_q[0].get_width()*4,ground_height-pipe_greenbig.get_height()))
    pftops = []
    x_offs = 0
    for i in range(69):
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-platform_top.get_height())))       
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-2*platform_top.get_height())))
        x_offs += platform_top.get_width()
    x_offs += platform_top.get_width() * 2
    for i in range(15):
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-platform_top.get_height())))       
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-2*platform_top.get_height())))
        x_offs += platform_top.get_width()
    x_offs += platform_top.get_width() * 3
    for i in range(64):
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-platform_top.get_height())))       
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-2*platform_top.get_height())))
        x_offs += platform_top.get_width()
    x_offs += platform_top.get_width() * 2
    for i in range(56):
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-platform_top.get_height())))       
        pftops.append(platform_top.get_rect(topleft=(x_offs,window.get_height()-2*platform_top.get_height())))
        x_offs += platform_top.get_width()

    slub1_r = slub[0].get_rect(topleft=((offset(348, map_length),ground_height-slub[0].get_height())))

    x_offs = platform_top.get_width() * 77
    for i in range(3):
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))
        x_offs += platform_top.get_width()

    for i in range(8):
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height()*2)))
        x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 3
    for i in range(3):
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height()*2)))
        x_offs += platform_top.get_width()

    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height()*2)))
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))

    x_offs += platform_top.get_width() * 6
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))
    x_offs += platform_top.get_width()
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))
    x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 4
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))
    x_offs += platform_top.get_width() * 3
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height()*2)))
    x_offs += platform_top.get_width() * 3
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))

    x_offs += platform_top.get_width() * 6
    rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))

    x_offs += platform_top.get_width() * 3
    for i in range(3):
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height()*2)))
        x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 4
    for i in range(4):
        if i == 1 or i == 2:
            rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height()*2)))
        x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 2
    for i in range(4):
        for j in range(i+1):
            rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-platform_q[0].get_height()*(j+1))))
        x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 2
    for i in range(4):
        for j in range(4-i):
            rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-platform_q[0].get_height()*(j+1))))
        x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 4
    for i in range(4):
        for j in range(i+1):
            rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-platform_q[0].get_height()*(j+1))))
        x_offs += platform_top.get_width()
    for i in range(4):
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-platform_q[0].get_height()*(i+1))))
    x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 2
    for i in range(4):
        for j in range(4-i):
            rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-platform_q[0].get_height()*(j+1))))
        x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 9
    for i in range(4):
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-pipe_greenbig.get_height())))
        x_offs += platform_top.get_width()

    x_offs += platform_top.get_width() * 9
    for i in range(8):
        for j in range(i+1):
            rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-platform_q[0].get_height()*(j+1))))
        x_offs += platform_top.get_width()
    for i in range(8):
        rects.append(platform_q[0].get_rect(topleft=(x_offs,ground_height-platform_q[0].get_height()*(i+1))))
    x_offs += platform_top.get_width()

    rects.append(pipe1_r)
    rects.append(pipe2_r)
    rects.append(pipe3_r)
    rects.append(pipe4_r)
    rects.append(pipe5_r)
    rects.append(pipe6_r)
    rects.append(pform1_r)
    rects.append(pform2_r)
    rects.append(pform3_r)
    rects.append(pform4_r)
    rects.append(pform5_r)
    rects.append(pform6_r)
    rects.extend(pftops)

    xxx = 0
    while True:
        xxx += 1
        dx = dy = 0
        window.blit(background, (0, 0))

        window.blit(pipe_green, (bias+offset(609, map_length), ground_height-pipe_green.get_height()))
        window.blit(pipe_greenbig, (bias+offset(737, map_length),
                           ground_height-pipe_greenbig.get_height()))
        window.blit(pipe_greenbig, (bias+offset(912, map_length),
                           ground_height-pipe_greenbig.get_height()))
        window.blit(pipe_greenbig, (bias+offset(448, map_length),
                           ground_height-pipe_greenbig.get_height()/2.0))
        window.blit(pipe_greenbig, (bias+offset(2608, map_length),
                           ground_height-pipe_greenbig.get_height()/2.0))
        window.blit(pipe_greenbig, (bias+offset(2864, map_length),
                           ground_height-pipe_greenbig.get_height()/2.0))

        x_offs = 0
        for i in range(69):
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-platform_top.get_height()))
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-2*platform_top.get_height()))            
            x_offs += platform_top.get_width()
        x_offs += platform_top.get_width() * 2
        for i in range(15):
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-platform_top.get_height()))
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-2*platform_top.get_height()))            
            x_offs += platform_top.get_width()
        x_offs += platform_top.get_width() * 3
        for i in range(64):
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-platform_top.get_height()))
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-2*platform_top.get_height()))            
            x_offs += platform_top.get_width()
        x_offs += platform_top.get_width() * 2
        for i in range(56):
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-platform_top.get_height()))
            window.blit(platform_top, (bias+x_offs,
                                       window.get_height()-2*platform_top.get_height()))            
            x_offs += platform_top.get_width()

        window.blit(hill, (bias+0, ground_height-hill.get_height()))
        window.blit(hill, (bias+offset(768, map_length), ground_height-hill.get_height()))
        window.blit(hill, (bias+offset(1535, map_length), ground_height-hill.get_height()))
        window.blit(hill, (bias+offset(2305, map_length), ground_height-hill.get_height()))
        window.blit(hill, (bias+offset(3073, map_length), ground_height-hill.get_height()))

        window.blit(hill2, (bias+offset(257, map_length), ground_height-hill2.get_height()))
        window.blit(hill2, (bias+offset(1024, map_length), ground_height-hill2.get_height()))
        window.blit(hill2, (bias+offset(1793, map_length), ground_height-hill2.get_height()))
        window.blit(hill2, (bias+offset(2560, map_length), ground_height-hill2.get_height()))
        window.blit(hill2, (bias+offset(3328, map_length), ground_height-hill2.get_height()))

        window.blit(bush1, (bias+offset(184, map_length), ground_height-bush1.get_height()))
        window.blit(bush1, (bias+offset(952, map_length), ground_height-bush1.get_height()))
        window.blit(bush1, (bias+offset(1721, map_length), ground_height-bush1.get_height()))

        window.blit(bush2, (bias+offset(665, map_length), ground_height-bush2.get_height()))
        window.blit(bush2, (bias+offset(1432, map_length), ground_height-bush2.get_height()))
        window.blit(bush2, (bias+offset(2203, map_length), ground_height-bush2.get_height()))

        window.blit(bush3, (bias+offset(376, map_length), ground_height-bush3.get_height()))
        window.blit(bush3, (bias+offset(1144, map_length), ground_height-bush3.get_height()))
        window.blit(bush3, (bias+offset(1913, map_length), ground_height-bush3.get_height()))
        window.blit(bush3, (bias+offset(2522, map_length), ground_height-bush3.get_height()))
        window.blit(bush3, (bias+offset(2681, map_length), ground_height-bush3.get_height()))
        window.blit(bush3, (bias+offset(3208, map_length), ground_height-bush3.get_height()))

        window.blit(platform_q[0], (bias+offset(257, map_length), ground_height-pipe_greenbig.get_height()))
        x_offs = 0
        for i in range(5):
            if i % 2:
                platform_basic = platform_q[0]
            else:
                platform_basic = platform_brick
            window.blit(platform_basic, (bias+offset(320, map_length)+x_offs, ground_height-pipe_greenbig.get_height()))
            x_offs += platform_basic.get_width()

        x_offs = platform_top.get_width() * 77
        for i in range(3):
            if i == 1:
                platform_basic = platform_q[0]
            else:
                platform_basic = platform_brick
            window.blit(platform_basic, (bias+x_offs,ground_height-pipe_greenbig.get_height()))
            x_offs += platform_basic.get_width()

        for i in range(8):
            window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()*2))
            x_offs += platform_basic.get_width()

        x_offs += platform_top.get_width() * 3
        for i in range(3):
            window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()*2))
            x_offs += platform_basic.get_width()

        window.blit(platform_q[0], (bias+x_offs,ground_height-pipe_greenbig.get_height()*2))
        window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()))

        x_offs += platform_top.get_width() * 6
        window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()))
        x_offs += platform_top.get_width()
        window.blit(platform_air, (bias+x_offs,ground_height-pipe_greenbig.get_height()))
        x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 4
        window.blit(platform_q[0], (bias+x_offs,ground_height-pipe_greenbig.get_height()))
        x_offs += platform_top.get_width() * 3
        window.blit(platform_q[0], (bias+x_offs,ground_height-pipe_greenbig.get_height()))
        window.blit(platform_q[0], (bias+x_offs,ground_height-pipe_greenbig.get_height()*2))
        x_offs += platform_top.get_width() * 3
        window.blit(platform_q[0], (bias+x_offs,ground_height-pipe_greenbig.get_height()))

        x_offs += platform_top.get_width() * 6
        window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()))

        x_offs += platform_top.get_width() * 3
        for i in range(3):
            window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()*2))
            x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 4
        for i in range(4):
            if i == 1 or i == 2:
                window.blit(platform_q[0], (bias+x_offs,ground_height-pipe_greenbig.get_height()*2))
                window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()))
            else:
                window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()*2))
            x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 2
        for i in range(4):
            for j in range(i+1):
                window.blit(platform_blue3, (bias+x_offs,ground_height-platform_q[0].get_height()*(j+1)))
            x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 2
        for i in range(4):
            for j in range(4-i):
                window.blit(platform_blue3, (bias+x_offs,ground_height-platform_q[0].get_height()*(j+1)))
            x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 4
        for i in range(4):
            for j in range(i+1):
                window.blit(platform_blue3, (bias+x_offs,ground_height-platform_q[0].get_height()*(j+1)))
            x_offs += platform_top.get_width()
        for i in range(4):
            window.blit(platform_blue3, (bias+x_offs,ground_height-platform_q[0].get_height()*(i+1)))
        x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 2
        for i in range(4):
            for j in range(4-i):
                window.blit(platform_blue3, (bias+x_offs,ground_height-platform_q[0].get_height()*(j+1)))
            x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 9
        for i in range(4):
            if i == 2:
                window.blit(platform_q[0], (bias+x_offs,ground_height-pipe_greenbig.get_height()))
            else:
                window.blit(platform_brick, (bias+x_offs,ground_height-pipe_greenbig.get_height()))
            x_offs += platform_top.get_width()

        x_offs += platform_top.get_width() * 9
        for i in range(8):
            for j in range(i+1):
                window.blit(platform_blue3, (bias+x_offs,ground_height-platform_q[0].get_height()*(j+1)))
            x_offs += platform_top.get_width()
        for i in range(8):
            window.blit(platform_blue3, (bias+x_offs,ground_height-platform_q[0].get_height()*(i+1)))
        x_offs += platform_top.get_width()

        if slub1_killed:
            if scnt == 40:
                slub1_dead = 1
            if scnt%10 < 5:
                cslub1 = slub[0]
            else:
                cslub1 = slub[2]
            scnt += 1

        if player_killed:
            if not pcnt:
                cplayer = player[5]
            if pcnt >= 40:
                color_surface(cplayer, 255, 255, 255)
            if pcnt == 80:
                player_dead = 1
            pcnt += 1

        if not slub1_dead:
            window.blit(cslub1, (bias+slub1_x, slub1_y))
        if not player_dead:
            window.blit(cplayer, (bias+px, py))

        ctime = Time.time()

        time = clock.tick(60)

        events = pygame.event.get()
        for event in events:
            if not player_killed:
                if event.type == KEYDOWN and event.key == K_j and not jump_speed:
                    dtime = Time.time()
                    ja = 1
                    jump_speed = 17
                    key_up = 0
                    first_added = 0
                if event.type == KEYUP and event.key == K_j:
                    key_up = 1

        if not player_killed:
            if pygame.key.get_pressed()[K_d]:
                dx += 3
                player_r.move_ip(3, 0)
                for rect in rects:
                    if player_r.colliderect(rect):
                        dx += rect.left - player_r.right
                        player_r.move_ip(rect.left-player_r.right, 0)
                if (count % 60) < 15: cplayer = player[0]
                elif (count % 60) < 30: cplayer = player[1]
                elif (count % 60) < 45: cplayer = player[2]
                else: cplayer = player[3]
            elif pygame.key.get_pressed()[K_a]:
                if px > 0:
                    dx -= 3
                    player_r.move_ip(-3, 0)
                for rect in rects:
                    if player_r.colliderect(rect):
                        dx += rect.right - player_r.left
                        player_r.move_ip(rect.right-player_r.left, 0)
                if (count % 60) < 15: cplayer = fplayer[0]
                elif (count % 60) < 30: cplayer = fplayer[1]
                elif (count % 60) < 45: cplayer = fplayer[2]
                else: cplayer = fplayer[3]
            else:
                if cplayer in player:
                    cplayer = player[0]
                elif cplayer in fplayer:
                    cplayer = fplayer[0]

        jump_speed -= ja
        dy -= jump_speed
        player_r.move_ip(0, -jump_speed)
        for rect in rects:
            if player_r.colliderect(rect):
                if jump_speed < 0:
                    dy += rect.top - player_r.bottom
                    player_r.move_ip(0, rect.top-player_r.bottom)
                else:
                    dy += rect.bottom - player_r.top
                    player_r.move_ip(0, rect.bottom-player_r.top)
                jump_speed = 0

        if jump_speed:
            if cplayer in player:
                cplayer = player[4]
            else:
                cplayer = fplayer[4]

        count += 1

        if px >= window.get_width() * 1.75 / 3.0:
            bias -= dx
        else:
            bias = 0

        if count%22 < 11: cslub1 = slub[0]
        else: cslub1 = slub[1]
        if not slub1_killed:
            slub1_x += slub1_speed
            slub1_r.move_ip(slub1_speed ,0)
        if slub1_r.colliderect(pipe1_r):
            slub1_speed = -slub1_speed
            slub1_x += pipe1_r.left - slub1_r.right
            slub1_r.right = pipe1_r.left
        if slub1_x < 0:
            slub1_speed = -slub1_speed
            slub1_x = 0
            slub1_r.left = 0

        px += dx
        py += dy

        if not slub1_killed:
            if player_r.colliderect(slub1_r):
                if jump_speed < 0:
                    slub1_killed = 1
                    jump_speed = 10
                else:
                    player_killed = 1

        pygame.display.update()

if __name__ == '__main__':
    main()