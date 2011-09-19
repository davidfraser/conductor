#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, pygame, numpy
import pygame.gfxdraw
import time
pygame.init()

width = height = 800
screen_size = width, height
black = 0, 0, 0
white = 255, 255, 255
grey = 128, 128, 128
red = 255, 0, 0
navy = 0, 0, 128

screen = pygame.display.set_mode(screen_size)

size = max(width / 16, 32)
move_size = int(size * 0.75)

# Create 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55 in black with background white
font_size = size * 2
font = pygame.font.Font(None, font_size)
numbers = [font.render(str(num), True, black, white) for num in range(0, 60, 5)]
border_width=40

speed = int(sys.argv[1])
beats = int(sys.argv[2]) if len(sys.argv) > 2 else 4

# TODO: use optparse for this
with_second_display=False

# Draw the clock
screen.fill(black)

wait_time = 60.0/speed

current_beat = 0

signature = {4: {0: (0.5, 0.7), 1: (0.2, 0.7), 2: (0.8, 0.7), 3: (0.5, 0.2)},
             3: {0: (0.2, 0.7), 1: (0.8, 0.7), 2: (0.5, 0.2)},
             2: {0: (0.5, 0.7), 1: (0.5, 0.2)},
             5: {0: (0.4, 0.7), 1: (0.2, 0.7), 2: (0.6, 0.7), 3: (0.8, 0.7), 4: (0.4, 0.2)},
            }

beat_positions = signature[beats]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    x, y = beat_positions[current_beat]
    center_x, center_y = int(width * x), int(height * y)
    pygame.draw.circle(screen, white, (center_x, center_y), size)
    beat_text = font.render(str(current_beat + 1), True, navy)
    screen.blit(beat_text, (center_x - (beat_text.get_width()/2), center_y - (beat_text.get_height()/2)))
    last_time = time.time()
    next_time = last_time + wait_time
    update_area = (center_x-size, center_y-size, center_x+size, center_y+size)
    print current_beat + 1
    pygame.display.update(update_area)
    left_time = next_time - time.time()
    drop_time = left_time - wait_time/8
    pygame.time.wait(int(drop_time*1000))
    pygame.draw.circle(screen, black, (center_x, center_y), size)
    pygame.display.update(update_area)
    current_beat = (current_beat + 1) % beats
    x, y = beat_positions[current_beat]
    next_x, next_y = int(width * x), int(height * y)
    last_x, last_y = center_x, center_y
    sweep_time = next_time - time.time()
    LOOPS = max(30, int(sweep_time / 0.01))
    for n in range(LOOPS):
        pygame.draw.circle(screen, black, (last_x, last_y), move_size)
        left_time = next_time - time.time()
        swept_time = sweep_time - left_time
        move_time = left_time / (LOOPS-n)
        move_x, move_y = int((center_x * left_time + next_x * swept_time)/sweep_time), int((center_y * left_time + next_y * swept_time)/sweep_time)
        pygame.draw.circle(screen, grey, (move_x, move_y), move_size)
        pygame.time.delay(int(move_time*1000))
        update_area = (min(last_x-move_size, move_x-move_size),
                       min(last_y-move_size, move_y-move_size),
                       max(last_x+move_size, move_x+move_size),
                       max(last_y+move_size, move_y+move_size))
        last_x, last_y = move_x, move_y
        pygame.display.update(update_area)
    pygame.draw.circle(screen, black, (last_x, last_y), move_size)
    pygame.display.update(update_area)

