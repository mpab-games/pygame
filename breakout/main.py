from enum import Enum, auto
import pygame
from dataclasses import dataclass

from game_globals import *
from game_sprites import *
from game_collision_logic import get_collision_normal

class GameState(Enum):
    ATTRACT1 = auto()
    ATTRACT2 = auto()
    SHOW_HIGH_SCORES = auto()
    RUNNING = auto()
    LIFE_LOST = auto()
    GET_READY = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()
    GAME_OVER_HIGH_SCORE = auto()
    ENTER_SCORE = auto()


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
    key_press: pygame.mixer.Sound


def sounds_init():
    pygame.mixer.init()
    context = SoundsContext(
        brick=pygame.mixer.Sound('./assets/Pop-sound-effect.mp3'),
        wall=pygame.mixer.Sound(
            './assets/baseball-bat-hit-sound-effect.mp3'),
        life_lost=pygame.mixer.Sound(
            './assets/Game-show-buzzer-sound-effect.mp3'),
        game_over=pygame.mixer.Sound(
            './assets/game-fail-sound-effect.mp3'),
        bat=pygame.mixer.Sound(
            './assets/bonk-sound-effect.mp3'),
        get_ready=pygame.mixer.Sound(
            './assets/Ding-sound-effect.mp3'),
        level_complete=pygame.mixer.Sound(
            './assets/cartoon-xylophone-gliss.mp3'),
        key_press=pygame.mixer.Sound(
            './assets/machine-button-being-pressed-sound-effect.mp3')
    )
    return context


@dataclass
class GameContext:
    """game context."""
    screen_rect: pygame.Rect
    game_state: GameState
    level: int
    screen: pygame.Surface
    bat_sprite: ImageSprite
    ball_sprite: BallSprite
    bottom_border_sprite: ImageSprite
    bricks: pygame.sprite.Group
    underlay: pygame.sprite.Group
    playfield: pygame.sprite.Group
    overlay: pygame.sprite.Group
    clock: pygame.time.Clock
    font_small: pygame.font.Font
    font_medium: pygame.font.Font
    font_large: pygame.font.Font
    score: int
    lives: int
    sounds: SoundsContext
    ticks: int
    high_scores: list
    score_name: str  # TODO replace with k, v dictionary per state


def make_context(state: GameState):
    screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = game_init(screen_rect)
    sounds = sounds_init()
    playfield = pygame.sprite.RenderPlain()
    bricks = pygame.sprite.RenderPlain()
    overlay = pygame.sprite.RenderPlain()
    underlay = pygame.sprite.RenderPlain()

    deadly_border_sprite = ImageSprite(deadly_border_shape())
    deadly_border_sprite.move_abs(0, screen_rect.bottom - 4)
    playfield.add(deadly_border_sprite)

    bat_sprite = BatSprite()
    bat_sprite.move_abs(screen.get_rect().w / 2, screen.get_rect().h - 32)
    playfield.add(bat_sprite)

    font_name = './assets/AtariFontFullVersion-ZJ23.ttf'

    font_small = pygame.font.Font(font_name, 16)
    font_medium = pygame.font.Font(font_name, 24)
    font_large = pygame.font.Font(font_name, 32)
    clock = pygame.time.Clock()

    high_scores = [("AAA", 100), ('BBB', 50), ('CCC', 10)]

    context = GameContext(
        screen_rect,
        state,
        0,
        screen,
        bat_sprite,
        None,
        deadly_border_sprite,
        bricks,
        underlay,
        playfield,
        overlay,
        clock,
        font_small,
        font_medium,
        font_large,
        0, 3,  # score, lives
        sounds,
        pygame.time.get_ticks(),  # ticks
        high_scores,
        '')

    reset_ball(context)

    return context


def add_bricks(group: pygame.sprite.Group):
    # for testing
    # group.add(BrickSprite(220, 100))
    # return
    for row in range(3):
        for col in range(BRICKS_PER_LINE):
            x = (SCREEN_WIDTH / BRICKS_PER_LINE) * col
            y = ((SCREEN_HEIGHT / 20) * row) + SCREEN_HEIGHT / 5
            brick = BrickSprite(rectangle_brick_shape(BRICK_FILL_COLOR))
            brick.move_abs(x, y)
            group.add(brick)


