import math


def convenient_atan(delta_y, delta_x):
    angle = math.atan(-abs(delta_y / delta_x)) if delta_x else \
        math.pi / 2 * (1 if delta_y <= 0 else -1)
    if delta_x < 0 < delta_y:
        angle = math.pi - angle
    if delta_y < 0 < delta_x:
        angle = 2 * math.pi - angle
    if delta_x < 0 and delta_y < 0:
        angle = angle + math.pi
    return angle
