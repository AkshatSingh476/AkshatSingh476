import numpy as np
import math

# Distance between two points
def distance(p1, p2):
    value = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
    return value


def normalize_vector(vector):
    # divide the vector by its magnitude (i.e. hypotenuse), so the hypotenuse becomes 1
    # linalg stands for Linear Algebra APIs in Numpy
    # np.linalg.norm(vector) provides magnitude of the vector
    result = vector / np.linalg.norm(vector)
    return result


# vector cross product is needed to calculate sine of an angle
# Sin(G) = cross_product/ magnitude
def vector_cross_product(va, vb):
    result = va[0] * vb[1] - va[1] * vb[0]
    return result


# vector dot product is used to calculate cosine of an angle
# Sin(G) = dot_product/ magnitude
def vector_dot_product(va, vb):
    result = va[0] * vb[0] + va[1] * vb[1]
    return result


def get_sine_angle(va, vb):
    v1 = normalize_vector(va)
    v2 = normalize_vector(vb)
    cp = vector_cross_product(v1, v2)
    m1 = np.linalg.norm(v1)
    m2 = np.linalg.norm(v2)
    sine_angle = cp / (m1 * m2)
    return sine_angle


def get_cosine_angle(va, vb):
    v1 = normalize_vector(va)
    v2 = normalize_vector(vb)
    dp = vector_dot_product(v1, v2)
    m1 = np.linalg.norm(v1)
    m2 = np.linalg.norm(v2)
    cosine_angle = dp / (m1 * m2)
    return cosine_angle

# index 3 - Normalized distance to the food
# index 4 - sine angle to the food
# index 5 - cosine angle to the food
def get_food_inputs(inputs, index, snake, food, DIAG_DISTANCE):
    snake_direction = snake.head_direction()
    food_direction = snake.food_direction(food)
    inputs[index] = snake.food_distance(food) / DIAG_DISTANCE
    inputs[index+1] = get_sine_angle(snake_direction, food_direction)
    inputs[index+2] = get_cosine_angle(snake_direction, food_direction)

