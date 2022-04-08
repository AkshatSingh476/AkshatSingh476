import sys
import math
import gui_utils as gu
import neat
import logging
import os

log = logging.getLogger(__name__)
log.setLevel(os.environ.get("LOGLEVEL", "INFO"))

# local imports
import game_utils as gmu
from game_utils import SnakeUtil
from model.field import Field
from model.snake import Snake
from model.food import Food
# ===============================================================================================
# Global variables
# ===============================================================================================
gen_number = 0
best_food_count = 0   # best food count among all generations
best_instance = None  # best instance among all generations
best_fitness = 0      # best fitness among all generations

# ===============================================================================================
# Method declaration
# ===============================================================================================
def play_game(genomes, config):
    global pop
    global pygame
    global screen
    global figure
    global gen_number
    global best_food_count
    global best_instance
    global best_fitness
    global best_fitness_values
    global avg_fitness_values
    global gen_numbers

    # best values for per generation
    avg_fitness = 0
    gen_food_count = 0
    gen_fitness = 0

    dx, dy = [1, 0]
    genome_number = 0
    snake_color = gmu.extract_rgb(gmu.SNAKE_COLOR)

    # Create the field, the snake and a bit of food
    field_color = gmu.extract_rgb(gmu.FIELD_COLOR)
    fieldObj = Field(screen, field_color, gmu.START_X, gmu.FIELD_WIDTH, gmu.FIELD_HEIGHT, gmu.BLOCK_SIZE)
    snakeUtil = SnakeUtil()

    # Outer loop is for all the genomes (total number of genomes => pop_size in the config-full file
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # Snake starts from a fixed location
        # snakeObj = Snake(fieldObj, snake_color, 5, x = int(sl.FIELD_WIDTH/2), y=int(sl.FIELD_HEIGHT/2))
        # snakeObj = Snake(fieldObj, snake_color, 5, x=0, y=int(gmu.FIELD_HEIGHT / 2))
        snakeObj = Snake(fieldObj, snake_color)
        dx, dy = snakeObj.head_direction()

        # create food at random position
        foodObj = Food(fieldObj)

        # initialize the run again
        score = 0.0
        loopPoints = set()
        food_count = 0   # initialize food_count when the generation starts

        while True:
            event = pygame.event.wait()
            pygame.event.get()

            # Window is going to be closed
            if event.type == pygame.QUIT:
                log.info("Quitting the game now ...")

                ## save the population
                gmu.save_obj_to_file(pop, gmu.GAME_POP_FILE)
                pygame.quit()
                sys.exit()

            # Every TIME_DURATION there will be a MOVE_EVENT to move the snake
            if event.type == MOVE_EVENT:
                # current distance from the food
                hx, hy = snakeObj.position()
                fx, fy = foodObj.position()
                dist_before_move = math.sqrt((hx - fx) ** 2 + (hy - fy) ** 2)

                # find out current input points
                inputs = snakeUtil.game_observations(snakeObj, foodObj)

                # it will generate 3 outputs (continue straight, left or right)
                outputs = net.activate(inputs)
                outputs[0] = round(outputs[0], 4)
                outputs[1] = round(outputs[1], 4)
                outputs[2] = round(outputs[2], 4)

                # find index of maximum value and determine the direction (0 - straight, 1 - left or 2 - right)
                direction = outputs.index(max(outputs))

                # decide the movement direction based on the outcome
                if direction == 1:  # turn left
                    (dx, dy) = snakeObj.left_direction()
                elif direction == 2:  # turn right
                    (dx, dy) = snakeObj.right_direction()
                else:  # keep going straight (direction = 0)
                    # dx and dy values will remain same
                    pass

                # move the snake now, also check if move is invalid or it got into the loop
                cur_dir = snakeObj.head_direction()
                moveResult = snakeObj.move(dx, dy)
                log.info('inputs:', inputs, 'outputs:', outputs, 'head:', snakeObj.position(), cur_dir, 'dir:', (dx, dy), 'result:', moveResult)

                # Apply penalty for hitting the wall or self
                # also, if the score goes below the MIN_SCORE, end the game
                if moveResult == gmu.MOVE_SELF_HIT or moveResult == gmu.MOVE_WALL_HIT:
                    # too bad snake died
                    # genome.fitness = 0
                    # score -= moveResult
                    break
                if snakeObj.body[0] in loopPoints:
                    score -= gmu.GOT_LOOP
                    # once the loop is detected then reset loopPoints
                    loopPoints.clear()
                    break
                else:
                    # Reward the snake for being alive
                    score += gmu.ALIVE_SCORE

                #log.info('Score: ', score, ' head: ', snakeObj.body[0])
                # Finally check the score
                if score <= gmu.MIN_SCORE:
                    break           

                # keep tracking head positon till next food grab
                loopPoints.add(snakeObj.body[0])

                # distance from the food after the move
                hx, hy = snakeObj.position()
                dist_after_move = math.sqrt((hx - fx) ** 2 + (hy - fy) ** 2)

                # adjust the score
                if (hx, hy) == (fx, fy):
                    # if snake grabs the food
                    food_count += 1
                    score += gmu.FOOD_SCORE
                    snakeObj.grow(2)          # grow by one length

                    # Make new food now
                    foodObj = Food(fieldObj)

                    # Also reset loopPoints
                    loopPoints = set()
                elif dist_after_move > dist_before_move:
                    score -= gmu.FAR_MOVE
                elif dist_after_move < dist_before_move:
                    score += gmu.NEAR_SCORE
                else:
                    # place holder for something else
                    pass
            # end of MOVE_EVENT
			# fitness update for each genome
            genome.fitness = gmu.calculate_fitness(food_count, score)

            # Render snake and food
            fieldObj.draw()   # will draw empty screen
            foodObj.draw()
            snakeObj.draw()

            # Update game display
            # pygame.display.update()
            pygame.display.flip()
            pygame.time.wait(gmu.renderdelay)
        # while loop done for the current genome

        # Tell about the fitness
        # genome.fitness = score / 100
        # genome.fitness = gmu.calculate_fitness(food_count, score)
        avg_fitness += genome.fitness

        # Track best fitness for the current generation
        if genome_number == 0:
            gen_fitness = genome.fitness
            gen_food_count = food_count
        else:
            gen_fitness = max(gen_fitness, genome.fitness)
            gen_food_count = max(gen_food_count, food_count)

        # Keep saving best instance
        if best_instance == None or genome.fitness > best_fitness:
            best_instance = {
                'num_generation': gen_number,
                'fitness': genome.fitness,
                'score': score,
                'genome': genome,
                'net': net
            }

        best_food_count = max(best_food_count, gen_food_count)
        best_fitness = max(best_fitness, genome.fitness)

        # Print the statistics
        print('Generation: {} / {} \tFoodCount: {} / {} /{} \tFitness: {:.4f} / {:.4f} / {:.4f} \tScore {:.2f}'.format(gen_number, genome_number,
            food_count, gen_food_count, best_food_count, genome.fitness, gen_fitness, best_fitness, score))

        # Increase the genome number
        genome_number += 1

    # end of for loop, all genomes are done for the current generation
    # increase the generation number
    gen_number += 1
    avg_fitness = avg_fitness / len(genomes)
    avg_fitness_values.append(avg_fitness)

    # Save end results
    gmu.save_best_gen_to_file(best_instance, gmu.GAME_PICKLE_FILE)
    if gen_number % 20 == 0:
        log.info("Exporting population")
        gmu.save_obj_to_file(pop, gmu.GAME_POP_FILE)

    # Plot fitness data
    # best_fitness_values.append(best_fitness)
    best_fitness_values.append(gen_fitness)
    gen_numbers.append(gen_number)
    cur_axis = gu.cur_axis
    cur_axis.plot(gen_numbers, best_fitness_values, 'r')
    cur_axis.plot(gen_numbers, avg_fitness_values, 'b')
    canvas = gu.agg.FigureCanvasAgg(figure)
    gu.canvas.draw()
    gu.canvas.flush_events()
    size = canvas.get_width_height()  # Size of the figure above i.e. 600x400
    pg_surf = pygame.image.fromstring(gu.renderer.tostring_rgb(), size, "RGB")
    screen.blit(pg_surf, (0, 0))
    pygame.display.flip()

# ===============================================================================================
# Execution of code starts here
# ===============================================================================================
pygame = gu.pg
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, gmu.EVENT_DURATION)
clock = pygame.time.Clock()

screen = gu.screen
figure = gu.figure
best_fitness_values = gu.best_fitness_values
avg_fitness_values = gu.avg_fitness_values
gen_numbers = gu.gen_numbers

# Load the configuration
game_config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                     neat.DefaultStagnation, gmu.GAME_CONFIG)

# Create the population
pop = neat.Population(game_config)
# pop = sl.load_object_from_file('saved/population_game.dat')

# play_game method will be called n number of times (n => number of generations)
winner = pop.run(play_game, 50)
