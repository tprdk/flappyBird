from src.Bird import Bird
from src.Pipe import Pipe
from src.Ground import Ground
import pygame
import os
import neat

images_path = os.path.abspath(os.getcwd())
images_path += '\\images'

GENERATION = -1
GROUND_HEIGHT = 730
WIN_WIDTH = 500
WIN_HEIGHT = 800
BackGround_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(images_path, "bg.png")))

pygame.font.init()
STAT_FONT = pygame.font.SysFont('comicsans', 50)


def collide(bird, pipe):
    bird_mask = bird.get_mask()
    pipe_top_mask = pipe.get_top_mask()  # getting mask of bird and pipe
    pipe_bot_mask = pipe.get_bot_mask()

    top_offset = (pipe.x - bird.x, pipe.top - round(bird.y))  # distance between pipe_bottom and bird
    bot_offset = (pipe.x - bird.x, pipe.bottom - round(bird.y))  # distance between pipe_top and bird

    b_point = bird_mask.overlap(pipe_bot_mask, bot_offset)  # is there any collision (bird, bottom_of_pipe)
    t_point = bird_mask.overlap(pipe_top_mask, top_offset)  # is there any collision (bird, top_of_pipe)

    if t_point or b_point:
        return True  # if there is collision return True
    return False


def draw_window(window, birds, pipes, ground, score, gene):
    window.blit(BackGround_IMAGE, (0, 0))  # draw window
    for pipe in pipes:
        pipe.draw(window)
    score_text = STAT_FONT.render('Score : ' + str(score), 1, (255, 255, 255))
    window.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))

    gene_text = STAT_FONT.render('Gene : ' + str(gene), 1, (255, 255, 255))
    window.blit(gene_text, (10, 10))

    ground.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()


def main(genomes, configuration):
    global GENERATION
    GENERATION += 1
    neural_networks = []
    genes = []
    birds = []
    for _, genome in genomes:
        neural_network = neat.nn.FeedForwardNetwork.create(genome, configuration)  # setting up a network for our genome
        neural_networks.append(neural_network)

        birds.append(Bird(230, 350))  # create a bird with that genome
        genome.fitness = 0
        genes.append(genome)  # add genome to genomes list to keep track of it's fitness value

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # opening main window
    ground = Ground(GROUND_HEIGHT)
    pipes = [Pipe(600)]  # creating pipe
    clock = pygame.time.Clock()
    score = 0  # initial score is 0
    run = True

    while run:
        clock.tick(30)  # set game to 30 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        trash_pipes = []
        add_pipe = False

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False     # we don't have any bird so end the game
            break

        for index, bird in enumerate(birds):
            bird.move()
            genes[index].fitness += 0.1  # while bird is alive it gains 0.1 fitness point

            output = neural_networks[index].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))      # giving inputs and getting output

            if output[0] > 0.5:     # if output is upper than 0.5 bird should jump
                bird.jump()

        for pipe in pipes:  # for all pipes

            for index, bird in enumerate(birds):
                if collide(bird, pipe):  # first check the collides
                    genes[index].fitness -= 1  # if bird hits the pipe its fitness score will decrease 1
                    birds.pop(index)  # remove this bird object
                    genes.pop(index)
                    neural_networks.pop(index)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True  # we can create new pipe
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # pipe out of the screen
                trash_pipes.append(pipe)  # we can remove this pipe

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            for gene in genes:  # if bird gets score its fitness value will increase 5
                gene.fitness += 5

        for trash_pipe in trash_pipes:
            pipes.remove(trash_pipe)

        for index, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= GROUND_HEIGHT or bird.y < 0:  # touch the ground
                birds.pop(index)
                neural_networks.pop(index)
                genes.pop(index)

        ground.move()
        draw_window(window, birds, pipes, ground, score, GENERATION)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    population = neat.Population(config)  # setting population

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()  # output
    population.add_reporter(stats)

    population.run(main, 10)    # run main function 10 times


if __name__ == '__main__':
    neat_path = os.path.abspath(os.getcwd())
    neat_path += '\\neat'
    config_path = os.path.join(neat_path, "config.txt")
    run(config_path)
