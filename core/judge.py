import math

# from config import player_vmax
import config


def adjust_target(p_pos, p_pos_target, time_limit):
    x1, y1 = p_pos
    x2, y2 = p_pos_target
    distance = math.hypot(x2 - x1, y2 - y1)
    max_distance = config.PLAYER_VMAX * time_limit
    if distance <= max_distance:
        return [x2, y2]  # リスト形式で返却
    else:
        ratio = max_distance / distance
        new_x = x1 + (x2 - x1) * ratio
        new_y = y1 + (y2 - y1) * ratio
        return [new_x, new_y]
