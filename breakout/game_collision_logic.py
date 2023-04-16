import pygame
import math
from game_draw_utils import draw_arrow

from game import sprite, color, shape, constant

def octagonal_collision_analyzer(collider, collidee, width_unit=4, height_unit=4):

    if not collider.rect.colliderect(collidee.rect):
        return 'no collision', 0, 0, 0

    dx = (collidee.rect.left + collidee.rect.width / 2) - \
        (collider.rect.left + collider.rect.width / 2)
    dy = (collidee.rect.top + collidee.rect.height / 2) - \
        (collider.rect.top + collider.rect.height / 2)
    theta = math.degrees(math.atan(dy/dx)) if (dx != 0) else 0.0

    te = pygame.Rect(collidee.rect.left + width_unit,
                     collidee.rect.top, collidee.rect.width - width_unit, height_unit)
    be = pygame.Rect(collidee.rect.left + width_unit, collidee.rect.top +
                     collidee.rect.height - height_unit, collidee.rect.width - width_unit, height_unit)
    le = pygame.Rect(collidee.rect.left, collidee.rect.top + height_unit,
                     width_unit, collidee.rect.height - height_unit)
    re = pygame.Rect(collidee.rect.left + collidee.rect.width - width_unit,
                     collidee.rect.top + height_unit, width_unit, collidee.rect.height - height_unit)
    tl = pygame.Rect(collidee.rect.left, collidee.rect.top,
                     width_unit, height_unit)
    tr = pygame.Rect(collidee.rect.left + collidee.rect.width -
                     width_unit, collidee.rect.top, width_unit, height_unit)
    bl = pygame.Rect(collidee.rect.left, collidee.rect.top +
                     collidee.rect.height - height_unit, width_unit, height_unit)
    br = pygame.Rect(collidee.rect.left + collidee.rect.width - width_unit,
                     collidee.rect.top + collidee.rect.height - height_unit, width_unit, height_unit)

    # print('le:%s re:%s te: %s be: %s tl: %s tr %s bl: %s br %s' % (left_edge, right_edge, top_edge, bottom_edge, tl, tr, bl, br))
    collision_info = 'unknown'

    collision_rects = (te, be, le, re, tl, tr, bl, br)

    if tl.colliderect(collider.rect):
        collision_info = 'top left'
        return collision_info, dx, dy, theta, collision_rects

    if tr.colliderect(collider.rect):
        collision_info = 'top right'
        return collision_info, dx, dy, theta, collision_rects

    if bl.colliderect(collider.rect):
        collision_info = 'bottom left'
        return collision_info, dx, dy, theta, collision_rects

    if br.colliderect(collider.rect):
        collision_info = 'bottom right'
        return collision_info, dx, dy, theta, collision_rects

    # edges have priority over corners
    if te.colliderect(collider.rect):
        collision_info = 'top edge'
        return collision_info, dx, dy, theta, collision_rects

    if be.colliderect(collider.rect):
        collision_info = 'bottom edge'
        return collision_info, dx, dy, theta, collision_rects

    if le.colliderect(collider.rect):
        collision_info = 'left edge'
        return collision_info, dx, dy, theta, collision_rects

    if re.colliderect(collider.rect):
        collision_info = 'right edge'
        return collision_info, dx, dy, theta, collision_rects

    print('collision_info: %s dx: %s dy: %s theta: %s' %
          (collision_info, dx, dy, theta))

    # raise Exception (collision_info, dx, dy, theta, collision_rects)
    return collision_info, dx, dy, theta, collision_rects


