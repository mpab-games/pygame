from sprite_types import *
from game_globals import *
from game_images import *


class BallSprite(VecImageSprite):

    def __init__(self,
                 image: pygame.image,
                 startpos: pygame.math.Vector2,
                 velocity: float,
                 startdir: pygame.math.Vector2,
                 frame: pygame.rect.Rect,
                 rect_collision_sound: pygame.mixer.Sound):
        super().__init__(image, startpos, velocity, startdir)
        self.frame = frame
        self.rect_collision_sound = rect_collision_sound

    def update(self):
        new_vel = pygame.math.Vector2(self.dir * self.velocity)
        self.pos += new_vel
        self.rect.center = round(self.pos.x), round(self.pos.y)

        if self.rect.left <= self.frame.left:
            self.rect_collision_sound.play()
            self.reflect((1, 0))
        if self.rect.right >= self.frame.right:
            self.rect_collision_sound.play()
            self.reflect((-1, 0))
        if self.rect.top <= self.frame.top:
            self.rect_collision_sound.play()
            self.reflect((0, 1))
        if self.rect.bottom >= self.frame.bottom:
            self.rect_collision_sound.play()
            self.reflect((0, -1))
        self.rect.clamp_ip(self.frame)


class BrickSprite(ImageSprite):
    def __init__(self, image: pygame.image):
        super().__init__(image)


class BatSprite(ImageSprite):
    def __init__(self):
        image = bat_shape()
        super().__init__(image)


class ScrollingSprite(ImageSprite):
    def __init__(self, surface: pygame.Surface, velocity):
        rect = surface.get_rect()
        self.velocity = velocity
        super().__init__(surface)

    def update(self):
        self.rect.move_ip(self.velocity)
        if (self.rect.bottom < 0):
            self.rect.top = SCREEN_HEIGHT
        if (self.rect.left < 0):
            self.rect.left = SCREEN_WIDTH


class DisappearingSprite(ImageSprite):
    def __init__(self, surface: pygame.Surface, velocity, countdown):
        rect = surface.get_rect()
        self.velocity = velocity
        self.countdown = countdown
        super().__init__((surface))

    def update(self):
        self.rect.move_ip(self.velocity)
        self.countdown = self.countdown - 1
        if (self.countdown <= 0):
            self.kill()
