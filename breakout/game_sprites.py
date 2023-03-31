from ast import Tuple
from game_types import *
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


class CentredScrollingTextSpriteWithShadow(Sprite):
    def __init__(self, text: str, font: pygame.font.Font, y: int, velocity):
        letters = font.render(text, False, (255, 255, 255))
        shadow = font.render(text, False, (0, 0, 0))

        w = letters.get_rect().width + 2
        h = letters.get_rect().height + 2

        text_surface = pygame.Surface([w, h])
        text_surface.fill(SCREEN_FILL_COLOR)
        text_surface.blit(shadow, (0, 0))
        text_surface.blit(shadow, (2, 0))
        text_surface.blit(shadow, (0, 2))
        text_surface.blit(shadow, (2, 2))
        text_surface.blit(letters, (1, 1))

        x = (SCREEN_WIDTH - text_surface.get_rect().width)//2
        rect = text_surface.get_rect()
        rect.centerx = x + w // 2
        rect.centery = y + h // 2

        self.velocity = velocity

        super().__init__((text_surface, rect))

    def update(self):
        self.rect.move_ip(self.velocity)
        if (self.rect.bottom < 0):
            self.rect.top = SCREEN_HEIGHT


class CentredTextScrollingSprite(Sprite):
    def __init__(self, text: str, font: pygame.font.Font, y: int, velocity):
        text_surface = font.render(text, False, (255, 255, 255))

        w = text_surface.get_rect().width
        h = text_surface.get_rect().height

        x = (SCREEN_WIDTH - text_surface.get_rect().width)//2
        rect = text_surface.get_rect()
        rect.centerx = x + w // 2
        rect.centery = y + h // 2

        self.velocity = velocity

        super().__init__((text_surface, rect))

    def update(self):
        self.rect.move_ip(self.velocity)
        if (self.rect.bottom < 0):
            self.rect.top = SCREEN_HEIGHT


class ScrollingSprite(Sprite):
    def __init__(self, surface: pygame.Surface, x, y: int, velocity):

        w = surface.get_rect().width
        h = surface.get_rect().height
        rect = surface.get_rect()
        rect.centerx = w // 2
        rect.centery = y + h // 2

        self.velocity = velocity

        super().__init__((surface, rect))

    def update(self):
        self.rect.move_ip(self.velocity)
        if (self.rect.bottom < 0):
            self.rect.top = SCREEN_HEIGHT
