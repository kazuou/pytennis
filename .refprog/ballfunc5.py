import math

# 初速度と角度の設定
v = 10  # 初速度 m/s
theta = 30  # y軸からの投射角度 degree
phi = 45  # 仰角 degree

# 初期条件
x_start = 1
y_start = -10
z_start = 0  # 初期高さ

g = 9.8  # 重力加速度 m/s^2

# 角度をラジアンに変換
theta_rad = math.radians(theta)
phi_rad = math.radians(phi)

# 初速度成分の計算
v_x = v * math.cos(phi_rad) * math.sin(theta_rad)
v_y = v * math.cos(phi_rad) * math.cos(theta_rad)
v_z = v * math.sin(phi_rad)

# 一番頂点の時間を計算
t_top = v_z / g

# その時の位置を計算
x_top = x_start + v_x * t_top
y_top = y_start + v_y * t_top
z_top = z_start + v_z * t_top - 0.5 * g * t_top ** 2

# 結果の出力
print(f"Time to reach the top: {t_top:.2f} s")
print(f"Top position: x = {x_top:.2f} m, y = {y_top:.2f} m, z = {z_top:.2f} m")