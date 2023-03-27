import pygame
from game_globals import *

def png_ball(pos):
    image = pygame.image.load("./assets/ball.png")
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
    pygame.draw.rect(image, (0, 0, 0), (0, 0, width, height), 0, 7)
    pygame.draw.rect(image, BAT_COLOR, (1, 1, width-2, height-2), 0, 7)
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

    width = SCREEN_WIDTH / BRICKS_PER_LINE
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