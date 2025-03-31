import numpy as np
#
x=2
y=3
vx=1
vy=2
a = 2 #(m/s/s)




# 加速度aを加えて
# 速度の大きさを計算
v = np.sqrt(v_x**2 + v_y**2)

# 半径の計算
# r = (m * v**2) / F
r = (v**2) / a

# 角速度の計算
omega = v / r (rad)

# 結果の表示
print(f"円運動の半径: {r:.2f} m")
print(f"円運動の角速度: {omega:.2f} rad/s")


# 初期条件
x, y = 2, 3  # 物体の現在位置
vx, vy = 1, 2  # 速度ベクトル
r = 5  # 半径

# 速度ベクトルの大きさを計算
v_magnitude = np.sqrt(vx**2 + vy**2)

# 単位ベクトルを計算
ux = vx / v_magnitude
uy = vy / v_magnitude

# 円の中心の座標を計算
xc = x - r * uy
yc = y + r * ux

print(f"円の中心の座標: ({xc:.2f}, {yc:.2f})")

dx = x1 - x0
dy = y1 - y0
d = np.sqrt(dx**2 + dy**2)
    
if d < r:
   print("点は円の内部にあります。接線は存在しません。")
   #減速フェーズ。一旦v=0にする。
   #加速フェーズ、減速フェーズ
   
else 
k = r / d

# 接点座標の計算
xt1 = x0 + k * dx
yt1 = y0 + k * dy

# 法線右90度のベクトル計算
offset_x = k * dy
offset_y = -k * dx

xt2a = xt1 + offset_x
yt2a = yt1 + offset_y
xt2b = xt1 - offset_x
yt2b = yt1 - offset_y



# 初期条件
x0, y0 = 1, 1  # 円の中心
x1, y2 = 4, 5  # 接点

# ベクトル計算
vx = x1 - x0
vy = y2 - y0

# 接線ベクトル
tx = -vy
ty = vx

# 接線の角度計算（y軸方向を0度とする）
theta_rad = np.arctan2(tx, ty)  # x成分とy成分で角度をラジアンで計算
theta_deg = np.degrees(theta_rad)  # ラジアンを度に変換

# 角度をy軸方向を基準: 0度とする変換
angle_from_y_axis = (theta_deg + 90) % 360  # 必ず0-360度の範囲に変換

print(f"接線の角度（y軸方向を0度とする）: {angle_from_y_axis:.2f} 度")


# 初期条件
vx, vy = 1, 0  # 初期ベクトル
omega = 1      # 角速度 (rad/s)
phi_deg = 90   # 目標角度 (度)

# 初期角度の計算
theta_initial_rad = np.arctan2(vx, vy)
theta_initial_deg = np.degrees(theta_initial_rad)

# 角度差の計算（度単位）
delta_theta_deg = (phi_deg - theta_initial_deg) % 360

# 時間の計算
t = delta_theta_deg / np.degrees(omega)

class Player:
    def __int___(self,pos,motion):
        self._pos = dict(pos)  # pos を辞書型として保存
        self._motion = dict(motion)  # motion を辞書型として保存
        #初期化時0
        #pos={'x':x,'y':y,'z':z},motion={'v':v,'theta':theta 仰角,'phi':phi 方位角}
    def round(self,xb,yb):
        #回転してxe,ye方向に向く。
    
    def accelerate(self)
    
    def mov(self,pos_b,t)
        # t時間以内に目標pos_bに向かう
        # 回転して向きを変える
        #     半径内にあるばあいは、0まで減速する。
        #     向きを変えてから追い越してしまう場合は、最初から0まで減速する。
        # 減速時間で到着できるなら減速
        # 等速運動で到着できるから等速→減速
        # 加速→減速
        # 加速→最大速度→減速
        # 到着できない場合は・・・
        

print(f"目標角度 {phi_deg} 度に達するまでの時間: {t:.2f} 秒")
def main():
    pos_p1={'x0':1.0,'y0':-6.0}
    v_p1={'vx':0,'vy':0}
    pos_p2={'x0':+3.0,'y0':+4.0}
    v_p2={'vx':0,'vy':0}
    player1 = Player(pos_p1,v_p1)
    player2 = Player(pos_p2,v_p2)

if __name__ == "__main__":
    main()
