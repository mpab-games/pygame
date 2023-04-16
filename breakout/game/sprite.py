import pygame

from game import shape, constant

class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.last_pos = (0, 0)

    def move_abs(self, x, y):
        self.last_pos = (self.rect.left, self.rect.top)
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
        if normal is None:
            return
        vec_normal = pygame.math.Vector2(normal)
        self.dir = \
            self.dir.reflect(vec_normal) if vec_normal.length(
            ) > 0 else self.dir.reflect(self.dir)

class BallSprite(VecImageSprite):

    def __init__(self,
                 image: pygame.image,
                 startpos: pygame.math.Vector2,
                 velocity: float,
                 startdir: pygame.math.Vector2,
                 bounds: pygame.rect.Rect,
                 rect_collision_sound: pygame.mixer.Sound):
        super().__init__(image, startpos, velocity, startdir)
        self.bounds = bounds
        self.rect_collision_sound = rect_collision_sound

    def update(self):
        new_vel = pygame.math.Vector2(self.dir * self.velocity)
        self.pos += new_vel
        self.rect.center = round(self.pos.x), round(self.pos.y)

        if self.rect.left <= self.bounds.left:
            self.rect_collision_sound.play()
            self.reflect((1, 0))
        if self.rect.right >= self.bounds.right:
            self.rect_collision_sound.play()
            self.reflect((-1, 0))
        if self.rect.top <= self.bounds.top:
            self.rect_collision_sound.play()
            self.reflect((0, 1))
        if self.rect.bottom >= self.bounds.bottom:
            self.rect_collision_sound.play()
            self.reflect((0, -1))
        self.rect.clamp_ip(self.bounds)


class BrickSprite(ImageSprite):
    def __init__(self, image: pygame.image):
        super().__init__(image)


class BatSprite(ImageSprite):
    def __init__(self):
        image = shape.bat_shape()
        super().__init__(image)


class ScrollingSprite(ImageSprite):
    def __init__(self, surface: pygame.Surface, velocity):
        self.velocity = velocity
        super().__init__(surface)

    def update(self):
        self.rect.move_ip(self.velocity)
        if (self.rect.bottom < 0):
            self.rect.top = constant.SCREEN_HEIGHT
        if (self.rect.left < 0):
            self.rect.left = constant.SCREEN_WIDTH


class DisappearingSprite(ImageSprite):
    def __init__(self, surface: pygame.Surface, velocity, countdown):
        self.velocity = velocity
        self.countdown = countdown
        super().__init__((surface))

    def update(self):
        self.rect.move_ip(self.velocity)
        self.countdown = self.countdown - 1
        if (self.countdown <= 0):
            self.kill()
