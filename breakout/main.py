from enum import Enum, auto
import pygame
from dataclasses import dataclass

from game import sprite, color, shape, constant
from game_collision_logic import rectangular_collision_analyzer


class GameState(Enum):
    ATTRACT = auto()
    SHOW_HIGH_SCORES = auto()
    RUNNING = auto()
    LIFE_LOST = auto()
    GET_READY = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()
    GAME_OVER_HIGH_SCORE = auto()
    ENTER_HIGH_SCORE = auto()


class Ticker():
    def __init__(self):
        self.ticks = pygame.time.get_ticks()
        self.counter_ms = 0

    def tick(self):
        ticks_now = pygame.time.get_ticks()
        ticks_diff = ticks_now - self.ticks
        self.counter_ms = ticks_diff

    def reset(self):
        self.ticks = pygame.time.get_ticks()
        self.counter_ms = 0


@dataclass
class SoundsContext:
    """sounds context."""
    bat: pygame.mixer.Sound
    brick: pygame.mixer.Sound
    life_lost: pygame.mixer.Sound
    game_over: pygame.mixer.Sound
    high_score: pygame.mixer.Sound
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
        high_score=pygame.mixer.Sound(
            './assets/trumpet-cornet-sound.mp3'),
        bat=pygame.mixer.Sound(
            './assets/bonk-sound-effect.mp3'),
        get_ready=pygame.mixer.Sound(
            './assets/notification-melody.mp3'),
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
    level: int
    screen: pygame.Surface
    bat_sprite: sprite.BatSprite
    ball_sprite: sprite.BallSprite
    deadly_border_sprite: sprite.ImageSprite
    animations: pygame.sprite.Group
    playfield: pygame.sprite.Group
    bricks: pygame.sprite.Group
    overlay: pygame.sprite.Group
    clock: pygame.time.Clock
    font_small: pygame.font.Font
    font_medium: pygame.font.Font
    font_large: pygame.font.Font
    score: int
    lives: int
    sounds: SoundsContext
    high_scores: list
    game_state: GameState
    game_state_ticker: Ticker
    bat_ball_debounce_ticker: Ticker
    custom_data: None


def create_game_context():
    screen_rect = pygame.Rect(
        0, 0, constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)
    screen = pygame.display.set_mode((screen_rect.width, screen_rect.height))
    sounds = sounds_init()

    animations = pygame.sprite.RenderPlain()
    playfield = pygame.sprite.RenderPlain()
    bricks = pygame.sprite.RenderPlain()
    overlay = pygame.sprite.RenderPlain()

    deadly_border_sprite = sprite.ImageSprite(shape.deadly_border_shape())
    deadly_border_sprite.move_abs(0, screen_rect.bottom - 4)
    playfield.add(deadly_border_sprite)

    bat_sprite = sprite.BatSprite()
    bat_sprite.move_abs(screen.get_rect().w / 2,
                        screen.get_rect().h - 2 * constant.BRICK_HEIGHT)
    playfield.add(bat_sprite)

    font_name = './assets/arcade-legacy.ttf'

    font_small = pygame.font.Font(font_name, 16)
    font_medium = pygame.font.Font(font_name, 24)
    font_large = pygame.font.Font(font_name, 32)
    clock = pygame.time.Clock()

    high_scores = [("AAA", 100), ('BBB', 50), ('CCC', 10)]

    context = GameContext(
        screen_rect,
        0,
        screen,
        bat_sprite,
        None,
        deadly_border_sprite,
        animations,
        playfield,
        bricks,
        overlay,
        clock,
        font_small,
        font_medium,
        font_large,
        0, 0,  # score, lives
        sounds,
        high_scores,
        None,  # game state
        Ticker(),  # state_ticker
        Ticker(),  # ball_speed_ticker
        None)  # custom_data

    reset_ball(context)

    return context


