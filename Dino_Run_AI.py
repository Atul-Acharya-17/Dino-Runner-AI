from GameObjects import *
import random
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
                          self.pterodactyl]
        self.objects = []
        self.background = Background()

        self.clouds = [Cloud(600), Cloud(1200)]
        self.clouds[1].y = 120

        self.dino = Dino()

        self.score = 0

        self.font = pygame.font.Font("freesansbold.ttf", 16)

        self.neural_network = pickle.load(open("neural_network_final.pickle", "rb"))

    def play_game(self):

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
        self.score = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)

            action = self.decide_action()
            self.take_action(action)

            self.move_clouds()

            if not self.dino.jump and not self.dino.descend:
                image = self.move_dino(walk)
            else:
                image = self.jump()

            if self.collision(image):
                running = False

            self.draw_objects()
            self.display_text()
            self.update_objects(walk)

            pygame.display.update()

            walk += 1

            self.score += 0.025

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

    def decide_action(self):
        inputs = self.get_inputs(self.dino)
        output = self.neural_network.activate(inputs)
        action = output.index(max(output))
        return action

    def take_action(self, action):
        if action == 0:
            if not self.dino.jump and not self.dino.descend:
                self.dino.jump = True
            self.dino.bend = False

        elif action == 1:
            self.dino.bend = True

        else:
            self.dino.bend = False

    def move_clouds(self):
        for cloud in self.clouds:
            self.screen.blit(cloud.cloud,
                             (cloud.x - self.background.background_velocity, cloud.y))

    def display_text(self):
        score = self.font.render("Score: " + str(int(self.score)), True, (0, 0, 0))
        self.screen.blit(score, (850, 15))

    def move_dino(self, walk):
        if not self.dino.jump and not self.dino.descend:
            if walk % 128 <= 63:
                if self.dino.bend:
                    self.dino.y = self.dino.bending_y
                    image = self.dino.dino_5
                    self.screen.blit(image, (self.dino.x, self.dino.y))
                else:
                    self.dino.y = self.dino.grounded_y - 1
                    image = self.dino.dino_2
                    self.screen.blit(image, (self.dino.x, self.dino.y))
            else:
                if self.dino.bend:
                    self.dino.y = self.dino.bending_y
                    image = self.dino.dino_6
                    self.screen.blit(image, (self.dino.x, self.dino.y))
                else:
                    self.dino.y = self.dino.grounded_y - 1
                    image = self.dino.dino_3
                    self.screen.blit(image, (self.dino.x, self.dino.y))
        try:
            return image
        except UnboundLocalError:
            return

    def jump(self):
        if self.dino.jump_height <= self.dino.y < self.dino.grounded_y:
            if self.dino.jump:
                self.dino.y -= 0.75
                self.dino.descend = False
                image = self.dino.dino_1
                self.screen.blit(image, (self.dino.x, self.dino.y))

            elif self.dino.descend:
                self.dino.y += 0.75
                self.dino.jump = False
                image = self.dino.dino_1
                self.screen.blit(image, (self.dino.x, self.dino.y))

        if self.dino.y < self.dino.jump_height:
            self.dino.y = self.dino.jump_height
            self.dino.jump = False
            self.dino.descend = True
        if self.dino.y > self.dino.grounded_y:
            self.dino.y = self.dino.grounded_y - 1
            self.dino.jump = False
            self.dino.descend = False

        try:
            return image
        except UnboundLocalError:
            return

    def collision(self, image):
        for i in range(len(self.objects)):
            if self.objects[i].x < self.dino.x + image.get_size()[0] < self.objects[i].x + \
                    self.objects[i].image.get_size()[0] and self.objects[i].y < self.dino.y + image.get_size()[
                    1] < self.objects[i].y + self.objects[i].image.get_size()[1]:
                return True

            if self.objects[i].x < self.dino.x < self.objects[i].x + \
                    self.objects[i].image.get_size()[0] and self.objects[i].y < self.dino.y + image.get_size()[
                    1] < self.objects[i].y + self.objects[i].image.get_size()[1]:
                return True

            elif self.objects[i].y < self.dino.y < self.objects[i].y + self.objects[i].image.get_size()[1]:
                if self.objects[i].x < self.dino.x < self.objects[i].x + self.objects[i].image.get_size()[0] or \
                        self.objects[i].x < self.dino.x + image.get_size()[0] < self.objects[i].x + \
                        self.objects[i].image.get_size()[0]:
                    return True

        return False

    def draw_objects(self):
        self.screen.blit(self.background.background,
                         (self.background.x - self.background.background_velocity, self.background.y))
        self.screen.blit(self.background.background, (
            self.background.x + self.screen_width - self.background.background_velocity, self.background.y))

        self.screen.blit(self.objects[0].image, (self.objects[0].x, self.objects[0].y))
        self.screen.blit(self.objects[1].image, (self.objects[1].x, self.objects[1].y))

    def update_objects(self, walk):
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
            self.objects.pop(0)
            obs = random.choice(self.obstacles).copy()
            obs.x = 1000 + random.random() * 500
            if obs.x - self.objects[0].x < 600:
                obs.x += 600
            if obs.type == 'bird':
                obs.y = random.choice(BIRD_HEIGHT)
            self.objects.append(obs)

        try:
            for i in range(len(self.objects)):
                if walk % 256 <= 127:
                    self.objects[i].image = self.objects[i].image_1
                else:
                    self.objects[i].image = self.objects[i].image_2

        except AttributeError:
            pass


if __name__ == '__main__':
    g = Game()
    g.play_game()
