import pygame
from game_globals import *


def png_ball(pos) -> tuple[pygame.Surface, pygame.Rect]:
    image = pygame.image.load("./assets/ball.png")
    rect = image.get_rect()
    rect.center = pos
    return image, rect


def ball_shape(pos) -> tuple[pygame.Surface, pygame.Rect]:
    radius = 8
    image = pygame.Surface([radius*2, radius*2])
    image.fill(SCREEN_COLOR)
    rect = image.get_rect()
    rect.center = pos
    pygame.draw.circle(image, BALL_COLOR, (radius, radius), radius)
    image.set_colorkey(SCREEN_COLOR)
    return image, rect


def bat_shape(pos) -> tuple[pygame.Surface, pygame.Rect]:
    width = 80
    height = 16
    image = pygame.Surface([width, height])
    image.fill(SCREEN_COLOR)
    rect = image.get_rect()
    rect.center = pos
    pygame.draw.rect(image, (0, 0, 0), (0, 0, width, height), 0, 7)
    pygame.draw.rect(image, BAT_COLOR, (1, 1, width-2, height-2), 0, 7)
    return image, rect


def border_shape() -> tuple[pygame.Surface, pygame.Rect]:
    image = pygame.Surface([SCREEN_WIDTH, 1])
    image.fill(BALL_COLOR)
    rect = image.get_rect()
    rect.bottom = SCREEN_HEIGHT
    return image, rect


def brick_shape(pos, fill_color) -> tuple[pygame.Surface, pygame.Rect]:
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
    return image, rect


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


def vertical_text_gradient_surface(text: str, font: pygame.font.Font, gradient_top, gradient_bottom):
    mask = font.render(text, False, (255, 255, 255))
    target = vertical_gradient_filled_surface(
        mask.get_size(), gradient_top, gradient_bottom)
    mask_blit_surface(target, mask)
    return target