def add_bricks(gctx: GameContext):
    # for testing
    # group.add(BrickSprite(220, 100))
    # return
    bricks_y_offset = constant.BRICK_HEIGHT * (gctx.level + 5)  # TODO level
    for row in range(constant.NUM_BRICK_ROWS):
        for col in range(constant.BRICKS_PER_ROW):
            x = col * constant.BRICK_WIDTH
            y = bricks_y_offset + row * constant.BRICK_HEIGHT
            brick = sprite.BrickSprite(shape.rectangle_brick_shape(row))
            brick.move_abs(x, y)
            gctx.bricks.add(brick)


def system_init():
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_cursor(
        (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))


def make_vertically_scrolling_text_sprite(font: pygame.font.Font, text: str, gradient_top, gradient_bottom):
    surface = shape.dual_vertical_text_gradient_surface(
        text, font, gradient_top, gradient_bottom)
    return sprite.ScrollingSprite(surface, (0, -1))


def add_high_score_sprites(group: pygame.sprite.Group, font: pygame.font.Font, high_scores: list):
    yoff = font.get_height()

    sprite = make_vertically_scrolling_text_sprite(
        font, "Today's High Scores", color.MIDBLUE_TO_LIGHTBLUE_GRADIENT, color.RED_TO_ORANGE_GRADIENT)
    sprite.move_abs((constant.SCREEN_WIDTH - sprite.rect.width) //
                    2, constant.SCREEN_HEIGHT + yoff)
    group.add(sprite)

    dummy_text_surface = shape.text_surface('abc   0123456789', font)
    xpos = (constant.SCREEN_WIDTH - dummy_text_surface.get_rect().width) // 2
    for idx, (name, score) in enumerate(high_scores):
        justified_name = name.ljust(3, ' ')
        justified_score = str(score).rjust(10, ' ')
        text = justified_name + '   ' + justified_score
        sprite = make_vertically_scrolling_text_sprite(
            font, text, color.ORANGE_TO_GOLD_GRADIENT, color.GOLD_TO_ORANGE_GRADIENT)
        sprite.move_abs(xpos, constant.SCREEN_HEIGHT + yoff * (idx + 3))
        group.add(sprite)


def reset_ball(gctx: GameContext):
    if (gctx.ball_sprite is not None):
        gctx.playfield.remove(gctx.ball_sprite)

    start, velocity, direction = gctx.screen_rect.center, gctx.level + \
        3, (1.0, 1.0)
    ball_sprite = sprite.BallSprite(
        shape.ball_shape(), start, velocity, direction, gctx.screen_rect, gctx.sounds.wall)
    gctx.playfield.add(ball_sprite)
    gctx.ball_sprite = ball_sprite


def new_game(gctx: GameContext):
    gctx.lives = 3
    gctx.level = 1
    gctx.score = 0
    reset_ball(gctx)
    add_bricks(gctx)


def draw_game_screen(gctx: GameContext):
    gctx.screen.fill(color.SCREEN_COLOR)
    gctx.playfield.draw(gctx.screen)
    gctx.bricks.draw(gctx.screen)
    gctx.animations.draw(gctx.screen)

    surface = shape.vertical_text_gradient_surface("Level:%s Lives:%s Score:%s" % (
        gctx.level, gctx.lives, gctx.score), gctx.font_small, color.BRIGHTYELLOW_TO_MIDYELLOW_GRADIENT)
    gctx.screen.blit(surface, (4, 4))


def handle_player_movement(gctx: GameContext, event: pygame.event.EventType):
    if event.type == pygame.MOUSEMOTION:
        position = event.pos
        gctx.bat_sprite.move_abs(
            position[0] - gctx.bat_sprite.rect.width / 2, gctx.bat_sprite.rect.top)


def run_get_ready(gctx: GameContext):
    for event in pygame.event.get():
        handle_player_movement(gctx, event)

    draw_game_screen(gctx)
    blit_centred_banner_text(gctx.screen, "GET READY!", gctx.font_large)

    if (gctx.game_state_ticker.counter_ms >= 2000):
        set_game_state(gctx, GameState.RUNNING)


