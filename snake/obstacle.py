import pyglet
import glob
import os
import sys


script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, 'obstacle.png')

obstacles_img = pyglet.image.load(path)
obstacles_batch = pyglet.graphics.Batch()
obstacles = []
game_level = 0
phase_files = glob.glob("{}/p*.txt".format(script_dir))

obstacles_list = []


def open_new_obstacles_file():
    global obstacles_list
    if game_level >= len(phase_files):
        raise SystemExit
        #pass
    file = open(phase_files[game_level], "r+")
    obstacles_list = file.readlines()
    file.close()


def generate_new_obstacles():
    global obstacles_list
    found = []
    for i in range(0, len(obstacles_list)):
        found = [i for i, c in enumerate(obstacles_list[i]) if c == 'X']
        for a in range(0, len(found)):
            x,y = found[a] * 20, 480-20*(i+1)
            obstacles.append(pyglet.sprite.Sprite(obstacles_img, x, y, batch=obstacles_batch))
