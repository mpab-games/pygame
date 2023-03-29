from enum import Enum, auto
import math
import pygame
from dataclasses import dataclass

from game_globals import *
from game_sprites import *


class GameState(Enum):
    ATTRACT1 = auto()
    ATTRACT2 = auto()
    SHOW_HIGH_SCORES = auto()
    RUNNING = auto()
    LIFE_LOST = auto()
    GET_READY = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()


@dataclass
class SoundsContext:
    """sounds context."""
    bat: pygame.mixer.Sound
    brick: pygame.mixer.Sound
    life_lost: pygame.mixer.Sound
    game_over: pygame.mixer.Sound
    wall: pygame.mixer.Sound
    get_ready: pygame.mixer.Sound
    level_complete: pygame.mixer.Sound


def sounds_init():
    pygame.mixer.init()
    context = SoundsContext(
        brick=pygame.mixer.Sound("./assets/Pop-sound-effect.mp3"),
        wall=pygame.mixer.Sound(
            "./assets/baseball-bat-hit-sound-effect.mp3"),
        life_lost=pygame.mixer.Sound(
            "./assets/Game-show-buzzer-sound-effect.mp3"),
        game_over=pygame.mixer.Sound(
            "./assets/game-fail-sound-effect.mp3"),
        bat=pygame.mixer.Sound(
            "./assets/bonk-sound-effect.mp3"),
        get_ready=pygame.mixer.Sound(
            "./assets/Ding-sound-effect.mp3"),
        level_complete=pygame.mixer.Sound(
            "./assets/cartoon-xylophone-gliss.mp3")
    )
    return context


@dataclass
class GameContext:
    """game context."""
    game_state: GameState
    level: int
    screen: pygame.Surface
    bat_sprite: Sprite
    ball_sprite: BallSprite
    bottom_border_sprite: Sprite
    bricks: pygame.sprite.Group
    playfield: pygame.sprite.Group
    overlay: pygame.sprite.Group
    clock: pygame.time.Clock
    font_small: pygame.font.Font
    font_medium: pygame.font.Font
    font_large: pygame.font.Font
    score: int
    lives: int
    ball_speed: int
    sounds: SoundsContext
    ticks: int


def add_bricks(group: pygame.sprite.Group):
    # for testing
    # group.add(BrickSprite(220, 100))
    # return
    for row in range(3):
        for col in range(BRICKS_PER_LINE):
            x = (SCREEN_WIDTH / BRICKS_PER_LINE) * col
            y = ((SCREEN_HEIGHT / 20) * row) + SCREEN_HEIGHT / 5
            group.add(BrickSprite(x, y))


