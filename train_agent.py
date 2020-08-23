from GameObjects import *
import random
import neat
import os
import pickle

pygame.init()
WHITE = (250, 250, 250)

BIRD_HEIGHT = [i for i in range(200, 240, 5)]


class Game:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 500
        self.screen = pygame.display.set_mode((1000, 500))
        pygame.display.set_caption("Dino Run")
        self.tree = Tree()
        self.tree1 = Tree1()
        self.tree2 = Tree2()
        self.tree3 = Tree3()
        self.tree4 = Tree4()
        self.tree5 = Tree5()
        self.pterodactyl = Pterodactyl()
        self.pterodactyl.y = random.choice(BIRD_HEIGHT)

        self.obstacles = [self.tree, self.tree1, self.tree2, self.tree3, self.tree4, self.tree5, self.pterodactyl,
                          self.pterodactyl, self.pterodactyl]
        self.objects = []
        self.background = Background()

        self.clouds = [Cloud(600), Cloud(1200)]

        self.dino = Dino()
        self.generaton = -1

        self.score = 0

        self.font = pygame.font.Font("freesansbold.ttf", 16)

    def fitness(self, genomes, config):
        self.generaton += 1
        dinos = []
        nets = []
        ge = []
        for g_id, g in genomes:
            self.objects = []
            walk = 0
            running = True
            obs = random.choice(self.obstacles).copy()
            obs.x = 700
            if obs.type == 'bird':
                obs.y = random.choice(BIRD_HEIGHT)
            self.objects.append(obs)
            obs = random.choice(self.obstacles).copy()
            obs.x = 1400
            if obs.type == 'bird':
                obs.y = random.choice(BIRD_HEIGHT)
            self.objects.append(obs)

            image = self.dino.dino_1

            net = neat.nn.FeedForwardNetwork.create(g, config)
            g.fitness = 0

            dino = Dino().copy()
            dinos.append(dino)
            ge.append(g)
            nets.append(net)

            self.score = 0

        while running:

            indices_to_remove = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(WHITE)

            for x, dino in enumerate(dinos):
                inputs = self.get_inputs(dino)
                output = nets[x].activate(inputs)
                action = output.index(max(output))

                if action == 0:
                    if not dinos[x].jump and not dinos[x].descend:
                        dinos[x].jump = True
                    dinos[x].bend = False

                elif action == 1:
                    dinos[x].bend = True

                else:
                    dinos[x].bend = False

            for cloud in self.clouds:
                self.screen.blit(cloud.cloud,
                                 (cloud.x - self.background.background_velocity, cloud.y))

            for x, dino in enumerate(dinos):
                if not dinos[x].jump and not dinos[x].descend:
                    if walk % 128 <= 63:
                        if dinos[x].bend:
                            dinos[x].y = dinos[x].bending_y
                            image = dinos[x].dino_5
                            self.screen.blit(image, (dinos[x].x, dinos[x].y))
                        else:
                            dinos[x].y = dinos[x].grounded_y - 1
                            image = dinos[x].dino_2
                            self.screen.blit(image, (dinos[x].x, dinos[x].y))
                    else:
                        if dinos[x].bend:
                            dinos[x].y = dinos[x].bending_y
                            image = dinos[x].dino_6
                            self.screen.blit(image, (dinos[x].x, dinos[x].y))
                        else:
                            dinos[x].y = dinos[x].grounded_y - 1
                            image = dinos[x].dino_3
                            self.screen.blit(image, (dinos[x].x, dinos[x].y))

                if dinos[x].jump_height <= dinos[x].y < dinos[x].grounded_y:
                    if dinos[x].jump:
                        dinos[x].y -= 0.75
                        dinos[x].descend = False
                        image = dinos[x].dino_1
                        self.screen.blit(image, (dinos[x].x, dinos[x].y))

                    elif dinos[x].descend:
                        dinos[x].y += 0.75
                        dinos[x].jump = False
                        image = dinos[x].dino_1
                        self.screen.blit(image, (dinos[x].x, dinos[x].y))

                if dinos[x].y < dinos[x].jump_height:
                    dinos[x].y = dinos[x].jump_height
                    dinos[x].jump = False
                    dinos[x].descend = True
                if dinos[x].y > dinos[x].grounded_y:
                    dinos[x].y = dinos[x].grounded_y - 1
                    dinos[x].jump = False
                    dinos[x].descend = False
                # ******************
                for i in range(len(self.objects)):
                    if self.objects[i].x < dinos[x].x + image.get_size()[0] < self.objects[i].x + \
                            self.objects[i].image.get_size()[0] and self.objects[i].y < dinos[x].y + image.get_size()[
                        1] < self.objects[i].y + self.objects[i].image.get_size()[1]:
                        indices_to_remove.append(x)

                    if self.objects[i].x < dinos[x].x < self.objects[i].x + \
                            self.objects[i].image.get_size()[0] and self.objects[i].y < dinos[x].y + image.get_size()[
                        1] < self.objects[i].y + self.objects[i].image.get_size()[1]:
                        indices_to_remove.append(x)

                    elif self.objects[i].y < dinos[x].y < self.objects[i].y + self.objects[i].image.get_size()[1]:
                        if self.objects[i].x < dinos[x].x < self.objects[i].x + self.objects[i].image.get_size()[0] or \
                                self.objects[i].x < dinos[x].x + image.get_size()[0] < self.objects[i].x + \
                                self.objects[i].image.get_size()[0]:
                            indices_to_remove.append(x)

            self.screen.blit(self.background.background,
                             (self.background.x - self.background.background_velocity, self.background.y))
            self.screen.blit(self.background.background, (
                self.background.x + self.screen_width - self.background.background_velocity, self.background.y))

            self.display_text(ge)

            self.screen.blit(self.objects[0].image, (self.objects[0].x, self.objects[0].y))
            self.screen.blit(self.objects[1].image, (self.objects[1].x, self.objects[1].y))

            self.objects[0].x += self.background.background_velocity
            self.objects[1].x += self.background.background_velocity
            self.background.x += self.background.background_velocity

            for i in range(len(self.clouds)):
                self.clouds[i].x += self.background.background_velocity

            if self.background.x <= -self.screen_width:
                self.background.x = 0

            for i in range(len(self.clouds)):
                if self.clouds[i].x + self.clouds[i].cloud.get_size()[0] < 0:
                    self.clouds[i].x = 1200

            if self.objects[0].x + self.objects[0].image.get_size()[0] <= 0:
                for i in range(len(ge)):
                    ge[i].fitness += 1
                self.objects.pop(0)
                obs = random.choice(self.obstacles).copy()
                obs.x = 1000 + random.random() * 500
                if obs.x - self.objects[0].x < 600:
                    obs.x += 600
                if obs.type == 'bird':
                    obs.y = random.choice(BIRD_HEIGHT)
                self.objects.append(obs)

            pygame.display.update()

            walk += 1

            try:
                for i in range(len(self.objects)):
                    if walk % 256 <= 127:
                        self.objects[i].image = self.objects[i].image_1
                    else:
                        self.objects[i].image = self.objects[i].image_2

            except AttributeError:
                pass

            indices_to_remove.sort(reverse=True)
            try:
                for e in indices_to_remove:
                    dinos.pop(e)
                    nets.pop(e)
                    ge.pop(e)

            except IndexError:
                pass

            if len(dinos) <= 0:
                break

            if ge[0].fitness > 1000:
                pickle.dump(nets[i], open("neural_network_final.pickle", "wb"))
                print("saved")
                running = False

            self.score += 0.03

    def get_inputs(self, dino):
        if self.objects[0].x - dino.x >= 0:
            index = 0
        else:
            index = 1

        if self.objects[index].type == 'tree':
            object_type = 1
        else:
            object_type = 0
        inputs = [(self.objects[index].x - dino.x) / self.screen_width,
                  self.objects[index].y / self.screen_height,
                  (self.objects[index].image.get_size()[1]) / self.screen_height,
                  object_type]

        return inputs

    def run(self, config_path):
        generations = 50
        self.generaton = -1
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)
        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)

        winner = population.run(self.fitness, generations)

        print('\nBest genome:\n{!s}'.format(winner))

    def display_text(self, ge):

        genome = self.font.render("Population: " + str(len(ge)), True, (0, 0, 0))
        generation = self.font.render("Generation: " + str(self.generaton), True, (0, 0, 0))
        score = self.font.render("Score: " + str(int(self.score)), True, (0, 0, 0))

        self.screen.blit(generation, (450, 20))
        self.screen.blit(genome, (445, 40))
        self.screen.blit(score, (880, 15))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEAT config.txt")
    g = Game()
    g.run(config_path)
