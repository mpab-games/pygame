import pygame
import math
from game_draw_utils import draw_arrow

from game_globals import *


def analyze_octagon_brick_collision(collider, brick):

    if not collider.rect.colliderect(brick.rect):
        return 'no collision', 0, 0, 0

    dx = (brick.rect.left + brick.rect.width / 2) - \
        (collider.rect.left + collider.rect.width / 2)
    dy = (brick.rect.top + brick.rect.height / 2) - \
        (collider.rect.top + collider.rect.height / 2)
    theta = math.degrees(math.atan(dy/dx)) if (dx != 0) else 0.0

    # div = 5
    width_unit = 4  # collidee.rect.width / div
    height_unit = 4  # collidee.rect.height / div

    te = pygame.Rect(brick.rect.left + width_unit,
                           brick.rect.top, brick.rect.width - width_unit, height_unit)
    be = pygame.Rect(brick.rect.left + width_unit, brick.rect.top +
                              brick.rect.height - height_unit, brick.rect.width - width_unit, height_unit)
    le = pygame.Rect(brick.rect.left, brick.rect.top + height_unit,
                            width_unit, brick.rect.height - height_unit)
    re = pygame.Rect(brick.rect.left + brick.rect.width - width_unit,
                             brick.rect.top + height_unit, width_unit, brick.rect.height - height_unit)
    tl = pygame.Rect(brick.rect.left, brick.rect.top,
                     width_unit, height_unit)
    tr = pygame.Rect(brick.rect.left + brick.rect.width -
                     width_unit, brick.rect.top, width_unit, height_unit)
    bl = pygame.Rect(brick.rect.left, brick.rect.top +
                     brick.rect.height - height_unit, width_unit, height_unit)
    br = pygame.Rect(brick.rect.left + brick.rect.width - width_unit,
                     brick.rect.top + brick.rect.height - height_unit, width_unit, height_unit)

    # print('le:%s re:%s te: %s be: %s tl: %s tr %s bl: %s br %s' % (left_edge, right_edge, top_edge, bottom_edge, tl, tr, bl, br))
    collision_info = 'unknown'

    collision_rects = (te, be, le, re, tl,tr, bl, br)

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
    return collision_info, dx, dy, theta, collision_rects


def get_collision_normal(collider, collidee):
    (collision_info, dx, dy, theta, collision_rects) = analyze_octagon_brick_collision(collider, collidee)

    normal = (0, 0)

    match (collision_info):
        case 'top edge':
            normal = (0, 1)
        case 'bottom edge':
            normal = (0, -1)
        case 'left edge':
            normal = (1, 0)
        case 'right edge':
            normal = (-1, 0)
        case 'top left':
            normal = (-1, -1)
        case 'top right':
            normal = (1, -1)
        case 'bottom left':
            normal = (-1, 1)
        case 'bottom right':
            normal = (1, 1)

    return collision_info, normal


def test_analyze_collision():

    def print_analyze_collision(collider, collidee):
        # print('testing collision: (%s)(%s)' % (collider.rect, collidee.rect))
        (collision_info, dx, dy, theta) = analyze_octagon_brick_collision(collider, collidee)
        print('%s (dx=%s, dy=%s, theta=%s)' % (collision_info, dx, dy, theta))

    print('++++++++++++++++++++++')
    print('test_analyze_collision')

    class TestObj():
        def __init__(self, rect: pygame.rect, velocity=[0, 0]):
            self.rect = rect
            self.velocity = velocity

    brick = TestObj(pygame.rect.Rect(0, 0, 40, 20))

    # walk top edge
    print('--- walk top edge ---')
    ball = TestObj(pygame.rect.Rect(0, 0, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(4, 0, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(5, 0, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(10, 0, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(15, 0, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(39, 0, 3, 3))
    print_analyze_collision(ball, brick)
    print()

    print('--- walk right edge ---')
    ball = TestObj(pygame.rect.Rect(39, 0, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(39, 5, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(39, 8, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(39, 12, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(39, 19, 3, 3))
    print_analyze_collision(ball, brick)
    print()

    print('--- walk bottom edge ---')
    ball = TestObj(pygame.rect.Rect(0, 19, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(5, 19, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(10, 19, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(15, 19, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(39, 19, 3, 3))
    print_analyze_collision(ball, brick)
    print()

    print('--- walk left edge ---')
    ball = TestObj(pygame.rect.Rect(0, 0, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(0, 5, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(0, 8, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(0, 12, 3, 3))
    print_analyze_collision(ball, brick)
    ball = TestObj(pygame.rect.Rect(0, 19, 3, 3))
    print_analyze_collision(ball, brick)
    print()


def test_analyze_collision_handling(screen: pygame.Surface):

    class TestObj():
        def __init__(self, rect: pygame.rect,
                     velocity,
                     direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)):
            self.rect = rect
            self.velocity = velocity
            self.direction = direction

        def reflect(self, normal: pygame.math.Vector2):
            vec_normal = pygame.math.Vector2(normal)
            self.direction = \
                self.direction.reflect(vec_normal) if vec_normal.length() > 0 else self.direction.reflect(self.direction)

    def analyze_collision_handling(collidee: TestObj, collider: TestObj):

        screen.fill(SCREEN_FILL_COLOR)
        screen.fill((0,0,255), brick.rect)
        (collision_info, _, _, _, collision_rects) = analyze_octagon_brick_collision(collider, brick)

        for idx, rect in enumerate(collision_rects):
            fill = (0,255,0) if idx < 4 else (255,255,0)
            screen.fill(fill, rect)

        screen.fill((255,0,0), collider.rect)
        start_dir = collider.direction
        print (start_dir)
        origin = collider.rect.center
        draw_arrow(screen, origin, (origin[0] + start_dir[0] * 50, origin[1] + start_dir[1] * 50), (255, 0, 0))

        pygame.display.flip()
        pygame.time.delay(1000)
        
        coll_in = (collider.velocity, collider.direction)
        (collision_info, normal) = get_collision_normal(collider, collidee)
        print('%s in vel, dir: %s' %
              (collision_info, coll_in))
        collider.reflect(normal)
        end_dir = collider.direction
        print (collider.direction)
        origin = collider.rect.center
        draw_arrow(screen, origin, (origin[0] + end_dir[0] * 50, origin[1] + end_dir[1] * 50), (255, 255, 0))

        coll_out = (collider.velocity, collider.direction)
        print('%s out vel, dir: %s' %
              (collision_info, coll_out))
        print('-----')


        pygame.display.flip()
        pygame.time.delay(1000)

    print('+++++++++++++++++++++++++++++++')
    print('test_analyze_collision_handling')

    brick = TestObj(pygame.rect.Rect(160, 180, 80, 30), 0, (0, 0))
    ball = TestObj(pygame.rect.Rect(151, 189, 12, 12), 6,
                   pygame.math.Vector2(0.707107, 0.707107))

    analyze_collision_handling(
        brick, ball)
    
    ball = TestObj(pygame.rect.Rect(170, 189, 12, 12), 6,
                   pygame.math.Vector2(0.707107, 0.707107))
    
    analyze_collision_handling(
        brick, ball)
    
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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    test_analyze_collision_handling(screen)
    
