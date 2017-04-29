import pyglet
import glob
import os


script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, 'images/obstacle.png')

obstacles_img = pyglet.image.load(path)
obstacles_batch = pyglet.graphics.Batch()
obstacles = []
game_level = 0
level_files = glob.glob("{}/levels/p*.txt".format(script_dir))

obstacles_list = []


def open_new_obstacles_file():
    global obstacles_list
    if game_level >= len(level_files):
        raise SystemExit

    file = open(level_files[game_level], "r+")
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
