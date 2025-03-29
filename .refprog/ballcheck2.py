import math

def calculate_landing_positions_with_rebound(start_pos, speed, angle, board_height, rebound_coefficient=0.9):
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

    return (int(round(y1)), int(round(x1))), t_flight_1, (int(round(y2)), int(round(x2))), t_flight_2

# テスト用の例
start_pos = (0, 0)  # スタート位置
speed = 10  # 投げるスピード
angle = 60  # 投げる角度
board_height = 19  # ボードの高さ
rebound_coefficient = 0.9  # 反発係数

# 計算
landing_pos_1, time_1, landing_pos_2, time_2 = calculate_landing_positions_with_rebound(start_pos, speed, angle, board_height, rebound_coefficient)
print(f"First landing position: {landing_pos_1}, Time for first bounce: {time_1:.2f} seconds")
print(f"Second landing position: {landing_pos_2}, Time for second bounce: {time_2:.2f} seconds")