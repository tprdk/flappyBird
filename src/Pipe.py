import pygame
import os
import random

images_path = os.path.abspath(os.getcwd())
images_path += '\\images'
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(images_path, "pipe.png")))

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def get_top_mask(self):
        return pygame.mask.from_surface(self.PIPE_TOP)

    def get_bot_mask(self):
        return pygame.mask.from_surface(self.PIPE_BOTTOM)
