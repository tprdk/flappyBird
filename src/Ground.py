import pygame
import os

images_path = os.path.abspath(os.getcwd())
images_path += '\\images'

GROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(images_path, "ground.png")))

class Ground:
    VEL = 5
    width = GROUND_IMAGE.get_width()
    image = GROUND_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.width < 0 :
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0 :
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.image, (self.x1, self.y))
        window.blit(self.image, (self.x2, self.y))
