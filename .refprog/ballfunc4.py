import math


def solve_quadratic(a, b, c):
    """ 二次方程式 ax^2 + bx + c = 0 の解を求める関数 """
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return []
    elif discriminant == 0:
        return [-b / (2*a)]
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return [root1, root2]


# 例えば、初速度を設定
v = 10  # 初速度 m/s
phi = 45  # 仰角 degree

# 初期条件
x_start = 1
y_start = -10
z_start = 0  # y=0を通過する高さ

g = 9.8  # 重力加速度 m/s^2

# 角度をラジアンに変換
phi_rad = math.radians(phi)

# 初速度成分の計算
v_x = 0  # y軸方向だけに速度を持つ
v_y = v * math.cos(phi_rad)
v_z = v * math.sin(phi_rad)

# y = 0 となる時間を求める
a = -0.5 * g
b = v_z
c = y_start

# 二次方程式の解を求める
times_to_pass_zero_y = solve_quadratic(a, b, c)

# 正の時間のみを出力
times_to_pass_zero_y = [t for t in times_to_pass_zero_y if t >= 0]

# 結果の出力
if times_to_pass_zero_y:
    for t in times_to_pass_zero_y:
        x = x_start + v_x * t
        y = x_start + v_y * t
        z = z_start + v_z * t - 0.5 * g * t**2
        print(f"t: {t:.2f} s, x: {x:.2f} m, y: {y:.2f} m, z: {z:.2f} m")
else:
    print("The ball does not pass through y = 0.")