def rectangular_collision_analyzer(collider, collidee, width_unit=4, height_unit=4):

    te = pygame.Rect(collidee.rect.left,
                     collidee.rect.top, collidee.rect.width, height_unit)
    be = pygame.Rect(collidee.rect.left, collidee.rect.top +
                     collidee.rect.height - height_unit, collidee.rect.width, height_unit)
    le = pygame.Rect(collidee.rect.left, collidee.rect.top,
                     width_unit, collidee.rect.height)
    re = pygame.Rect(collidee.rect.left + collidee.rect.width -
                     width_unit, collidee.rect.top, width_unit, collidee.rect.height)
    collision_rects = (te, be, le, re)
    normal = None

    dx = (collidee.rect.left + collidee.rect.width / 2) - \
        (collider.rect.left + collider.rect.width / 2)
    dy = (collidee.rect.top + collidee.rect.height / 2) - \
        (collider.rect.top + collider.rect.height / 2)
    theta = math.degrees(math.atan(dy/dx)) if (dx != 0) else 0.0

    if not collider.rect.colliderect(collidee.rect):
        collision_info = 'no collision'
        return normal, collision_info, collision_rects, dx, dy, theta

    collision_info = 'unknown'

    # TODO
    # return multiple collision rects and normals
    # for when collider intersects
    # multiple collision rects
    if te.colliderect(collider.rect):
        collision_info = 'top edge'
        normal = (0, -1)
        return normal, collision_info, collision_rects, dx, dy, theta

    if be.colliderect(collider.rect):
        collision_info = 'bottom edge'
        normal = (0, 1)
        return normal, collision_info, collision_rects, dx, dy, theta

    if le.colliderect(collider.rect):
        collision_info = 'left edge'
        normal = (-1, 0)
        return normal, collision_info, collision_rects, dx, dy, theta

    if re.colliderect(collider.rect):
        collision_info = 'right edge'
        normal = (1, 0)
        return normal, collision_info, collision_rects, dx, dy, theta

    print('normal: %s, collision_info: %s, dx: %s, dy: %s, theta: %s' %
          (normal, collision_info, dx, dy, theta))

    # raise Exception (collision_info, dx, dy, theta, collision_rects)
    return (0, 0), collision_info, collision_rects, dx, dy, theta


# # TODO, refactor/move
# def get_collision_normal(collision_info):

#     normal = (0, 0)

#     match (collision_info):
#         case 'top edge':
#             normal = (0, -1)
#         case 'bottom edge':
#             normal = (0, 1)
#         case 'left edge':
#             normal = (-1, 0)
#         case 'right edge':
#             normal = (1, 0)
#         case 'top left':
#             normal = (-1, -1)
#         case 'top right':
#             normal = (1, -1)
#         case 'bottom left':
#             normal = (-1, 1)
#         case 'bottom right':
#             normal = (1, 1)

#     return normal


# def test_analyze_collision():

#     def print_analyze_collision(collider, collidee):
#         # print('testing collision: (%s)(%s)' % (collider.rect, collidee.rect))
#         (collision_info, dx, dy, theta) = octagonal_collision_analyzer(
#             collider, collidee)
#         print('%s (dx=%s, dy=%s, theta=%s)' % (collision_info, dx, dy, theta))

#     print('++++++++++++++++++++++')
#     print('test_analyze_collision')

#     class TestObj():
#         def __init__(self, rect: pygame.rect, velocity=[0, 0]):
#             self.rect = rect
#             self.velocity = velocity

#     brick = TestObj(pygame.rect.Rect(0, 0, 40, 20))

#     # walk top edge
#     print('--- walk top edge ---')
#     ball = TestObj(pygame.rect.Rect(0, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(4, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(5, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(10, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(15, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(39, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     print()

#     print('--- walk right edge ---')
#     ball = TestObj(pygame.rect.Rect(39, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(39, 5, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(39, 8, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(39, 12, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(39, 19, 3, 3))
#     print_analyze_collision(ball, brick)
#     print()

#     print('--- walk bottom edge ---')
#     ball = TestObj(pygame.rect.Rect(0, 19, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(5, 19, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(10, 19, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(15, 19, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(39, 19, 3, 3))
#     print_analyze_collision(ball, brick)
#     print()

