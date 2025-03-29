import math

def calculate_positions_for_height_with_bounces(start_pos, speed, angle, initial_height, target_height, rebound_coefficient=0.9):
    x0, y0 = start_pos

    # Convert angle to radians
    theta = math.radians(angle)

    # Initial velocity components
    vx = speed * math.cos(theta)
    vy = speed * math.sin(theta)

    def calculate_time_and_position(vx, vy, start_time, start_x, start_y, target_height):
        g = 9.8

        # Calculate time to reach target height on the way up and down
        a = -0.5 * g
        b = vy
        c = start_y - target_height

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return None, None  # No real solution exists

        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)

        t1_total = start_time + t1 if t1 >= 0 else None
        t2_total = start_time + t2 if t2 >= 0 else None

        x1 = start_x + vx * t1_total if t1_total is not None else None
        x2 = start_x + vx * t2_total if t2_total is not None else None

        return (x1, t1_total), (x2, t2_total)

    # Calculate times and positions before the first bounce
    before_bounce_up, before_bounce_down = calculate_time_and_position(vx, vy, 0, x0, y0, target_height)

    # Time to first bounce (ground level)
    t_flight_1 = (vy + math.sqrt(vy**2 + 2 * 9.8 * y0)) / 9.8

    # Velocity after first bounce
    vy_rebound = vy * rebound_coefficient

    # Calculate times and positions after the first bounce
    after_bounce_up, after_bounce_down = calculate_time_and_position(vx, vy_rebound, t_flight_1, x0 + vx * t_flight_1, 0, target_height)

    # Time to second bounce (ground level)
    t_flight_2 = (2 * vy_rebound) / 9.8

    # Velocity after second bounce
    vy_rebound_2 = vy_rebound * rebound_coefficient

    # Calculate times and positions after the second bounce
    after_second_bounce_up, after_second_bounce_down = calculate_time_and_position(vx, vy_rebound_2, t_flight_1 + t_flight_2, x0 + vx * t_flight_1 + vx * t_flight_2, 0, target_height)

    return before_bounce_up, before_bounce_down, after_bounce_up, after_bounce_down, after_second_bounce_up, after_second_bounce_down


# テスト用の例
start_pos = (0, 0.5)  # スタート位置 (x, y) 50cm = 0.5m
speed = 10  # 初速度
angle = 45  # 投げる角度
target_height = 0.5  # 再び0.5mに到達する位置
rebound_coefficient = 0.9  # 反発係数

# 計算
before_bounce_up, before_bounce_down, after_bounce_up, after_bounce_down, after_second_bounce_up, after_second_bounce_down = calculate_positions_for_height_with_bounces(start_pos, speed, angle, start_pos[1], target_height, rebound_coefficient)

print(f"Before bounce (up) - Position: {before_bounce_up[0]:.2f} m, Time: {before_bounce_up[1]:.2f} s")
print(f"Before bounce (down) - Position: {before_bounce_down[0]:.2f} m, Time: {before_bounce_down[1]:.2f} s")
print(f"After first bounce (up) - Position: {after_bounce_up[0]:.2f} m, Time: {after_bounce_up[1]:.2f} s")
print(f"After first bounce (down) - Position: {after_bounce_down[0]:.2f} m, Time: {after_bounce_down[1]:.2f} s")
print(f"After second bounce (up) - Position: {after_second_bounce_up[0]:.2f} m, Time: {after_second_bounce_up[1]:.2f} s")
print(f"After second bounce (down) - Position: {after_second_bounce_down[0]:.2f} m, Time: {after_second_bounce_down[1]:.2f} s")