import math


def calculate_time_to_height(pos,motion, target_height):
    """高さ target_height に達する時刻を計算"""
    """returnはlist"""

    g = 9.8  # 重力加速度 m/s^2

    v_x = motion['v'] * math.cos(motion['theta']) * math.cos(motion['phi'])
    v_y = motion['v'] * math.cos(motion['theta']) * math.sin(motion['phi'])
    v_z = motion['v'] * math.sin(motion['theta'])

    # z(t) = z_0 + v_z * t - (1/2) * g * t^2
    # この式を解いて t を求める
    a = -0.5 * self.g
    b = v_z
    c = pos['z'] - target_height  # 高さ50に達するための

    # 二次方程式を解く: at^2 + bt + c = 0
    discriminant = b**2 - 4*a*c

    tz = []

    if discriminant > 0:
        t1 = (-b + math.sqrt(discriminant)) / (2*a)
        t2 = (-b - math.sqrt(discriminant)) / (2*a)

    # 時間が正の解を選ぶ
    if t1 >= 0:
        tz.append t1
    if t2 >= 0:
        tz.append t2

    pos2,motion2,t0 = calculate_trajectory(pos,motion)

    v2_x = motion2['v'] * math.cos(motion2['theta']) * math.cos(motio2['phi'])
    v2_y = motion2['v'] * math.cos(motion2['theta']) * math.sin(motion2['phi'])
    v2_z = motion2['v'] * math.sin(motion2['theta'])

    # z(t) = z_0 + v_z * t - (1/2) * g * t^2
    # この式を解いて t を求める
    a = -0.5 * g
    b = v2_z
    c = pos2['z'] - target_height  # 高さ50に達するための

     # 二次方程式を解く: at^2 + bt + c = 0
    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        t1 = (-b + math.sqrt(discriminant)) / (2*a)
        t2 = (-b - math.sqrt(discriminant)) / (2*a)

    # 時間が正の解を選ぶ
    if t1 >= 0:
        tz.append (t1+t0)
    if t2 >= 0:
        tz.append (t2+t0)

def calculate_position_at_y_zero(pos,motion):
    """y = 0 を通過した時の z 座標を計算"""
    """y = 0 を通過する時刻を計算"""
    g = 9.8  # 重力加速度 m/s^2

    # v_x = motion['v'] * math.cos(motion['theta']) * math.cos(motion['phi'])
    v_y = motion['v'] * math.cos(motion['theta']) * math.sin(motion['phi'])
    v_z = motion['v'] * math.sin(motion['theta'])

    # y(t) = y_0 + v_y * t = 0
    # y_0 + v_y
    # この式を解いて t を求める
    t_y0 = pos['y']/v_y
    # z(t) = z_0 + v_z * t - 0.5 * g * t ^ 2
    z_y0 = pos['z'] + v_z * t_y0 - 0.5 * g * t_y0 ** 2
    if z_y0 < 0 :
        z_y0 = 0

    return z_y0

def calculate_trajectory(pos,motion):
    """投げたときのワンバウンド地点を計算"""
    # 初速度の成分
    g = 9.8  # 重力加速度 m/s^2
    e = 0.8
    v_x = motion['v'] * math.cos(motion['theta']) * math.cos(motion['phi'])
    v_y = motion['v'] * math.cos(motion['theta']) * math.sin(motion['phi'])
    v_z = motion['v'] * math.sin(motion['theta'])

    # 地面に着くまでの時間 (z = 0 のときの時間)
    t_f = (v_z + math.sqrt(v_z**2 + 2 * g * pos['z'])) / g

    pos1 = {'x':0,'y':0,'z':0 }

    # 水平距離
    pos1['x'] = pos['x'] + v_x * t_f
    pos1['y'] = pos['y'] + v_y * t_f
    pos1['z'] = 0  # 着地時のz座標は0

    """反射後の速度ベクトルを計算"""
    # 水平方向の速度は変わらない
    #pos={'x':x,'y':y,'z':z},motion={'v':v,'theta':theta 仰角,'phi':phi 方位角}
    motion1={'v':0,'theta':0,'phi':0}

    v_x_r = v_x
    v_y_r = v_y

    # 鉛直方向の速度は反射係数を掛けて方向を逆にする
    v_z_r = -e * v_z

    motion1['v'] =  math.sqrt(v_x_r**2 + v_y_r**2 + v_z_r**2)
    # 反射後の仰角と方位角を計算
    # 仰角 (theta')
    motion1['theta'] = math.atan(math.sqrt(v_x_r**2 + v_y_r**2) / abs(v_z_r))

    # 方位角 (phi')
    motion1['phi'] = math.atan2(v_y_r, v_x_r)

    return pos1,motion1,t_f


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

