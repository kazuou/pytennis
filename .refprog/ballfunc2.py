import math

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

# 位置を時間の関数として計算する関数を定義
def position_at_time(t, v_x, v_y, v_z, z_0):
    x = v_x * t
    y = v_y * t
    z = z_0 + v_z * t - 0.5 * g * t**2
    return x, y, z

# テーブル形式で位置を示すための時間のリストを生成
times = [i*0.1 for i in range(50)]  # 5秒間、0.1秒刻みのリスト

# 各時刻の位置を計算して出力
for t in times:
    x, y, z = position_at_time(t, v_x, v_y, v_z, z_0)
    print(f"t: {t:.1f} s, x: {x:.2f} m, y: {y:.2f} m, z: {z:.2f} m")