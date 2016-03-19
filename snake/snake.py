#! /usr/bin/env python

import pyglet
from pyglet.window import key
import random
from collections import deque
import obstacle
import os

new_script_dir = os.path.dirname(__file__)


# Globals constants
resolution = 640, 480
sprite_size = 20
window = pyglet.window.Window(caption="Snake")
background_img_path = os.path.join(new_script_dir, 'background.png')
background = pyglet.image.load(background_img_path)

# Global vars
current_orientation = 0
last_key_pressed = 0
score = 0

# Snake sprite
snake_img_path = os.path.join(new_script_dir, 'snake.png')
snake_img = pyglet.image.load(snake_img_path)
snake_batch = pyglet.graphics.Batch()
snake = deque([])


def create_snake():
    global snake_curr_pos
    snake_curr_pos = random.randrange(0, resolution[0], sprite_size), random.randrange(0, resolution[1], sprite_size)
    snake.append(pyglet.sprite.Sprite(snake_img, snake_curr_pos[0], snake_curr_pos[1],
                                  batch=snake_batch))


create_snake()

# Food sprite
food_img_path = os.path.join(new_script_dir, 'food.png')
food_img = pyglet.image.load(food_img_path)
food_batch = pyglet.graphics.Batch()
food = []


# Score
font_path = os.path.join(new_script_dir, 'font.ttf')
pyglet.font.add_file(font_path)
font = pyglet.font.load("FFF Forward")
score_label = pyglet.text.Label("Score: {}".format(score),
                                font_name="FFF Forward",
                                font_size=20,
                                x=60, y=450,
                                anchor_x="left", anchor_y="center")

# Obstacles

def random_xy_coordinates():
    return random.randrange(0, resolution[0], sprite_size), random.randrange(0, resolution[1], sprite_size)


def generate_new_food():
    for i in range(0, (obstacle.game_level+1) * 4):
        g = [1]
        while (len(g)!=0):
            x, y = random_xy_coordinates()
            g = [i for i,o in enumerate(obstacle.obstacles) if o.x == x and o.y == y]
        food.append(pyglet.sprite.Sprite(food_img, x, y,
                                         batch=food_batch))


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    snake_batch.draw()
    food_batch.draw()
    score_label.draw()
    obstacle.obstacles_batch.draw()


def new_orientation(orientation, key_pressed):
    if key_pressed == key.RIGHT:
        orientation -= 90
    elif key_pressed == key.LEFT:
        orientation += 90
    if orientation < 0:
        orientation += 360
    return orientation % 360


def new_position(orientation):
    x, y = snake_curr_pos
    if orientation == 0:
        x += sprite_size
    elif orientation == 90:
        y += sprite_size
    elif orientation == 180:
        x -= sprite_size
    elif orientation == 270:
        y -= sprite_size
    x %= resolution[0]
    y %= resolution[1]

    return x, y

# end game


def game_over():
    global score, game_level
    obstacle.game_level = 0
    food.clear()
    snake.clear()
    obstacle.obstacles.clear()
    cord = random_xy_coordinates()
    snake.append(pyglet.sprite.Sprite(snake_img, cord[0], cord[1],
                                  batch=snake_batch))
    obstacle.open_new_obstacles_file()
    obstacle.generate_new_obstacles()
    generate_new_food()
    score = 0
    score_label.text = "Score:{}".format(score)



@window.event
def on_key_press(symbol, modifiers):
    global last_key_pressed
    last_key_pressed = symbol


obstacle.open_new_obstacles_file()
obstacle.generate_new_obstacles()
generate_new_food()


def update(dt):
    global snake_curr_pos
    global last_key_pressed
    global score, current_orientation
    global game_level
    current_orientation = new_orientation(current_orientation, last_key_pressed)
    snake_curr_pos = new_position(current_orientation)
    snake_x, snake_y = snake_curr_pos
    last_key_pressed = 0
    snake.append(pyglet.sprite.Sprite(snake_img, snake_x, snake_y,
                                      batch=snake_batch))
    eaten = [i for i, f in enumerate(food) if f.x == snake_x and f.y == snake_y]
    tail = [r for r in snake if r.x == snake_x and r.y == snake_y]
    obstacles_touched = [r for r in obstacle.obstacles if r.x == snake_x and r.y == snake_y]

    if len(eaten) == 0:
        snake.popleft()
    else:
        food.pop(eaten[0])
        score += 1
        score_label.text = "Score: {}".format(score)
    if len(food) == 0:
        obstacle.game_level += 1
        obstacle.obstacles.clear()
        snake.clear()
        create_snake()
        print(">> {}".format(obstacle.game_level))
        obstacle.open_new_obstacles_file()
        obstacle.generate_new_obstacles()
        generate_new_food()

    if len(tail) > 1:
        print("Game over")
        game_over()
    if len(obstacles_touched):
        print("game over")
        game_over()


def main():
    pyglet.clock.schedule_interval(update, 1 / 12)
    pyglet.app.run()

main()
