import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_rect_tuple):
        super(Sprite, self).__init__()
        (self.image, self.rect) = image_rect_tuple

    def move_abs(self, x, y):
        self.rect.move_ip(x - self.rect.left, y - self.rect.top)
