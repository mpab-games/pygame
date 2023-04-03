import pygame


class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()

    def move_abs(self, x, y):
        self.rect.move_ip(x - self.rect.left, y - self.rect.top)


class VecImageSprite(pygame.sprite.Sprite):

    def __init__(self,
                 image: pygame.Surface,
                 startpos: pygame.math.Vector2,
                 velocity: float,
                 startdir: pygame.math.Vector2):
        
        super().__init__()
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect(
            center=(round(self.pos.x), round(self.pos.y)))

    def move_abs(self, x, y):
        self.pos = pygame.math.Vector2((x, y))
        self.rect = self.image.get_rect(
            center=(round(self.pos.x), round(self.pos.y)))

    def reflect(self, normal: pygame.math.Vector2):
        vec_normal = pygame.math.Vector2(normal)
        self.dir = \
            self.dir.reflect(vec_normal) if vec_normal.length() > 0 else self.dir.reflect(self.dir)

