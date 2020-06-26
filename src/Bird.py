import pygame
import os

images_path = os.path.abspath(os.getcwd())
images_path += '\\images'

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join(images_path, "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join(images_path, "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join(images_path, "bird3.png")))]
class Bird:
    images = BIRD_IMAGES
    max_rotation = 25
    rot_vel = 20
    change_image_counter = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.image_count = 0              #image count
        self.image = self.images[0]       # image that currently showing

    def jump(self):
        self.vel = -10.5                  #for increase y coordinate we need negative velocity
        self.tick_count = 0               #jump action currently happened
        self.height = self.y

    def move(self):
        self.tick_count += 1              #how many move happened from the last jump

        d = self.vel * self.tick_count + 1.5 * (self.tick_count ** 2)           # this equation provide to change the coordinates of bird with velocity

        if d >= 16:                                     # limit of changing coordinate
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.y + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel

    def draw(self, window):
        self.image_count += 1

        if self.image_count < self.change_image_counter:                      #image will change when 5 draw function called
            self.image = self.images[0]
        elif self.image_count < self.change_image_counter * 2:
            self.image = self.images[1]
        elif self.image_count < self.change_image_counter * 3:
            self.image = self.images[2]
        elif self.image_count < self.change_image_counter * 4:
            self.image = self.images[1]
        elif self.image_count == self.change_image_counter * 4 + 1:
            self.image = self.images[0]
            self.image_count = 0

        if self.tilt <= -80:                                           #bird is diving down
            self.image = self.images[1]
            self.image_count = self.change_image_counter * 2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
