import math

def calculate_landing_position_with_rebound(start_pos, speed, angle, board_height, rebound_coefficient=0.9):
    x0, y0 = start_pos

    # Convert angle to radians
    theta = math.radians(angle)

    # Initial velocity components
    vx = speed * math.cos(theta)
    vy = speed * math.sin(theta)

    # Time to land (first bounce)
    t_flight_1 = (2 * vy) / 9.8

    # Calculate first landing position
    x1 = x0 + vx * t_flight_1
    y1 = y0 + vy * t_flight_1 - 0.5 * 9.8 * (t_flight_1 ** 2)

    # Calculate velocities after first bounce
    vy_rebound = vy * rebound_coefficient
    vx_rebound = vx

    # Time to land (second bounce)
    t_flight_2 = (2 * vy_rebound) / 9.8

    # Calculate second landing position
    x2 = x1 + vx_rebound * t_flight_2
    y2 = y1 + vy_rebound * t_flight_2 - 0.5 * 9.8 * (t_flight_2 ** 2)

    return (int(round(y1)), int(round(x1))), (int(round(y2)), int(round(x2)))

def is_valid_landing_with_rebound(start_pos, speed, angle, board_height, board_width, throw_width, throw_height, rebound_coefficient=0.9):
    x_center = (board_width - throw_width) // 2
    y_center = (board_height - throw_height) // 2

    landing_pos_1, landing_pos_2 = calculate_landing_position_with_rebound(start_pos, speed, angle, board_height, rebound_coefficient)
    x1, y1 = landing_pos_1
    x2, y2 = landing_pos_2

    # Check both bounces
    valid_landing_1 = (y_center <= x1 < y_center + throw_height) and (x_center <= y1 < x_center + throw_width)
    valid_landing_2 = (y_center <= x2 < y_center + throw_height) and (x_center <= y2 < x_center + throw_width)

    net_y = board_height // 2

    if x1 >= net_y or x2 >= net_y:
        return False

    return valid_landing_1 and valid_landing_2

# テスト用の例
start_pos = (18, 9)  # スタート位置
speed = 10  # 投げるスピード
angle = 45  # 投げる角度
board_height = 19  # ボードの高さ
board_width = 18  # ボードの幅
throw_width = 9  # 投げるエリアの幅
throw_height = 13  # 投げるエリアの高さ
rebound_coefficient = 0.9  # 反発係数

# 計算
landing_pos_1, landing_pos_2 = calculate_landing_position_with_rebound(start_pos, speed, angle, board_height, rebound_coefficient)
valid = is_valid_landing_with_rebound(start_pos, speed, angle, board_height, board_width, throw_width, throw_height, rebound_coefficient)
print(f"First landing position: {landing_pos_1}, Second landing position: {landing_pos_2}, Valid throw: {valid}")