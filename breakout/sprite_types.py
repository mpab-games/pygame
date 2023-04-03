import pygame


class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()

    def move_abs(self, x, y):
        self.rect.move_ip(x - self.rect.left, y - self.rect.top)


class VecImageSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, velocity: float, direction: pygame.math.Vector2):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()

        self.pos = pygame.math.Vector2((0, 0))
        self.velocity = velocity
        self.direction = pygame.math.Vector2(direction).normalize()

    def move_abs(self, x, y):
        self.rect.move_ip(x - self.pos[0], y - self.pos[1])
