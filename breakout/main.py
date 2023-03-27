from enum import Enum
import math
import pygame
from dataclasses import dataclass

from game_globals import *
from game_shapes import *
from game_types import *


class GameState(Enum):
    ATTRACT = 1
    RUNNING = 2
    GAME_OVER = 3


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


@dataclass
class SoundsContext:
    """sounds context."""
    bat: pygame.mixer.Sound
    brick: pygame.mixer.Sound
    lose_a_life: pygame.mixer.Sound
    game_over: pygame.mixer.Sound
    wall: pygame.mixer.Sound


def sounds_init():
    pygame.mixer.init()
    context = SoundsContext(
        brick=pygame.mixer.Sound("./resources/Pop-sound-effect.mp3"),
        wall=pygame.mixer.Sound(
            "./resources/baseball-bat-hit-sound-effect.mp3"),
        lose_a_life=pygame.mixer.Sound(
            "./resources/Game-show-buzzer-sound-effect.mp3"),
        game_over=pygame.mixer.Sound(
            "./resources/game-fail-sound-effect.mp3"),
        bat=pygame.mixer.Sound(
            "./resources/bonk-sound-effect.mp3")
    )
    return context


@dataclass
class GameContext:
    """game context."""
    state: GameState
    level: int
    screen: pygame.Surface
    bat_sprite: Sprite
    ball_sprite: BallSprite
    bottom_border_sprite: Sprite
    bricks: pygame.sprite.Group
    playfield: pygame.sprite.Group
    clock: pygame.time.Clock
    font_small: pygame.font.Font
    font_large: pygame.font.Font
    score: int
    lives: int
    ball_speed: int
    sounds: SoundsContext
    ticks: int


def add_brick_sprites(group):
    for row in range(3):
        for col in range(20):
            x = (SCREEN_WIDTH / 20) * col
            y = ((SCREEN_HEIGHT / 20) * row) + SCREEN_HEIGHT / 5
            group.add(Sprite(brick_shape((x, y), (128, 128, 255))))


