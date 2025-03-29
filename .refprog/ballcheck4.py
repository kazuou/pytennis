import math

def calculate_landing_positions_with_rebound(start_pos, speed, angle, board_height, rebound_coefficient=0.9, net_x=None):
    x0, y0 = start_pos

    # ボールの初期位置が0.5m（50cm）の高さからの場合
    initial_height = y0

    # Convert angle to radians
    theta = math.radians(angle)

    # Initial velocity components
    vx = speed * math.cos(theta)
    vy = speed * math.sin(theta)

    # Time to land (first bounce), considering initial height y0
    t_flight_1 = (vy + math.sqrt(vy**2 + 2 * 9.8 * initial_height)) / 9.8

    # Calculate first landing position
    x1 = x0 + vx * t_flight_1
    y1 = 0  # First landing is on the ground, hence y1 = 0

    # Calculate velocities after first bounce
    vy_rebound = vy * rebound_coefficient
    vx_rebound = vx

    # Time to land (second bounce)
    t_flight_2 = (2 * vy_rebound) / 9.8

    # Calculate second landing position
    x2 = x1 + vx_rebound * t_flight_2
    y2 = 0  # Second landing is also on the ground, hence y2 = 0

    net_height = None
    if net_x is not None:
        # Time to reach net
        t_net = net_x / vx
        net_height = initial_height + vy * t_net - 0.5 * 9.8 * (t_net ** 2)

    return (int(round(x1)), int(round(y1))), t_flight_1, (int(round(x2)), int(round(y2))), t_flight_2, net_height

# テスト用の例
start_pos = (0, 0.5)  # スタート位置 (x, y) 50cm = 0.5m
speed = 10  # 投げるスピード
angle = 45  # 投げる角度
board_height = 19  # ボードの高さ
rebound_coefficient = 0.9  # 反発係数
net_x = 5  # ネットの位置

# 計算
landing_pos_1, time_1, landing_pos_2, time_2, net_height = calculate_landing_positions_with_rebound(start_pos, speed, angle, board_height, rebound_coefficient, net_x)
print(f"First landing position: {landing_pos_1}, Time for first bounce: {time_1:.2f} seconds")
print(f"Second landing position: {landing_pos_2}, Time for second bounce: {time_2:.2f} seconds")
print(f"Height at net (position {net_x}): {net_height:.2f} meters" if net_height is not None else "Net position not provided")