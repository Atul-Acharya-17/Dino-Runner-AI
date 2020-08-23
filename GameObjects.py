import pygame
import copy

PATH = "Images\\"


class Tree:
    def __init__(self):
        self.image = pygame.image.load(PATH + 'tree.png')
        self.x = 700
        self.y = 283
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.type = 'tree'

    def copy(self):
        copyobj = Tree()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Tree1:
    def __init__(self):
        self.image = pygame.image.load(PATH + 'tree1.png')
        self.x = 700
        self.y = 289
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.type = 'tree'

    def copy(self):
        copyobj = Tree1()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Tree2:
    def __init__(self):
        self.image = pygame.image.load(PATH + 'tree2.png')
        self.x = 700
        self.y = 283
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.type = 'tree'

    def copy(self):
        copyobj = Tree2()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Tree3:
    def __init__(self):
        self.image = pygame.image.load(PATH + 'tree3.png')
        self.x = 700
        self.y = 250
        self.type = 'tree'

    def copy(self):
        copyobj = Tree3()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Tree4:
    def __init__(self):
        self.image = pygame.image.load(PATH + 'tree4.png')
        self.x = 700
        self.y = 276
        self.type = 'tree'

    def copy(self):
        copyobj = Tree4()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Tree5:
    def __init__(self):
        self.image = pygame.image.load(PATH + 'tree4.png')
        self.x = 700
        self.y = 277
        self.type = 'tree'

    def copy(self):
        copyobj = Tree5()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Pterodactyl:
    def __init__(self):
        self.image_1 = pygame.image.load(PATH + 'bird1.png')
        self.image_2 = pygame.image.load(PATH + 'bird2.png')
        self.x = 700
        self.y = 285
        self.image_1 = pygame.transform.scale(self.image_1, (60, 40))
        self.image_2 = pygame.transform.scale(self.image_2, (60, 40))
        self.image = self.image_1
        self.type = 'bird'

    def copy(self):
        copyobj = Pterodactyl()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Background:
    def __init__(self):
        self.background = pygame.image.load(PATH + 'ground.png')
        self.background_velocity = -1.25
        self.x = 0
        self.y = 320


class Dino:
    def __init__(self):
        self.dino_1 = pygame.image.load(PATH + 'dra1.png')
        self.dino_2 = pygame.image.load(PATH + 'dra3.png')
        self.dino_3 = pygame.image.load(PATH + 'dra4.png')
        self.dino_4 = pygame.image.load(PATH + 'dra5.png')
        self.dino_5 = pygame.image.load(PATH + 'dra7.png')
        self.dino_6 = pygame.image.load(PATH + 'dra8.png')
        self.dino_1 = pygame.transform.scale(self.dino_1, (50, 50))
        self.dino_2 = pygame.transform.scale(self.dino_2, (50, 50))
        self.dino_3 = pygame.transform.scale(self.dino_3, (50, 50))
        self.dino_4 = pygame.transform.scale(self.dino_4, (50, 50))
        self.dino_5 = pygame.transform.scale(self.dino_5, (70, 50))
        self.dino_6 = pygame.transform.scale(self.dino_6, (70, 50))
        self.x = 100
        self.y = 276
        self.grounded_y = self.y + 1
        self.jump_height = 150
        self.bending_y = 282
        self.jump = False
        self.descend = False
        self.bend = False

    def copy(self):
        copyobj = Dino()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Cloud:
    def __init__(self, x):
        self.cloud = pygame.image.load(PATH + 'cloud.png')
        self.x = x
        self.y = 150