def run_life_lost(gctx: GameContext):
    pygame.event.pump()

    draw_game_screen(gctx)
    text = "%s LIVES LEFT" % (
        gctx.lives) if gctx.lives != 1 else "%s LIFE LEFT" % (gctx.lives)
    blit_centred_banner_text(gctx.screen, text, gctx.font_large)

    if (gctx.game_state_ticker.counter_ms >= 2000):
        gctx.sounds.get_ready.play()
        set_game_state(gctx, GameState.GET_READY)


def make_high_scores(gctx: GameContext, new_score_name, new_score):
    new_high_scores = gctx.high_scores.copy()
    new_high_scores.append((new_score_name, new_score))
    new_high_scores.sort(key=lambda tup: tup[1], reverse=True)
    return new_high_scores[:3]


def handle_ball_brick_collision_physics(ball: sprite.BallSprite, brick: sprite.ImageSprite):
    (normal, collision_info, collision_rects, _, _,
     _) = rectangular_collision_analyzer(ball, brick)

    # unknown hit box & zero normal is now handled in ball.reflect
    if collision_info == 'unknown':
        print('%s %s %s %s %s' %
              (ball.pos, ball.dir, ball.velocity, ball.rect, brick.rect))

    ball.reflect(normal)


def handle_ball_bat_collision_physics(gctx: GameContext):
    if (gctx.bat_ball_debounce_ticker.counter_ms < 17): # wait 1 frame @ 60 Hz
        return
    gctx.bat_ball_debounce_ticker.reset()

    normal = pygame.math.Vector2(0, -1)

    dx = gctx.bat_sprite.rect.left - gctx.bat_sprite.last_pos[0]
    dir_angle = pygame.math.Vector2(0, 1).angle_to(gctx.ball_sprite.dir)
    english_dir = pygame.math.Vector2(
        (gctx.ball_sprite.dir[0] + dx / 10, gctx.ball_sprite.dir[1])).normalize()
    english_dir_angle = pygame.math.Vector2(0, 1).angle_to(english_dir)

    # print('angle: %s, english angle: %s' % (dir_angle, english_dir_angle))
    if english_dir_angle < -65:
        # print('angle out of bounds')
        english_dir_angle = -65
    if english_dir_angle > 65:
        # print('angle out of bounds')
        english_dir_angle = 65

    new_vec = pygame.math.Vector2()
    new_vec.from_polar((1, english_dir_angle))
    new_vec.normalize()
    clamped_english_dir = pygame.math.Vector2(-new_vec[1], new_vec[0])
    # print('english_dir: %s' % english_dir)
    # print('clamped_english_dir: %s' % clamped_english_dir)

    gctx.ball_sprite.dir = clamped_english_dir
    gctx.ball_sprite.reflect(normal)
    gctx.sounds.bat.play()


