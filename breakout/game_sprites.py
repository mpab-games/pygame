from ast import Tuple
from sprite import *
from game_globals import *
from game_surfaces import *


class BallSprite(Sprite):
    def __init__(self, image_rect_tuple, sound, velocity=[0, 0]):
        super().__init__(image_rect_tuple)
        self.sound = sound
        self.velocity = velocity

    def update(self):
        if self.rect.left < 0 or self.rect.right >= SCREEN_WIDTH:
            self.velocity[0] *= -1
            self.sound.play()
        if self.rect.top < 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity[1] *= -1
            self.sound.play()
        self.rect.move_ip(self.velocity)


class BrickSprite(Sprite):
    def __init__(self, x: int, y: int):
        image_rect_tuple = brick_shape((x, y), (128, 128, 255))
        super().__init__(image_rect_tuple)


class BatSprite(Sprite):
    def __init__(self, x: int, y: int):
        image_rect_tuple = bat_shape((x, y))
        super().__init__(image_rect_tuple)


class ScrollingSprite(Sprite):
    def __init__(self, surface: pygame.Surface, velocity):
        rect = surface.get_rect()
        self.velocity = velocity
        super().__init__((surface, rect))

    def update(self):
        self.rect.move_ip(self.velocity)
        if (self.rect.bottom < 0):
            self.rect.top = SCREEN_HEIGHT
        if (self.rect.left < 0):
            self.rect.left = SCREEN_WIDTH


class DisappearingSprite(Sprite):
    def __init__(self, surface: pygame.Surface, velocity, countdown):
        rect = surface.get_rect()
        self.velocity = velocity
        self.countdown = countdown
        super().__init__((surface, rect))

    def update(self):
        self.rect.move_ip(self.velocity)
        self.countdown = self.countdown - 1
        if (self.countdown <= 0):
            self.kill()
