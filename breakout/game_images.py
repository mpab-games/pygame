import pygame
from game_globals import *


def png_ball(pos) -> pygame.Surface:
    image = pygame.image.load("./assets/ball.png")
    rect = image.get_rect()
    rect.center = pos
    return image


def ball_shape() -> pygame.Surface:
    radius = 6
    image = pygame.Surface([radius*2, radius*2])
    image.fill(SCREEN_FILL_COLOR)
    pygame.draw.circle(image, BALL_BORDER_COLOR, (radius, radius), radius)
    pygame.draw.circle(image, BALL_FILL_COLOR, (radius, radius), radius-1)
    image.set_colorkey(SCREEN_FILL_COLOR)
    return image


def bat_shape() -> pygame.Surface:
    width = 80
    height = 16
    image = pygame.Surface([width, height])
    image.fill(SCREEN_FILL_COLOR)
    pygame.draw.rect(image, BAT_BORDER_COLOR, (0, 0, width, height), 0, 7)
    pygame.draw.rect(image, BAT_FILL_COLOR, (1, 1, width-2, height-2), 0, 7)
    return image


def deadly_border_shape() -> pygame.Surface:
    image = pygame.Surface([SCREEN_WIDTH, 4])
    image.fill((255, 0, 0))
    rect = image.get_rect(topleft=(0, SCREEN_HEIGHT - 4))
    return image


def rectangle_brick_shape(fill_color) -> pygame.Surface:
    dark_color = (64, 64, 64)
    bright_color = (255, 255, 255)

    width = SCREEN_WIDTH / BRICKS_PER_LINE
    height = SCREEN_HEIGHT / 20
    image = pygame.Surface([width, height])
    image.fill(SCREEN_FILL_COLOR)
    pygame.draw.rect(image, fill_color, (0, 0, width, height))

    pygame.draw.line(image, dark_color, (0, height - 2),
                     (width - 2, height - 2), 2)
    pygame.draw.line(image, dark_color, (width - 2, 0),
                     (width - 2, height - 2), 2)

    pygame.draw.line(image, bright_color, (0, 0), (width - 2, 0), 2)
    pygame.draw.line(image, bright_color, (0, 0), (0, height - 2), 2)
    return image

def octagon_brick_shape(fill_color) -> pygame.Surface:
    dark_color = (64, 64, 64)
    bright_color = (255, 255, 255)

    width = SCREEN_WIDTH / BRICKS_PER_LINE
    height = SCREEN_HEIGHT / 20
    image = pygame.Surface([width, height])
    image.fill(SCREEN_FILL_COLOR)
    pygame.draw.rect(image, fill_color, (0, 0, width, height))

    pygame.draw.line(image, dark_color, (0, height - 2),
                     (width - 2, height - 2), 2)
    pygame.draw.line(image, dark_color, (width - 2, 0),
                     (width - 2, height - 2), 2)

    pygame.draw.line(image, bright_color, (0, 0), (width - 2, 0), 2)
    pygame.draw.line(image, bright_color, (0, 0), (0, height - 2), 2)
    return image


def vertical_gradient_filled_surface(size, startcolor, endcolor) -> pygame.Surface:
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    surface = pygame.Surface((1, height)).convert_alpha()
    dd = 1.0/height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(height):
        surface.set_at((0, y),
                       (int(sr + rm*y),
                        int(sg + gm*y),
                        int(sb + bm*y),
                        int(sa + am*y))
                       )
    return pygame.transform.scale(surface, size)


def mask_blit_surface(target_surface: pygame.Surface, mask_surface: pygame.Surface):
    mask_surface.set_colorkey((0, 0, 0))
    target_surface.blit(mask_surface, (0, 0), None,
                        pygame.BLEND_RGBA_MULT)
    target_surface.set_colorkey((0, 0, 0))


def vertical_text_gradient_surface(text: str, font: pygame.font.Font, gradient: Gradient):
    mask = font.render(text, False, (255, 255, 255))
    target = vertical_gradient_filled_surface(
        mask.get_size(), gradient.start, gradient.end)
    mask_blit_surface(target, mask)
    return target


def dual_vertical_text_gradient_surface(text: str, font: pygame.font.Font, gradient_top: Gradient, gradient_bottom: Gradient):
    mask = font.render(text, False, (255, 255, 255))
    sz = (mask.get_size()[0], mask.get_size()[1]//2)
    s1 = vertical_gradient_filled_surface(
        sz, gradient_top.start, gradient_top.end)
    s2 = vertical_gradient_filled_surface(
        sz, gradient_bottom.start, gradient_bottom.end)
    surface = pygame.Surface(mask.get_size())
    surface.blit(s1, (0, 0), None)
    surface.blit(s2, (0, sz[1]), None)
    mask_blit_surface(surface, mask)
    return surface
