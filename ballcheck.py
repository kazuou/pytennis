import math


def calculate_time_to_height(self, target_height):
    """高さ target_height に達する時刻を計算"""
    # y(t) = y_0 + v_y * t - (1/2) * g * t^2
    # この式を解いて t を求める
    a = -0.5 * self.g
    b = self.v_y
    c = self.y - target_height  # 高さ50に達するためのc

    # 二次方程式を解く: at^2 + bt + c = 0
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        return None  # 解なし（物体は指定した高さに達しない）

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)

    # 時間が正の解を選ぶ
    if t1 >= 0:
        return t1
    elif t2 >= 0:
        return t2
    else:
        return None  # 両方の解が負の場合

def calculate_reflected_velocity(self):
    """反射後の速度ベクトルを計算"""
    # 水平方向の速度は変わらない
    v_x_reflected = self.v_x
    v_y_reflected = self.v_y

    # 鉛直方向の速度は反射係数を掛けて方向を逆にする
    v_z_reflected = -self.e * self.v_z

    # 反射後の仰角と方位角を計算
    # 仰角 (theta')
    theta_reflected = math.atan(math.sqrt(v_x_reflected**2 + v_y_reflected**2) / abs(v_z_reflected))

    # 方位角 (phi')
    phi_reflected = math.atan2(v_y_reflected, v_x_reflected)

    return v_x_reflected, v_y_reflected, v_z_reflected, theta_reflected, phi_reflected


def calculate_position_at_height(self, target_height):
    """指定した高さに達した時の x, y, z 座標を計算"""
    t_to_target = self.calculate_time_to_height(target_height)
    
    if t_to_target is None:
        return None  # 高さに達しない場合

    # x(t) = x_0 + v_x * t
    x_target = self.x + self.v_x * t_to_target
    # z(t) = z_0 + v_z * t - (1/2) * g * t^2
    z_target = self.z + self.v_z * t_to_target - 0.5 * self.g * t_to_target**2
    # y(t) はターゲットの高さなので target_height に設定
    y_target = target_height

    return x_target, y_target, z_target

def calculate_y_zero_time(self):
    """y = 0 を通過する時刻を計算"""
    # y(t) = y_0 + v_y * t - (1/2) * g * t^2
    # この式を解いて t を求める
    a = -0.5 * self.g
    b = self.v_y
    c = self.y

    # 二次方程式を解く: at^2 + bt + c = 0
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        return None  # 解なし（物体はy=0を通過しない）

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)

    # y=0 を通過する時間は 0 より大きい時間
    if t1 >= 0:
        return t1
    elif t2 >= 0:
        return t2
    else:
        return None  # 両方の解が負の場合

def calculate_position_at_y_zero(self):
    """y = 0 を通過した時の x, z 座標を計算"""
    t_y_zero = self.calculate_y_zero_time()
    
    if t_y_zero is None:
        return None  # y = 0 を通過しない場合

    # x(t) = x_0 + v_x * t
    x_zero = self.x + self.v_x * t_y_zero
    # z(t) = z_0 + v_z * t - (1/2) * g * t^2
    z_zero = self.z + self.v_z * t_y_zero - 0.5 * self.g * t_y_zero**2

    return x_zero, z_zero

def calculate_trajectory(self):
"""投げたときのワンバウンド地点を計算"""
# 初速度の成分
v_x = self.v * math.cos(self.theta) * math.cos(self.phi)
v_y = self.v * math.cos(self.theta) * math.sin(self.phi)
v_z = self.v * math.sin(self.theta)

# 地面に着くまでの時間 (z = 0 のときの時間)
t_f = (v_z + math.sqrt(v_z**2 + 2 * self.g * self.z)) / self.g

# 水平距離
x_land = self.x + v_x * t_f
y_land = self.y + v_y * t_f
z_land = 0  # 着地時のz座標は0

return x_land, y_land, z_land


def solve_quadratic(a, b, c):
    """二次方程式 ax^2 + bx + c = 0 の解を求める関数"""
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return []
    elif discriminant == 0:
        return [-b / (2 * a)]
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return [root1, root2]


class Ball:
    def __int___(self,pos,motion)
        self._pos0 = dict(pos)  # pos を辞書型として保存
        self._motion0 = dict(motion)  # motion を辞書型として保存
        #初期化時0
        #pos={'x'=x,'y'=y,'z'=z},mothon={'v'=v,'theta'=theta,'phi'=phi 仰角}
        #obj = Ball(pos,mothon)

    print(self._pos0)

    def check_net(self,_pos0,_motion0)
        

    def calculate_trajectory(self):
        """投げたときのワンバウンド地点を計算"""
        # 初速度の成分
        v_x = self.v * math.cos(self.theta) * math.cos(self.phi)
        v_y = self.v * math.cos(self.theta) * math.sin(self.phi)
        v_z = self.v * math.sin(self.theta)

        # 地面に着くまでの時間 (z = 0 のときの時間)
        t_f = (v_z + math.sqrt(v_z**2 + 2 * self.g * self.z)) / self.g

        # 水平距離
        x_land = self.x + v_x * t_f
        y_land = self.y + v_y * t_f
        z_land = 0  # 着地時のz座標は0

        return x_land, y_land, z_land

    def calculate_position_at_y_zero(self):
        """y = 0 を通過した時の x, z 座標を計算"""
        t_y_zero = self.calculate_y_zero_time()
        
        if t_y_zero is None:
            return None  # y = 0 を通過しない場合

        # x(t) = x_0 + v_x * t
        x_zero = self.x + self.v_x * t_y_zero
        # z(t) = z_0 + v_z * t - (1/2) * g * t^2
        z_zero = self.z + self.v_z * t_y_zero - 0.5 * self.g * t_y_zero**2

        return x_zero, z_zero


    def check_short(self, threshold=1.0):
        pos2 = 
        """v が threshold より小さいかどうかをチェック"""
        return self.v < threshold


def checksort(hit):
    """
    ネットに届いているかチェック
    """


def checlnet():
    """
    ネットを超えているかチェック
    """


def main():
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


if __name__ == "__main__":
    main()