def game_init(screen_rect: pygame.Rect):
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_cursor(
        (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    return pygame.display.set_mode((screen_rect.width, screen_rect.height))


def make_vertically_scrolling_text_sprite(font: pygame.font.Font, text: str, gradient_top, gradient_bottom):
    surface = dual_vertical_text_gradient_surface(
        text, font, gradient_top, gradient_bottom)
    return ScrollingSprite(surface, (0, -1))


def add_high_score_sprites(group: pygame.sprite.Group, font: pygame.font.Font, high_scores: list):
    yoff = font.get_height() * 1.5

    sprite = make_vertically_scrolling_text_sprite(
        font, "Today's High Scores", MIDBLUE_TO_LIGHTBLUE_GRADIENT, RED_TO_ORANGE_GRADIENT)
    sprite.move_abs((SCREEN_WIDTH - sprite.rect.width) //
                    2, SCREEN_HEIGHT + yoff)
    group.add(sprite)

    xpos = None
    for idx, (name, score) in enumerate(high_scores):
        text = "%s  %s" % (name, score)
        sprite = make_vertically_scrolling_text_sprite(
            font, text, ORANGE_TO_GOLD_GRADIENT, GOLD_TO_ORANGE_GRADIENT)
        if xpos == None:
            xpos = (SCREEN_WIDTH - sprite.rect.width) // 2
        sprite.move_abs(xpos, SCREEN_HEIGHT + yoff * (idx + 3))
        group.add(sprite)


def reset_ball(ctx: GameContext):
    if (ctx.ball_sprite is not None):
        ctx.playfield.remove(ctx.ball_sprite)

    start, velocity, direction = ctx.screen_rect.center, ctx.level + \
        3, (1.0, 1.0)
    ball_sprite = BallSprite(
        ball_shape(), start, velocity, direction, ctx.screen_rect, ctx.sounds.wall)
    ctx.playfield.add(ball_sprite)
    ctx.ball_sprite = ball_sprite


def new_game(ctx: GameContext):
    ctx.lives = 3
    ctx.level = 1
    reset_ball(ctx)
    add_bricks(ctx.bricks)


def render_screen(ctx: GameContext):
    ctx.screen.fill(SCREEN_FILL_COLOR)
    ctx.playfield.draw(ctx.screen)
    ctx.bricks.draw(ctx.screen)
    ctx.underlay.draw(ctx.screen)

    surface = vertical_text_gradient_surface("Level:%s Lives:%s Score:%s" % (
        ctx.level, ctx.lives, ctx.score), ctx.font_small, BRIGHTYELLOW_TO_MIDYELLOW_GRADIENT)
    ctx.screen.blit(surface, (4, 4))


def handle_player_movement(ctx: GameContext, event: pygame.event.EventType):
    if event.type == pygame.MOUSEMOTION:
        position = event.pos
        ctx.bat_sprite.rect.left = position[0] - \
            ctx.bat_sprite.rect.width / 2


def run_get_ready(ctx: GameContext):
    for event in pygame.event.get():
        handle_player_movement(ctx, event)

    render_screen(ctx)
    blit_centred_banner_text(ctx.screen, "GET READY!", ctx.font_large)

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        set_game_state(ctx, GameState.RUNNING)


def run_life_lost(ctx: GameContext):
    pygame.event.pump()

    render_screen(ctx)
    text = "%s LIVES LEFT" % (
        ctx.lives) if ctx.lives != 1 else "%s LIFE LEFT" % (ctx.lives)
    blit_centred_banner_text(ctx.screen, text, ctx.font_large)

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        ctx.sounds.get_ready.play()
        set_game_state(ctx, GameState.GET_READY)


def make_high_scores(ctx: GameContext):
    new_high_scores = ctx.high_scores.copy()
    new_high_scores.append((ctx.score_name, ctx.score))
    new_high_scores.sort(key=lambda tup: tup[1], reverse=True)
    return new_high_scores[:3]


def handle_ball_brick_collision_physics(ball: BallSprite, brick: ImageSprite):
    (collision_info, normal) = get_collision_normal(ball, brick)

    if collision_info == 'unknown': # TODO BUG
        print ('%s %s %s %s %s' % (ball.pos, ball.dir, ball.velocity, ball.rect, brick.rect))

    ball.reflect(normal)


def run_game(ctx: GameContext):
    for event in pygame.event.get():
        handle_player_movement(ctx, event)

    if pygame.sprite.collide_mask(ctx.bat_sprite, ctx.ball_sprite):
        ctx.ball_sprite.reflect((0, -1))
        ctx.sounds.bat.play()

    if pygame.sprite.collide_mask(ctx.bottom_border_sprite, ctx.ball_sprite):
        ctx.lives = ctx.lives - 1

        if (ctx.lives <= 0):
            ctx.sounds.game_over.play()
            ctx.level = 0
            reset_ball(ctx)

            new_high_scores = make_high_scores(ctx)
            if (new_high_scores != ctx.high_scores):
                set_game_state(ctx, GameState.GAME_OVER_HIGH_SCORE)
                return

            set_game_state(ctx, GameState.GAME_OVER)
            return

        ctx.sounds.life_lost.play()
        reset_ball(ctx)
        set_game_state(ctx, GameState.LIFE_LOST)
        return

    for brick in ctx.bricks:
        if pygame.sprite.collide_mask(ctx.ball_sprite, brick):
            ctx.bricks.remove(brick)

            destroyed_brick = DisappearingSprite(brick.image, (0, 2), 32)
            bx = brick.rect.left
            by = brick.rect.top
            destroyed_brick.move_abs(brick.rect.left, brick.rect.top)
            ctx.underlay.add(destroyed_brick)

            handle_ball_brick_collision_physics(ctx.ball_sprite, brick)
            points_sprite = DisappearingSprite(vertical_text_gradient_surface(
                '+10', ctx.font_small, BRIGHTYELLOW_TO_MIDYELLOW_GRADIENT), (0, -1), 32)
            px = bx + (brick.rect.width - points_sprite.rect.width) // 2
            py = by + brick.rect.height // 2
            points_sprite.move_abs(px, py)
            ctx.underlay.add(points_sprite)

            num_bricks = len(ctx.bricks.sprites())
            # print(num_bricks)
            # treat the collision as two balls bouncing off each other, but one is fixed

            ctx.score = ctx.score + 10
            ctx.sounds.brick.play()
            if (num_bricks == 0):
                ctx.sounds.level_complete.play()
                set_game_state(ctx, GameState.LEVEL_COMPLETE)
                return

    ctx.playfield.update()
    ctx.underlay.update()
    render_screen(ctx)

    # ball speed gets faster over time
    last_ticks = ctx.ticks
    now_ticks = pygame.time.get_ticks()
    if (now_ticks - last_ticks > 20000):  # check every 20 seconds
        ctx.ticks = now_ticks
        ball_speed = ctx.ball_sprite.velocity + 1
        if (ball_speed <= 20):  # maximum speed clamp
            ctx.ball_sprite.velocity = ball_speed

    return True


def blit_centred_banner_text(target: pygame.Surface, text: str, font: pygame.font.Font):
    surface = dual_vertical_text_gradient_surface(
        text, font, MIDBLUE_TO_LIGHTBLUE_GRADIENT, RED_TO_ORANGE_GRADIENT)
    x = (SCREEN_WIDTH - surface.get_rect().width)//2
    y = (SCREEN_HEIGHT - surface.get_rect().height)//2
    target.blit(surface, (x, y))
    return surface


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
    blit_centred_banner_text(ctx.screen, "Press Mouse Button", ctx.font_large)

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
    blit_centred_banner_text(ctx.screen, "To Start", ctx.font_large)

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
    blit_centred_banner_text(ctx.screen, "Game Over", ctx.font_large)

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        set_game_state(ctx, GameState.ATTRACT1)


def run_gameover_high_score(ctx: GameContext):
    pygame.event.pump()

    render_screen(ctx)
    blit_centred_banner_text(ctx.screen, "Game Over", ctx.font_large)

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        set_game_state(ctx, GameState.ENTER_SCORE)


def run_level_complete(ctx: GameContext):
    pygame.event.pump()

    render_screen(ctx)
    ctx.underlay.update()
    blit_centred_banner_text(ctx.screen, "LEVEL COMPLETE", ctx.font_large)

    if (pygame.time.get_ticks() - ctx.ticks > 2000):
        ctx.level = ctx.level + 1
        reset_ball(ctx)
        add_bricks(ctx.bricks)
        # TODO add new game state NEXT_LEVEL
        ctx.sounds.get_ready.play()
        set_game_state(ctx, GameState.GET_READY)


def run_enter_score(ctx: GameContext):
    char = ''

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                # TODO add state NEW_GAME
                set_game_state(ctx, GameState.SHOW_HIGH_SCORES)
                ctx.high_scores = make_high_scores(ctx)
                ctx.overlay = pygame.sprite.RenderPlain()
                add_high_score_sprites(
                    ctx.overlay, ctx.font_medium, ctx.high_scores)
                ctx.score_name = ''
                return

            char = pygame.key.name(event.key)

            if char == 'backspace' and len(ctx.score_name):
                ctx.score_name = ctx.score_name[:-1]
                ctx.sounds.key_press.play()

            if len(char) == 1 and len(ctx.score_name) < 3:
                ctx.score_name = ctx.score_name + char
                ctx.sounds.key_press.play()

    ctx.screen.fill(SCREEN_FILL_COLOR)
    banner_text_surface = blit_centred_banner_text(
        ctx.screen, "New High Score!", ctx.font_large)

    display_name = ctx.score_name + '_'

    surface = dual_vertical_text_gradient_surface(
        display_name, ctx.font_medium, ORANGE_TO_GOLD_GRADIENT, GOLD_TO_ORANGE_GRADIENT)
    x = (SCREEN_WIDTH - surface.get_rect().width)//2
    y = banner_text_surface.get_rect().height + (SCREEN_HEIGHT -
                                                 surface.get_rect().height)//2
    ctx.screen.blit(surface, (x, y))


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

        case GameState.GAME_OVER_HIGH_SCORE:  # kludge
            run_gameover_high_score(ctx)

        case GameState.LEVEL_COMPLETE:
            run_level_complete(ctx)

        case GameState.ENTER_SCORE:
            run_enter_score(ctx)

    return True


def main():
    ctx = make_context(GameState.GAME_OVER)
    reset_ball(ctx)
    add_high_score_sprites(ctx.overlay, ctx.font_medium, ctx.high_scores)

    while (run_game_state(ctx)):
        pygame.display.flip()
        ctx.clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
