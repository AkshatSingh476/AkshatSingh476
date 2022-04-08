import pygame
import numpy as np
import math
import game_utils as gmu

class Snake:
    # A snake has a body that consists of several points
    # The body has a head (first point) and a tail (last point)
    headColor = (50, 255, 0)
    bodyColor = (0, 200, 0)
    damageColor = (255, 0, 0)

    # ===================================================================
    # constructor
    # ===================================================================
    def __init__(self, field, color, len = 5, x = 10, y = 10):
        # Start with a snake in a horizontal position
        self.field = field
        self.body = []
        self.growLength = 0

        for i in range(0, len):
            # self.body.append((x, y-i))
            # self.body.append((x + i, y))
            self.body.append((x - i, y))

        self.color = color

        # print('Snake direction: ', np.array(self.body[0]) - np.array(self.body[1]))

    # ===================================================================
    def grow(self, length = 1):
        self.growLength += length

    def position(self):
        return self.body[0]

    # current head direction
    def head_direction(self):
        result = np.array(self.body[0]) - np.array(self.body[1])
        return result

    # current head direction
    def orientation(self):
        result = np.array(self.body[0]) - np.array(self.body[1])
        return (result[0], result[1])

    # current head reverse direction
    def reverse_direction(self):
        result = np.array(self.body[1]) - np.array(self.body[0])
        return result

    def tail_direction(self):
        result = np.array(self.body[-2]) - np.array(self.body[-1])
        return result

    # left to the current (i.e relative left)
    def left_direction(self):
        dx, dy = self.head_direction()
        return (-dy, dx)

    # right to the current (i.e. relative right)
    def right_direction(self):
        dx, dy = self.head_direction()
        return (dy, -dx)

    def food_direction(self, food):
        result = np.array(food.position()) - np.array(self.body[0])
        return result

    def food_distance(self, food):
        hx, hy = self.body[0]
        fx, fy = food.position()
        result = math.sqrt(((hx-fx)**2) + ((hy-fy)**2))
        return result

    # ===================================================================
    # Move the snake in the given direction and check if the move was valid or not
    # if snake hits any wall - is not valid
    # if snake head bumps into its own body - invalid move
    # it will return False for an invalid move, otherwise True
    # ===================================================================
    def move(self, dx, dy):
        # Move the snake in the given direction
        # either it will move one position on X axis or one position on Y axis
        # first get current position of head
        (nx, ny) = self.body[0]

        # calculate new position of head
        nx += dx
        ny += dy

        # check if this new move makes the head clashing with its own body
        # return False if it collides its an invalid move
        # if (self.body[0]) in self.body[1:]:
        if (nx, ny) in self.body[0:]:
            #print("I hit myself ...")
            return gmu.MOVE_SELF_HIT

        if nx < 0 or nx >= self.field.width or ny < 0 or ny >= self.field.height:
            # Does it hit any walls
            # if yes then it is also an invalid move
            #print("I hit the wall ...")
            return gmu.MOVE_WALL_HIT

        # Insert a new head position in the front
        self.body.insert(0, (nx, ny)) # insert new position of head

        if self.growLength > 0:
            # every next move will increase the length by growLength value
            # it will keep growing till growLength becomes 0
            self.growLength -= 1
        else:
            # otherwise just move the snake i.e. remove last element i.e. tail
            self.body.pop()

        # otherwise its a valid move
        return gmu.MOVE_OK

    # ===================================================================
    # Display the snake
    # ===================================================================
    def draw(self, damage = False):
        # Draw body of the snake
        for i in range(0, len(self.body)):
            (x, y) = self.body[i]
            px = x * self.field.block_size + self.field.start_x
            py = y * self.field.block_size
            rect = (px, py, self.field.block_size, self.field.block_size)
            pygame.draw.rect(self.field.screen, self.color, rect, 0)
