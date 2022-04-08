import math
import os
import pickle
import food_angle as fa

GAME_POP_FILE = 'data/population_game.dat'
GAME_PICKLE_FILE = 'data/best_game_gen_inst.pickle'
GAME_CONFIG = 'config'

WALLS_POP_FILE = 'data/population_walls.dat'
WALLS_PICKLE_FILE = 'data/best_walls_gen_inst.pickle'

FIELD_COLOR = 0x000000   # Black
SNAKE_COLOR = 0xFFFFFF   # White
BLOCK_SIZE = 20          # size of blocks in pixels
FIELD_WIDTH = 16         # size of field width in blocks
FIELD_HEIGHT = 16
DIAG_DISTANCE = math.sqrt((FIELD_WIDTH * FIELD_WIDTH) + (FIELD_HEIGHT * FIELD_HEIGHT))

START_X = 660
SCREEN_SIZE = (FIELD_WIDTH * BLOCK_SIZE, FIELD_HEIGHT * BLOCK_SIZE)

renderdelay = 20  #20
rendering = True
debug_on = False

EVENT_DURATION = 1  # Every mill secs there will be an event

# Game would end if WALL_HIT, SELF_HIT, GOT_LOOP or reached MIN_SCORE
MIN_SCORE = -100

# Following would be added to the score
FOOD_SCORE = 20
NEAR_SCORE = 0.2
ALIVE_SCORE = 1

# Following would be deducted from the score
WALL_HIT = 10
SELF_HIT = 10
GOT_LOOP = 3
FAR_MOVE = 0  #1  # 2

# Move result
MOVE_OK = 0
MOVE_SELF_HIT = 1
MOVE_WALL_HIT = 2


# dictionary to transform directions
# key: current orientation
# first value: direction value clock wise (i.e. left, up, right, down)
# second value: if turning to left
# third value: if turning to right
dir_dict = {
    # current        Left      Right
    (-1,  0):  [0, ( 0, -1), ( 0,  1)],   # current direction is left
    ( 0,  1):  [1, (-1,  0), ( 1,  0)],   # current direction is up
    ( 1,  0):  [2, ( 0,  1), ( 0, -1)],   # current direction is right
    ( 0, -1):  [3, ( 1,  0), (-1,  0)]    # current direction is down
}
# By just simple observation, we can find out relative left and right directions from the current
# i.e. if dx, dy is the current direction then
# left => -dy, dx
# right => dy, -dx

# ======================================================================================
# Some separate methods
# ======================================================================================
# Extract RGB components from the color value
def extract_rgb(color):
    r = (color & 0xFF0000) >> 16
    g = (color & 0x00FF00) >> 8
    b = (color & 0x0000FF)

    return (r, g, b)

# save pickle file
def save_obj_to_file(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object_from_file(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


# instance will be saved as a pickle file
def save_best_gen_to_file(instance, filename):
    instances = []

    if os.path.isfile(filename):
        instances = load_object_from_file(filename)

    instances.append(instance)
    save_obj_to_file(instances, filename)

def calculate_fitness(food_count, score):
    return ((food_count*2) + score) / 100

# =======================================================================================
# SnakeUtil class
# =======================================================================================
class SnakeUtil:
    def __init__(self):
        pass

    # Distance between two points
    def distance(self, p1, p2):
        value = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
        return value

    def get_direction_value(self, cur_dir):
        dx, dy = cur_dir[0], cur_dir[1]
        result = dir_dict.get((dx, dy))[0]
        return result

    def left(self, orientation):
        dx, dy = orientation[0], orientation[1]
        result = dir_dict.get((dx, dy))[1]
        return result

    def right(self, orientation):
        dx, dy = orientation[0], orientation[1]
        result = dir_dict.get((dx, dy))[2]
        return result

    # ====================================================================================
    # find out safe distance in relative 3 directions i.e. left, straight and right
    # divide the distances by WIDTH or HEIGHT to normalize the values
    def relative_safe_distances(self, inputs, index, snake):
        inputs[index] = self.get_safe_distance(snake, snake.left_direction())
        inputs[index+1] = self.get_safe_distance(snake, snake.head_direction())
        inputs[index+2] = self.get_safe_distance(snake, snake.right_direction())


    # get safe distances in a given direction
    def get_safe_distance(self, snake, direction):
        dx, dy = direction[0], direction[1]
        hx, hy = snake.body[0]

        # if dx is 0 then snake is either moving up or down
        if dx == 0:
            if dy == -1:   # moving down
                dist = hy
                last_point = -1  # y will be checked up to 0
            else:    # moving up
                dist = FIELD_HEIGHT - hy
                last_point = FIELD_HEIGHT

            for py in range(hy+dy, last_point, dy):  # values from (hy+dy) to (last_point-1)
                me_there = (hx, py) in snake.body
                if me_there:
                    dist = abs(hy - py)
                    break
        else:
            # snake is moving either left or right
            if dx == -1:
                dist = hx
                last_point = -1
            else:
                dist = FIELD_WIDTH - hx
                last_point = FIELD_WIDTH

            for px in range(hx+dx, last_point, dx):
                me_there = (px, hy) in snake.body
                if me_there:
                    dist = abs(px - hx)
                    break

        #if me_there:
        #    print("I see myself over there ...")

        return dist / FIELD_WIDTH


    # ====================================================================================
    # generate inputs based on the snake current position, food position, and the walls
    def get_safety_inputs(self, inputs, index, snake):
        # input parameters to be generated
        # index 0 - is it clear straight ahead
        # index 1 - is it clear to the left
        # index 2 - is it clear to the right

        orientation = snake.orientation()
        (hx, hy) = snake.position()
        # initialize straight, left and right points as head position first
        (sx, sy) = (lx, ly) = (rx, ry) = (hx, hy)

        if orientation == (-1, 0):  # moving left
            sx = sx - 1
            ly = ly - 1
            ry = ry + 1
        elif orientation == (1, 0):  # moving right
            sx = sx + 1
            ly = ly + 1
            ry = ry - 1
        elif orientation == (0, 1):  # moving up
            sy = sy + 1
            lx = lx - 1
            rx = rx + 1
        elif orientation == (0, -1):  # moving down
            sy = sy - 1
            lx = lx + 1
            rx = rx - 1

        inputs[index] = self.check_position(sx, sy, snake)
        inputs[index + 1] = self.check_position(lx, ly, snake)
        inputs[index + 2] = self.check_position(rx, ry, snake)

    def check_position(self, px, py, snake):
        # if point is not safe return 0 otherwise 1
        if px < 0 or px >= FIELD_WIDTH or py < 0 or py >= FIELD_HEIGHT or (px, py) in snake.body:
            return 0
        else:
            return 1

    def game_observations(self, snake, food):
        inputs = [0] * 8
        # self.relative_safe_distances(inputs, 0, snake)
        (inputs[0], inputs[1]) = snake.orientation()
        self.get_safety_inputs(inputs, 2, snake)
        fa.get_food_inputs(inputs, 5, snake, food, DIAG_DISTANCE)

        # total 6 values
        return inputs
