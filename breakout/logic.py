import pygame
import math


def analyze_collision(collider, collidee):

    if not collider.rect.colliderect(collidee.rect):
        return 'no collision', 0, 0, 0

    dx = (collidee.rect.left + collidee.rect.width / 2) - \
        (collider.rect.left + collider.rect.width / 2)
    dy = (collidee.rect.top + collidee.rect.height / 2) - \
        (collider.rect.top + collider.rect.height / 2)
    theta = math.degrees(math.atan(dy/dx)) if (dx != 0) else 0.0

    # div = 5
    width_unit = 4  # collidee.rect.width / div
    height_unit = 4  # collidee.rect.height / div

    top_edge = pygame.Rect(collidee.rect.left + width_unit,
                           collidee.rect.top, collidee.rect.width - width_unit, height_unit)
    bottom_edge = pygame.Rect(collidee.rect.left + width_unit, collidee.rect.top +
                              collidee.rect.height - height_unit, collidee.rect.width - width_unit, height_unit)

    left_edge = pygame.Rect(collidee.rect.left, height_unit,
                            width_unit, collidee.rect.height - height_unit)
    right_edge = pygame.Rect(collidee.rect.left + collidee.rect.width - width_unit,
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

    if tl.colliderect(collider.rect):
        collision_info = 'top left'
        return collision_info, dx, dy, theta

    if tr.colliderect(collider.rect):
        collision_info = 'top right'
        return collision_info, dx, dy, theta

    if bl.colliderect(collider.rect):
        collision_info = 'bottom left'
        return collision_info, dx, dy, theta

    if br.colliderect(collider.rect):
        collision_info = 'bottom right'
        return collision_info, dx, dy, theta

    # edges have priority over corners
    if top_edge.colliderect(collider.rect):
        collision_info = 'top edge'
        return collision_info, dx, dy, theta
    if bottom_edge.colliderect(collider.rect):
        collision_info = 'bottom edge'
        return collision_info, dx, dy, theta

    if left_edge.colliderect(collider.rect):
        collision_info = 'left edge'
        return collision_info, dx, dy, theta

    if right_edge.colliderect(collider.rect):
        collision_info = 'right edge'
        return collision_info, dx, dy, theta

    print('collision_info: %s dx: %s dy: %s theta: %s' %
          (collision_info, dx, dy, theta))
    return collision_info, dx, dy, theta


def get_collision_normal(collider, collidee):
    (collision_info, dx, dy, theta) = analyze_collision(collider, collidee)

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
        (collision_info, dx, dy, theta) = analyze_collision(collider, collidee)
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


def test_analyze_collision_handling():

    class TestObj():
        def __init__(self, rect: pygame.rect, velocity, direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)):
            self.rect = rect
            self.velocity = velocity
            self.direction = direction

        def reflect(self, normal: pygame.math.Vector2):
            self.direction = self.direction.reflect(normal)

    def print_analyze_collision_handling(collidee: TestObj, collider: TestObj):
        # print('testing collision: (%s)(%s)' % (collider.rect, collidee.rect))
        coll_in = (collider.velocity, collider.direction)
        (collision_info, normal) = get_collision_normal(collider, collidee)
        print('%s in vel, dir: %s' %
              (collision_info, coll_in))
        collider.reflect(normal)
        coll_out = (collider.velocity, collider.direction)
        print('%s out vel, dir: %s' %
              (collision_info, coll_out))
        print('-----')

    print('+++++++++++++++++++++++++++++++')
    print('test_analyze_collision_handling')

    brick = TestObj(pygame.rect.Rect(0, 0, 40, 20), 0, (0, 0))

    # vlist = ((1, 0), (1, 45), (1, 90), (1, 135), (1, 180), (1, 225), (1, 270), (1, 315))
    vlist = ((1, 0), (1, 1), (0, 1), (-1, -1),
             (-1, 0), (-1, 1), (0, -1), (1, -1))

    for d in vlist:
        # walk top edge
        dirvec = pygame.math.Vector2(d)
        print_analyze_collision_handling(
            brick, TestObj(pygame.rect.Rect(0, 0, 3, 3), 1, dirvec))
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
    test_analyze_collision_handling()