def run_game(gctx: GameContext):
    for event in pygame.event.get():
        handle_player_movement(gctx, event)

    if pygame.sprite.collide_mask(gctx.ball_sprite, gctx.bat_sprite):
        handle_ball_bat_collision_physics(gctx)

    if pygame.sprite.collide_mask(gctx.deadly_border_sprite, gctx.ball_sprite):
        gctx.lives = gctx.lives - 1

        if (gctx.lives <= 0):
            gctx.sounds.game_over.play()

            new_high_scores = make_high_scores(gctx, '', gctx.score)
            if (new_high_scores != gctx.high_scores):
                set_game_state(gctx, GameState.GAME_OVER_HIGH_SCORE)
                return

            set_game_state(gctx, GameState.GAME_OVER)
            return

        gctx.sounds.life_lost.play()
        reset_ball(gctx)
        set_game_state(gctx, GameState.LIFE_LOST)
        return

    for brick in gctx.bricks:
        if pygame.sprite.collide_mask(gctx.ball_sprite, brick):
            gctx.bricks.remove(brick)

            destroyed_brick = sprite.DisappearingSprite(
                brick.image, (0, 2), 32)
            bx = brick.rect.left
            by = brick.rect.top
            destroyed_brick.move_abs(brick.rect.left, brick.rect.top)
            gctx.animations.add(destroyed_brick)

            handle_ball_brick_collision_physics(gctx.ball_sprite, brick)
            points_sprite = sprite.DisappearingSprite(shape.vertical_text_gradient_surface(
                '+10', gctx.font_small, color.BRIGHTYELLOW_TO_MIDYELLOW_GRADIENT), (0, -1), 32)
            px = bx + (brick.rect.width - points_sprite.rect.width) // 2
            py = by + brick.rect.height // 2
            points_sprite.move_abs(px, py)
            gctx.animations.add(points_sprite)

            num_bricks = len(gctx.bricks.sprites())
            # print(num_bricks)

            gctx.score = gctx.score + 10
            gctx.sounds.brick.play()
            if (num_bricks == 0):
                gctx.sounds.level_complete.play()
                set_game_state(gctx, GameState.LEVEL_COMPLETE)
                return

    gctx.playfield.update()
    gctx.animations.update()
    draw_game_screen(gctx)

    # ball speed gets faster over time
    if (gctx.game_state_ticker.counter_ms > 20000):
        gctx.game_state_ticker.reset()
        if (gctx.ball_sprite.velocity < 20):  # maximum speed clamp
            gctx.ball_sprite.velocity = gctx.ball_sprite.velocity + 1

    return True


def blit_centred_banner_text(target: pygame.Surface, text: str, font: pygame.font.Font):
    surface = shape.dual_vertical_text_gradient_surface(
        text, font, color.MIDBLUE_TO_LIGHTBLUE_GRADIENT, color.RED_TO_ORANGE_GRADIENT)
    x = (constant.SCREEN_WIDTH - surface.get_rect().width)//2
    y = (constant.SCREEN_HEIGHT - surface.get_rect().height)//2
    target.blit(surface, (x, y))
    return surface


def set_game_state(gctx: GameContext, game_state: GameState):
    gctx.game_state = game_state
    gctx.game_state_ticker.reset()
    gctx.bat_ball_debounce_ticker.reset()
    gctx.custom_data = None


def run_attract(gctx: GameContext):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            gctx.sounds.get_ready.play()
            # TODO add state NEW_GAME
            set_game_state(gctx, GameState.GET_READY)
            new_game(gctx)
            return

    gctx.playfield.update()
    draw_game_screen(gctx)

    text = ''
    if (0 <= gctx.game_state_ticker.counter_ms <= 2000):
        text = 'Press Mouse Button'
    elif (2000 <= gctx.game_state_ticker.counter_ms <= 4000):
        text = 'To Start'
    else:
        set_game_state(gctx, GameState.SHOW_HIGH_SCORES)

    blit_centred_banner_text(gctx.screen, text, gctx.font_large)


def run_show_high_scores(gctx: GameContext):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            gctx.sounds.get_ready.play()
            # TODO add state NEW_GAME
            set_game_state(gctx, GameState.GET_READY)
            new_game(gctx)
            return

    gctx.playfield.update()
    draw_game_screen(gctx)

    gctx.overlay.draw(gctx.screen)
    gctx.overlay.update()

    if (gctx.game_state_ticker.counter_ms >= 10000):
        set_game_state(gctx, GameState.ATTRACT)


def run_gameover(gctx: GameContext):
    pygame.event.pump()

    draw_game_screen(gctx)
    blit_centred_banner_text(gctx.screen, "Game Over", gctx.font_large)

    if (gctx.game_state_ticker.counter_ms >= 2000):
        set_game_state(gctx, GameState.ATTRACT)


