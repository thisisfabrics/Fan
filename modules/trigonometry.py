import math


def convenient_atan(delta_y, delta_x, mode="rad"):
    if not delta_x:
        angle = math.pi / 2 * (1 if delta_y <= 0 else -1)
    elif not delta_y:
        angle = math.pi if delta_x <= 0 else 0
    else:
        angle = math.atan(-abs(delta_y / delta_x))
        if delta_x < 0 < delta_y:
            angle = math.pi - angle
        if delta_y < 0 < delta_x:
            angle = 2 * math.pi - angle
        if delta_x < 0 and delta_y < 0:
            angle = angle + math.pi
    return angle if mode == "rad" else math.degrees(angle)
