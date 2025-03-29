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

# 初期条件を設定する
v = 10  # 初速度 m/s
theta = 30  # y軸からの投射角度 degree
phi = 45  # 仰角（上向きの角度） degree
z_0 = 0.5  # 初期高さ m
g = 9.8  # 重力加速度 m/s^2

# 角度をラジアンに変換
theta_rad = math.radians(theta)
phi_rad = math.radians(phi)

# 初速度を x, y, z 方向の成分に分解
v_x = v * math.cos(phi_rad) * math.sin(theta_rad)
v_y = v * math.cos(phi_rad) * math.cos(theta_rad)
v_z = v * math.sin(phi_rad)

# 二次方程式の係数
a = -0.5 * g
b = v_z
c = z_0

# 落下するまでの時間（地面に到達する時間）を求める
times_to_fall = solve_quadratic(a, b, c)

# 正の時間のみを出力
times_to_fall = [t for t in times_to_fall if t >= 0]

# 結果の出力
if times_to_fall:
    for t in times_to_fall:
        print(f"Time to fall to the ground: t = {t:.2f} s")
else:
    print("The ball does not fall to the ground.")