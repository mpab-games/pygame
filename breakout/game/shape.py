import pygame
from game import color, constant

def png_ball(pos) -> pygame.Surface:
    image = pygame.image.load("./assets/ball.png")
    rect = image.get_rect()
    rect.center = pos
    return image


def ball_shape() -> pygame.Surface:
    radius = 6
    image = pygame.Surface([radius*2, radius*2])
    image.fill(color.SCREEN_COLOR)
    pygame.draw.circle(image, color.BALL_BORDER_COLOR, (radius, radius), radius)
    pygame.draw.circle(image, color.BALL_FILL_COLOR, (radius, radius), radius-1)
    image.set_colorkey(color.SCREEN_COLOR)
    return image


def bat_shape() -> pygame.Surface:
    width = 80
    height = 16
    image = pygame.Surface([width, height])
    image.fill(color.SCREEN_COLOR)
    pygame.draw.rect(image, color.BAT_BORDER_COLOR, (0, 0, width, height), 0, 7)
    pygame.draw.rect(image, color.BAT_FILL_COLOR, (1, 1, width-2, height-2), 0, 7)
    return image


def deadly_border_shape() -> pygame.Surface:
    image = pygame.Surface([constant.SCREEN_WIDTH, 4])
    image.fill((255, 0, 0))
    return image


def rectangle_brick_shape(row) -> pygame.Surface:
    # TODO: use a brighten/darken function
    fill_color = color.BRICK_FILL_COLOR

    match row % 6:
        case 0: fill_color = color.silver
        case 1: fill_color = color.red
        case 2: fill_color = color.yellow
        case 3: fill_color = color.blue
        case 4: fill_color = color.magenta
        case 5: fill_color = color.green

    # TODO: saturate
    dark_color = (63, 63, 63)
    bright_color = (255, 255, 255)

    image = pygame.Surface([constant.BRICK_WIDTH, constant.BRICK_HEIGHT])
    image.fill(color.SCREEN_COLOR)
    pygame.draw.rect(image, fill_color, (0, 0, constant.BRICK_WIDTH, constant.BRICK_HEIGHT))

    pygame.draw.line(image, dark_color, (0, constant.BRICK_HEIGHT - 1),
                     (constant.BRICK_WIDTH, constant.BRICK_HEIGHT - 1), 1)
    pygame.draw.line(image, dark_color, (constant.BRICK_WIDTH - 1, 0),
                     (constant.BRICK_WIDTH - 1, constant.BRICK_HEIGHT - 1), 1)

    pygame.draw.line(image, bright_color, (0, 0), (constant.BRICK_WIDTH, 0), 1)
    pygame.draw.line(image, bright_color, (0, 0), (0, constant.BRICK_HEIGHT), 1)
    return image


def octagon_brick_shape(fill_color) -> pygame.Surface:
    dark_color = (64, 64, 64)
    bright_color = (255, 255, 255)

    image = pygame.Surface([constant.BRICK_WIDTH, constant.BRICK_HEIGHT])
    image.fill(color.SCREEN_COLOR)
    pygame.draw.rect(image, fill_color, (0, 0, constant.BRICK_WIDTH, constant.BRICK_HEIGHT))

    pygame.draw.line(image, dark_color, (0, constant.BRICK_HEIGHT - 2),
                     (constant.BRICK_WIDTH - 2, constant.BRICK_HEIGHT - 2), 2)
    pygame.draw.line(image, dark_color, (constant.BRICK_WIDTH - 2, 0),
                     (constant.BRICK_WIDTH - 2, constant.BRICK_HEIGHT - 2), 2)

    pygame.draw.line(image, bright_color, (0, 0), (constant.BRICK_WIDTH - 2, 0), 2)
    pygame.draw.line(image, bright_color, (0, 0), (0, constant.BRICK_HEIGHT - 2), 2)
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


def text_surface(text: str, font: pygame.font.Font, color=(255, 255, 255)):
    return font.render(text, False, color)


def vertical_text_gradient_surface(text: str, font: pygame.font.Font, gradient: color.Gradient):
    mask = text_surface(text, font)
    target = vertical_gradient_filled_surface(
        mask.get_size(), gradient.start, gradient.end)
    mask_blit_surface(target, mask)
    return target


def dual_vertical_text_gradient_surface(text: str, font: pygame.font.Font, gradient_top: color.Gradient, gradient_bottom: color.Gradient):
    mask = text_surface(text, font)
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
