import math

# 初期条件
v = 10  # m/s
theta = 45  # degree
y_0 = 0.5  # m
g = 9.8  # m/s^2

# 角度をラジアンに変換
theta_rad = math.radians(theta)

# 初速度の成分
v_x = v * math.cos(theta_rad)
v_y = v * math.sin(theta_rad)

# 関数を定義
def position_at_time(t):
    x = v_x * t
    y = y_0 + v_y * t - 0.5 * g * t**2
    return x, y

# テーブル形式で位置を示すための時間のリスト
times = [i*0.1 for i in range(20)]

# 各時刻の位置を計算して出力
for t in times:
    x, y = position_at_time(t)
    print(f"t: {t:.1f} s, x: {x:.2f} m, y: {y:.2f} m")


