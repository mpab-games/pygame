import pygame
import os
from game_globals import *
from sprite import Sprite

from collections import namedtuple
GameSettings = namedtuple(
    "GameSettings",
    "level screen bat_sprite ball_sprite bottom_border_sprite bricks playfield clock font")


def png_ball(pos):
    image = pygame.image.load(os.path.join('resources', 'ball.png'))
    rect = image.get_rect()
    rect.center = pos
    return rect, image


def ball_shape(pos):
    radius = 8
    image = pygame.Surface([radius*2, radius*2])
    image.fill(SCREEN_COLOR)
    rect = image.get_rect()
    rect.center = pos
    pygame.draw.circle(image, BALL_COLOR, (radius, radius), radius)
    image.set_colorkey(SCREEN_COLOR)
    return rect, image


def bat_shape(pos):
    width = 80
    height = 16
    image = pygame.Surface([width, height])
    image.fill(SCREEN_COLOR)
    rect = image.get_rect()
    rect.center = pos
    pygame.draw.rect(image, BAT_COLOR, (0, 0, width, height))
    return rect, image


def border_shape():
    image = pygame.Surface([SCREEN_WIDTH, 1])
    image.fill(BALL_COLOR)
    rect = image.get_rect()
    rect.bottom = SCREEN_HEIGHT
    return rect, image


def brick_shape(pos, fill_color):
    dark_color = (0, 0, 0)
    bright_color = (255, 255, 255)

    width = SCREEN_WIDTH / 20
    height = SCREEN_HEIGHT / 20
    image = pygame.Surface([width, height])
    image.fill(SCREEN_COLOR)
    rect = image.get_rect()
    # rect.center = pos
    rect.centerx = pos[0] + width / 2
    rect.centery = pos[1] + height / 2
    pygame.draw.rect(image, fill_color, (0, 0, width, height))

    pygame.draw.line(image, dark_color, (0, height - 2),
                     (width - 2, height - 2), 2)
    pygame.draw.line(image, dark_color, (width - 2, 0),
                     (width - 2, height - 2), 2)

    pygame.draw.line(image, bright_color, (0, 0), (width - 2, 0), 2)
    pygame.draw.line(image, bright_color, (0, 0), (0, height - 2), 2)
    return rect, image


def add_brick_sprites(group):
    for row in range(3):
        for col in range(20):
            x = (SCREEN_WIDTH / 20) * col
            y = ((SCREEN_HEIGHT / 20) * row) + SCREEN_HEIGHT / 5
            group.add(Sprite(brick_shape((x, y), (128, 128, 255))))


def game_init():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Sprite Test")
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def make_level(level):
    screen = game_init()
    playfield = pygame.sprite.RenderPlain()
    bricks = pygame.sprite.RenderPlain()
    add_brick_sprites(bricks)

    ball_sprite = Sprite(ball_shape((200, 180)), [level, level])
    playfield.add(ball_sprite)

    bottom_border_sprite = Sprite(border_shape())
    playfield.add(bottom_border_sprite)

    bat_sprite = Sprite(
        bat_shape((screen.get_rect().w / 2, screen.get_rect().h - 32)))
    playfield.add(bat_sprite)

    font = pygame.font.SysFont('NovaMono', 24)
    clock = pygame.time.Clock()

    game = GameSettings(
        level,
        screen,
        bat_sprite,
        ball_sprite,
        bottom_border_sprite,
        bricks,
        playfield,
        clock,
        font)

    return game


def run_game(game):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            position = event.pos
            game.bat_sprite.rect.left = position[0] - \
                game.bat_sprite.rect.width / 2

    game.screen.fill(SCREEN_COLOR)
    game.playfield.update()
    game.playfield.draw(game.screen)
    game.bricks.draw(game.screen)

    text = "Level: %s Lives: %s" % (game.level, 1)
    text_img = game.font.render(text, False, (0, 0, 0))
    game.screen.blit(text_img, (0, 0))

    pygame.display.flip()
    game.clock.tick(120)

    if pygame.sprite.collide_mask(game.bat_sprite, game.ball_sprite):
        if (game.ball_sprite.velocity[1] > 0):
            game.ball_sprite.velocity[1] *= -1

    if pygame.sprite.collide_mask(game.bottom_border_sprite, game.ball_sprite):
        running = False

    for brick in game.bricks:
        if pygame.sprite.collide_mask(game.ball_sprite, brick):
            game.bricks.remove(brick)
            game.ball_sprite.velocity[1] *= -1

    return running


def main():
    lives = 3

    game = make_level(1)
    running = True

    while running:
        running = run_game(game)

    pygame.quit()


if __name__ == "__main__":
    main()
