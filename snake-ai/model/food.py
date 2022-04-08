import pygame
import random

# Draw food rectangle at a random position inside the field
class Food():
    foodColors = [
            (255, 255, 0),   # yellow
            (0, 255, 255),   # cyan
            (255, 0, 255),   # magenta
            (128, 128, 255)  # light blue
            ]

    def __init__(self, field):
        self.field = field

        # x and y are logical movement coordinates and not the pixel positions
        self.x = random.randint(0, field.width - 1)
        self.y = random.randint(0, field.height - 1)

        # random food color
        self.color = random.choice(self.foodColors)

    # return current position of the food
    def position(self):
        result = (self.x, self.y)
        return result

    def draw(self):
        # (start_x, start_y, width, height)
        # (start_x, start_y) are from top left corner
        px = self.field.start_x + self.x * self.field.block_size
        py = self.y * self.field.block_size
        rect = (px, py, self.field.block_size, self.field.block_size)
        pygame.draw.rect(self.field.screen, self.color, rect, 0)