#     print('--- walk left edge ---')
#     ball = TestObj(pygame.rect.Rect(0, 0, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(0, 5, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(0, 8, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(0, 12, 3, 3))
#     print_analyze_collision(ball, brick)
#     ball = TestObj(pygame.rect.Rect(0, 19, 3, 3))
#     print_analyze_collision(ball, brick)
#     print()


def test_analyze_collision_handling(screen: pygame.Surface):

    def analyze_collision_handling(collidee: sprite.BrickSprite, collider: sprite.BallSprite):

        screen.fill(color.SCREEN_COLOR)
        screen.fill((0, 0, 255), collidee.rect)
        (normal, collision_info, collision_rects, _, _,
         _) = rectangular_collision_analyzer(collider, collidee)

        c = 128
        for _, rect in enumerate(collision_rects):
            fill = (c, 0, c)
            screen.fill(fill, rect)
            c += 32

        screen.fill((255, 0, 0), collider.rect)
        start_dir = collider.dir
        print(start_dir)
        origin = collider.rect.center
        draw_arrow(screen, origin, (origin[0] + start_dir[0]
                   * 50, origin[1] + start_dir[1] * 50), (255, 0, 0))

        pygame.display.flip()
        pygame.time.delay(1000)

        coll_in = (collider.velocity, collider.dir)
        print('%s in vel, dir: %s' %
              (collision_info, coll_in))

        if (normal):
            draw_arrow(screen, origin, (origin[0] + normal[0]
                                        * 50, origin[1] + normal[1] * 50), (255, 255, 0))
        pygame.display.flip()
        pygame.time.delay(1000)

        collider.reflect(normal)
        end_dir = collider.dir
        print(collider.dir)
        origin = collider.rect.center
        draw_arrow(screen, origin, (origin[0] + end_dir[0]
                   * 50, origin[1] + end_dir[1] * 50), (0, 255, 0))

        coll_out = (collider.velocity, collider.dir)
        print('%s out vel, dir: %s' %
              (collision_info, coll_out))
        print('-----')

        pygame.display.flip()
        pygame.time.delay(1000)

    print('+++++++++++++++++++++++++++++++')
    print('test_analyze_collision_handling')

    brick = sprite.BrickSprite(shape.rectangle_brick_shape(0))
    brick.move_abs(160, 180)

    # 170, 189
    ball = sprite.BallSprite(shape.ball_shape(), (170, 189), 6,
                      pygame.math.Vector2(1, 1), None, None)

    analyze_collision_handling(brick, ball)

    ball.rect.move_ip(2, 2)
    analyze_collision_handling(brick, ball)

    ball.move_abs(170, 100)
    analyze_collision_handling(brick, ball)

    return

    brick = TestObj(pygame.rect.Rect(0, 0, 40, 20), 0, (0, 0))

    # vlist = ((1, 0), (1, 45), (1, 90), (1, 135), (1, 180), (1, 225), (1, 270), (1, 315))
    vlist = ((1, 0), (1, 1), (0, 1), (-1, -1),
             (-1, 0), (-1, 1), (0, -1), (1, -1))

    for d in vlist:
        # walk top edge
        dirvec = pygame.math.Vector2(d)
        analyze_collision_handling(
            brick, TestObj(pygame.rect.Rect(0, 0, 3, 3), 1, d))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(0, 0, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(0, 0, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(0, 0, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(0, 0, 3, 3), v))

        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(4, 0, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(5, 0, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(10, 0, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(39, 0, 3, 3), v))
        # print()

        # print('--- walk bottom edge ---')
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(0, 19, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(5, 19, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(10, 19, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(15, 19, 3, 3), v))
        # print_analyze_collision_handling(
        #     brick, TestObj(pygame.rect.Rect(39, 19, 3, 3), v))
        # print()


if __name__ == "__main__":
    screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    test_analyze_collision_handling(screen)

    running = True
    while running:
        running = False if pygame.event.peek(eventtype=pygame.QUIT) else True
        pygame.time.delay(100)