def game_init():
    pygame.init()
    pygame.font.init()
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def reset_ball(ctx: GameContext):
    ctx.ball_speed = ctx.level + 1
    ctx.ball_sprite.velocity = [ctx.ball_speed, ctx.ball_speed]
    ctx.ball_sprite.move_abs(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

def new_game(ctx: GameContext):
    ctx.lives = 3
    ctx.level = 1
    reset_ball(ctx)
    add_brick_sprites(ctx.bricks)
    ctx.state = GameState.RUNNING


def make_context():
    screen = game_init()
    sounds = sounds_init()
    playfield = pygame.sprite.RenderPlain()
    bricks = pygame.sprite.RenderPlain()

    ball_sprite = BallSprite(ball_shape((0, 0)), sounds.wall)
    playfield.add(ball_sprite)

    bottom_border_sprite = Sprite(border_shape())
    playfield.add(bottom_border_sprite)

    bat_sprite = Sprite(
        bat_shape((screen.get_rect().w / 2, screen.get_rect().h - 32)))
    playfield.add(bat_sprite)

    font_small = pygame.font.SysFont('NovaMono', 32)
    font_large = pygame.font.SysFont('NovaMono', 96)
    clock = pygame.time.Clock()

    context = GameContext(
        GameState.ATTRACT,
        0,
        screen,
        bat_sprite,
        ball_sprite,
        bottom_border_sprite,
        bricks,
        playfield,
        clock,
        font_small,
        font_large,
        0, 0, 0,  # score, lives, ball_speed
        sounds,
        pygame.time.get_ticks()) # ticks

    return context

def render_screen(ctx: GameContext):
    ctx.screen.fill(SCREEN_COLOR)
    ctx.playfield.draw(ctx.screen)
    ctx.bricks.draw(ctx.screen)

    text = "Level: %s Lives: %s Score: %s" % (ctx.level, ctx.lives, ctx.score)
    text_img = ctx.font_small.render(text, False, (255, 255, 255))
    ctx.screen.blit(text_img, (0, 0))

def run_game(ctx: GameContext):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEMOTION:
            position = event.pos
            ctx.bat_sprite.rect.left = position[0] - \
                ctx.bat_sprite.rect.width / 2

    if pygame.sprite.collide_mask(ctx.bat_sprite, ctx.ball_sprite):
        if (ctx.ball_sprite.velocity[1] > 0):
            ctx.ball_sprite.velocity[1] *= -1
            ctx.sounds.bat.play()

    if pygame.sprite.collide_mask(ctx.bottom_border_sprite, ctx.ball_sprite):
        ctx.lives = ctx.lives - 1
        ctx.sounds.lose_a_life.play()
        pygame.time.delay(1000)

        if (ctx.lives <= 0):
            ctx.sounds.game_over.play()
            pygame.time.delay(2000)
            ctx.state = GameState.GAME_OVER
            return True
        
        reset_ball(ctx)

    for brick in ctx.bricks:
        if pygame.sprite.collide_mask(ctx.ball_sprite, brick):
            ctx.bricks.remove(brick)
            ctx.ball_sprite.velocity[1] *= -1
            ctx.score = ctx.score + 10
            ctx.sounds.brick.play()

    ctx.playfield.update()
    render_screen(ctx)

    # ball speed gets faster over time
    last_ticks = ctx.ticks
    now_ticks = pygame.time.get_ticks()
    if (now_ticks - last_ticks > 20000): # check every 20 seconds
        ctx.ticks = now_ticks
        ctx.ball_speed = ctx.ball_speed + 1
        if (ctx.ball_speed <= 20): # maximum speed clamp
            vx = math.copysign(ctx.ball_speed, ctx.ball_sprite.velocity[0])
            vy = math.copysign(ctx.ball_speed, ctx.ball_sprite.velocity[1])
            ctx.ball_sprite.velocity = [vx, vy]

    return True

def draw_banner_text(ctx: GameContext, text):
    letters = ctx.font_large.render(text, False, (255, 255, 255))
    shadow = ctx.font_large.render(text, False, (128, 128, 128))
    x = (SCREEN_WIDTH - letters.get_rect().width)//2
    y = (SCREEN_HEIGHT - letters.get_rect().height)//2
    ctx.screen.blit(shadow, (x-1, y-1))
    ctx.screen.blit(shadow, (x-1, y+1))
    ctx.screen.blit(shadow, (x+1, y-1))
    ctx.screen.blit(shadow, (x+1, y+1))
    ctx.screen.blit(letters, (x, y))

def run_attract(ctx: GameContext):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.lives = 0
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            new_game(ctx)
            return True

    ctx.playfield.update()
    render_screen(ctx)
    draw_banner_text(ctx, "PRESS MOUSE")

    last_ticks = ctx.ticks
    now_ticks = pygame.time.get_ticks()
    if (now_ticks - last_ticks > 2000):
        ctx.ticks = now_ticks
        ctx.state = GameState.GAME_OVER

    return True


def run_gameover(ctx: GameContext):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.lives = 0
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            new_game(ctx)
            return True

    ctx.playfield.update()
    render_screen(ctx)
    draw_banner_text(ctx, "GAME OVER")

    last_ticks = ctx.ticks
    now_ticks = pygame.time.get_ticks()
    if (now_ticks - last_ticks > 2000):
        ctx.ticks = now_ticks
        ctx.state = GameState.ATTRACT

    return True


def run_game_state(ctx: GameContext):
    match (ctx.state):
        case GameState.ATTRACT:
            return run_attract(ctx)

        case GameState.RUNNING:
            return run_game(ctx)

        case GameState.GAME_OVER:
            return run_gameover(ctx)


def main():
    ctx = make_context()
    reset_ball(ctx)

    while (run_game_state(ctx)):
        pygame.display.flip()
        ctx.clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