def game_init():
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_cursor(
        (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def make_high_scores(ctx: GameContext):
    yoff = ctx.font_medium.get_height() * 2
    ctx.overlay.add(CentredTextScrollingSprite(
        "HIGH SCORES", ctx.font_medium, SCREEN_HEIGHT, (0, -1)))
    ctx.overlay.add(CentredTextScrollingSprite(
        "AAA 10000", ctx.font_medium, SCREEN_HEIGHT + yoff, (0, -1)))
    ctx.overlay.add(CentredTextScrollingSprite(
        "BBB 5000", ctx.font_medium, SCREEN_HEIGHT + yoff * 2, (0, -1)))
    ctx.overlay.add(CentredTextScrollingSprite(
        "CCC 1000", ctx.font_medium, SCREEN_HEIGHT + yoff * 3, (0, -1)))


def reset_ball(ctx: GameContext):
    ctx.ball_speed = ctx.level + 1
    ctx.ball_sprite.velocity = [ctx.ball_speed, ctx.ball_speed]
    ctx.ball_sprite.move_abs(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


def new_game(ctx: GameContext):
    ctx.lives = 3
    ctx.level = 1
    reset_ball(ctx)
    add_bricks(ctx.bricks)


def make_context():
    screen = game_init()
    sounds = sounds_init()
    playfield = pygame.sprite.RenderPlain()
    bricks = pygame.sprite.RenderPlain()
    overlay = pygame.sprite.RenderPlain()

    ball_sprite = BallSprite(ball_shape((0, 0)), sounds.wall)
    playfield.add(ball_sprite)

    bottom_border_sprite = Sprite(border_shape())
    playfield.add(bottom_border_sprite)

    bat_sprite = BatSprite(screen.get_rect().w / 2, screen.get_rect().h - 32)
    playfield.add(bat_sprite)

    font_name = './assets/dogicapixel.ttf'  # NovaMono

    font_small = pygame.font.Font(font_name, 16)
    font_medium = pygame.font.Font(font_name, 24)
    font_large = pygame.font.Font(font_name, 48)
    clock = pygame.time.Clock()

    context = GameContext(
        GameState.ATTRACT1,
        0,
        screen,
        bat_sprite,
        ball_sprite,
        bottom_border_sprite,
        bricks,
        playfield,
        overlay,
        clock,
        font_small,
        font_medium,
        font_large,
        0, 0, 0,  # score, lives, ball_speed
        sounds,
        pygame.time.get_ticks())  # ticks

    return context


def render_screen(ctx: GameContext):
    ctx.screen.fill(SCREEN_COLOR)
    ctx.playfield.draw(ctx.screen)
    ctx.bricks.draw(ctx.screen)

    text = "Level: %s Lives: %s Score: %s" % (ctx.level, ctx.lives, ctx.score)
    text_img = ctx.font_small.render(text, False, (255, 255, 255))
    ctx.screen.blit(text_img, (0, 0))


def handle_player_movement(ctx: GameContext, event: pygame.event.EventType):
    if event.type == pygame.MOUSEMOTION:
        position = event.pos
        ctx.bat_sprite.rect.left = position[0] - \
            ctx.bat_sprite.rect.width / 2


def run_get_ready(ctx: GameContext):
    for event in pygame.event.get():
        handle_player_movement(ctx, event)

    render_screen(ctx)
    draw_banner_text(ctx, "GET READY")

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        set_game_state(ctx, GameState.RUNNING)


def run_life_lost(ctx: GameContext):
    pygame.event.pump()

    render_screen(ctx)
    draw_banner_text(ctx, "OH NO!")

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        ctx.sounds.get_ready.play()
        set_game_state(ctx, GameState.GET_READY)


def run_game(ctx: GameContext):
    for event in pygame.event.get():
        handle_player_movement(ctx, event)

    if pygame.sprite.collide_mask(ctx.bat_sprite, ctx.ball_sprite):
        if (ctx.ball_sprite.velocity[1] > 0):
            ctx.ball_sprite.velocity[1] *= -1
            ctx.sounds.bat.play()

    if pygame.sprite.collide_mask(ctx.bottom_border_sprite, ctx.ball_sprite):
        ctx.lives = ctx.lives - 1

        if (ctx.lives <= 0):
            ctx.sounds.game_over.play()
            ctx.level = 0
            reset_ball(ctx)
            set_game_state(ctx, GameState.GAME_OVER)
            return

        ctx.sounds.life_lost.play()
        reset_ball(ctx)
        set_game_state(ctx, GameState.LIFE_LOST)
        return

    for brick in ctx.bricks:
        if pygame.sprite.collide_mask(ctx.ball_sprite, brick):
            ctx.bricks.remove(brick)
            num_bricks = len(ctx.bricks.sprites())
            # print(num_bricks)
            ctx.ball_sprite.velocity[1] *= -1
            ctx.score = ctx.score + 10
            ctx.sounds.brick.play()
            if (num_bricks == 0):
                ctx.sounds.level_complete.play()
                set_game_state(ctx, GameState.LEVEL_COMPLETE)
                return

    ctx.playfield.update()
    render_screen(ctx)

    # ball speed gets faster over time
    last_ticks = ctx.ticks
    now_ticks = pygame.time.get_ticks()
    if (now_ticks - last_ticks > 20000):  # check every 20 seconds
        ctx.ticks = now_ticks
        ctx.ball_speed = ctx.ball_speed + 1
        if (ctx.ball_speed <= 20):  # maximum speed clamp
            vx = math.copysign(ctx.ball_speed, ctx.ball_sprite.velocity[0])
            vy = math.copysign(ctx.ball_speed, ctx.ball_sprite.velocity[1])
            ctx.ball_sprite.velocity = [vx, vy]

    return True


def draw_banner_text(ctx: GameContext, text):
    letters = ctx.font_large.render(text, False, (255, 255, 255))
    x = (SCREEN_WIDTH - letters.get_rect().width)//2
    y = (SCREEN_HEIGHT - letters.get_rect().height)//2
    ctx.screen.blit(letters, (x, y))


def set_game_state(ctx: GameContext, game_state: GameState):
    ctx.ticks = pygame.time.get_ticks()
    ctx.game_state = game_state


def run_attract1(ctx: GameContext):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            ctx.sounds.get_ready.play()
            set_game_state(ctx, GameState.GET_READY)  # TODO add state NEW_GAME
            new_game(ctx)
            return

    ctx.playfield.update()
    render_screen(ctx)
    draw_banner_text(ctx, "PRESS MOUSE")

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        set_game_state(ctx, GameState.ATTRACT2)


def run_attract2(ctx: GameContext):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            ctx.sounds.get_ready.play()
            set_game_state(ctx, GameState.GET_READY)  # TODO add state NEW_GAME
            new_game(ctx)
            return

    ctx.playfield.update()
    render_screen(ctx)
    draw_banner_text(ctx, "TO START")

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        set_game_state(ctx, GameState.SHOW_HIGH_SCORES)


def run_show_high_scores(ctx: GameContext):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            ctx.sounds.get_ready.play()
            set_game_state(ctx, GameState.GET_READY)  # TODO add state NEW_GAME
            new_game(ctx)
            return

    ctx.playfield.update()
    render_screen(ctx)

    ctx.overlay.draw(ctx.screen)
    ctx.overlay.update()

    if (pygame.time.get_ticks() - ctx.ticks > 10000):
        set_game_state(ctx, GameState.ATTRACT1)


def run_gameover(ctx: GameContext):
    pygame.event.pump()

    render_screen(ctx)
    draw_banner_text(ctx, "GAME OVER")

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        set_game_state(ctx, GameState.ATTRACT1)


def run_level_complete(ctx: GameContext):
    pygame.event.pump()

    render_screen(ctx)
    draw_banner_text(ctx, "LEVEL COMPLETE")

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        ctx.level = ctx.level + 1
        reset_ball(ctx)
        add_bricks(ctx.bricks)
        # TODO add new game state NEXT_LEVEL
        ctx.sounds.get_ready.play()
        set_game_state(ctx, GameState.GET_READY)


def run_game_state(ctx: GameContext):
    if pygame.event.peek(eventtype=pygame.QUIT):
        return False

    match (ctx.game_state):
        case GameState.ATTRACT1:
            run_attract1(ctx)

        case GameState.ATTRACT2:
            run_attract2(ctx)

        case GameState.SHOW_HIGH_SCORES:
            run_show_high_scores(ctx)

        case GameState.RUNNING:
            run_game(ctx)

        case GameState.LIFE_LOST:
            run_life_lost(ctx)

        case GameState.GET_READY:
            run_get_ready(ctx)

        case GameState.GAME_OVER:
            run_gameover(ctx)

        case GameState.LEVEL_COMPLETE:
            run_level_complete(ctx)

    return True


def main():
    ctx = make_context()
    reset_ball(ctx)
    make_high_scores(ctx)

    while (run_game_state(ctx)):
        run_game_state(ctx)
        pygame.display.flip()
        ctx.clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
