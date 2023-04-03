from sprite_types import *
from game_globals import *
from game_surfaces import *


class xBallSprite(VecImageSprite):
    def __init__(self, image: pygame.Surface, velocity: float, direction: pygame.math.Vector2, frame: pygame.rect.Rect, rect_collision_sound: pygame.mixer.Sound):
        super().__init__(image, velocity, direction)
        self.rect_collision_sound = rect_collision_sound
        self.frame = frame
        
        print ('---------------')
        print (type(self.pos))
        print (type(self.direction))
        print (type(self.velocity))

    def reflect(self, normal: pygame.math.Vector2):
        self.direction = self.direction.reflect(normal)

    def update(self):
        self.pos += self.direction * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def xupdate(self):
        self.pos += self.direction * self.velocity
        if self.rect.left <= self.frame.left:
            self.reflect(1, 0)
            self.rect_collision_sound.play()
        if self.rect.right >= self.frame.right:
            self.reflect(-1, 0)
            self.rect_collision_sound.play()
        if self.rect.top <= self.frame.top:
            self.reflect(0, 1)
            self.rect_collision_sound.play()
        if self.rect.bottom >= self.frame.bottom:
            self.reflect(0, -1)
            self.rect_collision_sound.play()
        self.rect.clamp_ip(self.frame)


class BrickSprite(ImageSprite):
    def __init__(self):
        image = brick_shape(BRICK_FILL_COLOR)
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
