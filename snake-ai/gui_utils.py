import matplotlib

matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import pylab  # Procedural interface to Matplotlib
import pygame as pg

gen_numbers = []
best_fitness_values = []
avg_fitness_values = []

# Data plot area (left side window)
figure = pylab.figure(figsize=[6.6, 3.2], dpi=100)  # pixels => 660, 320
data_axis = figure.add_subplot(111)

cur_axis = figure.gca()   # get current axis
cur_axis.plot(gen_numbers, best_fitness_values, 'r')
cur_axis.plot(gen_numbers, avg_fitness_values, 'b')

pylab.xlabel('Generation')
pylab.ylabel('Best fitness')
pylab.title('Snake AI')

canvas = agg.FigureCanvasAgg(figure)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()  # all xFF bytes

pg.init()

# pygame display
window = pg.display.set_mode((980, 320), pg.DOUBLEBUF)  # display empty window with back background
pg.display.set_caption("Hello Pygame")
screen = pg.display.get_surface()

# Create plot surface from plot canvas and add it to pygame
size = canvas.get_width_height() # Size of above plotting area
pg_surf = pg.image.fromstring(raw_data, size, "RGB")

# Add pygame surface into the full screen
screen.blit(pg_surf, (0,0))
pg.display.flip()
# pg.display.set_caption("Hello Pygame: " + str(count))