class Player:
    def __int___(self,pos,maxv):
        self._pos = dict(pos)
        self.maxv = maxv
    
    def posision_start(self,pos2,t0)
        #まず向かう場所を決める
        self.a = 2 #m/秒^2
        self.maxv = 5 ##m/秒
        self._pos1 = self._pos
        self._pos2 = pos2
        self.t0 = t0

    def 

     

class Ball:
    def __int___(self,pos,motion):
        self._pos = dict(pos)  # pos を辞書型として保存
        self._motion = dict(motion)  # motion を辞書型として保存
        #初期化時0
        #pos={'x':x,'y':y,'z':z},motion={'v':v,'theta':theta 仰角,'phi':phi 方位角}
        #obj = Ball(pos,mothon)
        self._pos2,self._motion2,self._t2 = calculate_trajectory(self._pos,self._motion):
        self.z_y0 = calculate_position_at_y_zero(pos,motion):

    def checksort(self):
        """
        ネットに届いているかチェック
        """
        return(self.z_y0 > 0)
    
    def checkout(self):
        return(self._pos2['x'] > court['x0'] and self._pos2['x'] < court['x1'] and self._pos2['y'] < court['y1'])
     

fieldxl=(-548.5-652)/100  #フィールドの左のx座標　中心は0
fieldxr=(548.5+652)/100   #フィールドの右のx座標
fieldy1= (-1188.5-612)/100
fieldy2=(1188.5+612)/100
baseline2 = (1188.5)/100
baseline1 = (-1188.5)/100
servieline2 = (1828.5-1188.5)/100
servieline1 = (548.5-1188.5)/100

netline=0

#フィールドサイズ。描画用
fielddrow = {'x0':fieldxl,'y0':fieldy1,'x1':fieldxr,'y1':fieldy2}
#コートサイズ描画用
courtdrow = {'x0':-548.5/100, 'y0':-1188.5/100, 'x1':411.5/100,'y1':1188.5/100}
#フィールドサイズ。移動可能範囲
field1 = {'x0':fieldxl,'y0':fieldy1,'x1':fieldxr,'y1':fieldy2}
field2 = {'x0':fieldxl,'y0':fieldy1,'x1':fieldxr,'y1':fieldy2}
#コートサイズ判定用。
#プレーヤー1が(手前側)から打った時の判定。1d、1aはサービス。デュースサイドとアドサイド
court1 = {'x0':-411.5/100, 'y0':0, 'x1':411.5/100,'y1':1188.5/100}
court1d = {'x0':-411.5/100, 'y0':0, 'x1':0,'y1':1188.5/100}
court1a = {'x0':0, 'y0':0, 'x1':411.5/100,'y1':1188.5/100}
#プレーヤー2が(手前側)から打った時の判定。2d、2aはサービス。デュースサイドとアドサイド
court2 = {'x0':-411.5/100, 'y0':-1188.5/100, 'x1':411.5/100,'y1':1188.5/100}
court2d = {'x0':0, 'y0':-1188.5/100, 'x1':411.5/100,'y1':1188.5/100}
court2a = {'x0':-411.5/100, 'y0':-1188.5/100, 'x1':411.5/100,'y1':0}
#
#
game=0
point=0
hit=0
# 0待機(打つ方向を入力中)　1(走る方向を入力中)
time=0

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

#採点 0 ネット
#採点 1 アウト
#採点 2 返ってきたボールが取れない
#採点 5 相手が取れない