def run_gameover_high_score(gctx: GameContext):
    pygame.event.pump()

    draw_game_screen(gctx)
    blit_centred_banner_text(gctx.screen, "Game Over", gctx.font_large)

    if (gctx.game_state_ticker.counter_ms >= 2000):
        set_game_state(gctx, GameState.ENTER_HIGH_SCORE)
        gctx.sounds.high_score.play()


def run_level_complete(gctx: GameContext):
    pygame.event.pump()

    draw_game_screen(gctx)
    gctx.animations.update()
    blit_centred_banner_text(gctx.screen, "LEVEL COMPLETE", gctx.font_large)

    if (gctx.game_state_ticker.counter_ms >= 2000):
        gctx.level = gctx.level + 1
        reset_ball(gctx)
        add_bricks(gctx)
        # TODO add new game state NEXT_LEVEL
        gctx.sounds.get_ready.play()
        set_game_state(gctx, GameState.GET_READY)


def run_enter_high_score(gctx: GameContext):

    if gctx.custom_data is None:
        gctx.custom_data = ''

    score_name: str = gctx.custom_data

    char = ''

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                # TODO add state NEW_GAME
                set_game_state(gctx, GameState.SHOW_HIGH_SCORES)
                gctx.high_scores = make_high_scores(
                    gctx, score_name, gctx.score)
                gctx.overlay = pygame.sprite.RenderPlain()
                add_high_score_sprites(
                    gctx.overlay, gctx.font_medium, gctx.high_scores)
                return

            char = pygame.key.name(event.key)
            if char == 'backspace' and len(score_name):
                score_name = score_name[:-1]
                gctx.sounds.key_press.play()
            elif len(char) == 1 and len(score_name) < 3:
                score_name = score_name + char.upper()
                gctx.sounds.key_press.play()

    gctx.screen.fill(color.SCREEN_COLOR)
    banner_text_surface = blit_centred_banner_text(
        gctx.screen, "New High Score!", gctx.font_large)

    cursor = '_' if (gctx.game_state_ticker.counter_ms // 500) & 1 else ' '
    display_name = score_name + cursor

    surface = shape.dual_vertical_text_gradient_surface(
        display_name, gctx.font_medium, color.ORANGE_TO_GOLD_GRADIENT, color.GOLD_TO_ORANGE_GRADIENT)
    x = (constant.SCREEN_WIDTH - surface.get_rect().width)//2
    y = banner_text_surface.get_rect().height + (constant.SCREEN_HEIGHT -
                                                 surface.get_rect().height)//2
    gctx.screen.blit(surface, (x, y))

    gctx.custom_data = score_name


def run_game_state(gctx: GameContext) -> bool:

    for _ in pygame.event.get(pygame.QUIT):
        return False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        return False

    gctx.game_state_ticker.tick()
    gctx.bat_ball_debounce_ticker.tick()

    match (gctx.game_state):
        case GameState.ATTRACT:
            run_attract(gctx)

        case GameState.SHOW_HIGH_SCORES:
            run_show_high_scores(gctx)

        case GameState.RUNNING:
            run_game(gctx)

        case GameState.LIFE_LOST:
            run_life_lost(gctx)

        case GameState.GET_READY:
            run_get_ready(gctx)

        case GameState.GAME_OVER:
            run_gameover(gctx)

        case GameState.GAME_OVER_HIGH_SCORE:  # kludge
            run_gameover_high_score(gctx)

        case GameState.LEVEL_COMPLETE:
            run_level_complete(gctx)

        case GameState.ENTER_HIGH_SCORE:
            run_enter_high_score(gctx)

    return True


def main():
    system_init()
    gctx = create_game_context()
    reset_ball(gctx)
    add_high_score_sprites(gctx.overlay, gctx.font_medium, gctx.high_scores)

    set_game_state(gctx, GameState.GAME_OVER)
    while (run_game_state(gctx)):
        pygame.display.flip()
        gctx.clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
