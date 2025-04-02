import numpy as np
import math
#
def max_distance(t):
    """
    Calculate the maximum distance traveled given the maximum speed, acceleration, and total time.
    
    Parameters:
    v_max (float): Maximum speed.
    a (float): Acceleration.
    t (float): Total time.
    
    Returns:
    float: The maximum distance traveled.
    """
    global v_max,a
    # Calculate the time to reach maximum speed
    t1 = v_max / a
    
    # If the total time is less than the time to accelerate and decelerate, it means we don't maintain maximum speed
    if t < 2 * t1:
        # Accelerate and then decelerate immediately
        t_accelerate = t / 2
        # distance = 0.5 * a * t_accelerate ** 2 + 0.5 * a * t_accelerate ** 2
        distance =  a * t_accelerate ** 2

    else:
        # Time at maximum speed
        t2 = t - 2 * t1
        # Distance travelled while accelerating
        d1 = 0.5 * a * t1 ** 2
        # Distance travelled while maintaining maximum speed
        d2 = v_max * t2
        # Distance travelled while decelerating
        d3 = 0.5 * a * t1 ** 2
        # Total distance
        distance = d1 + d2 + d3

    return distance


v_max = 20.0  # Maximum speed
a = 2.0       # Acceleration


# distance = max_distance(v_max, a, t)
# print(f"The maximum distance traveled is {distance:.2f} meters.")

class Character:
    """キャラクターーオブジェクト"""
    def __init__(self):
        self.status = 0
        self.jump_status = 0
        self.image_type = 0 #
        self.x = 0
        self.y = 0
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.rotx = 0   #回転　ボールのみ
        self.roty = 0
        self.rotz = 0
        self.dx = 0     #目的地
        self.dy = 0
        self.dz = 0
        self.shotgear=50
        self.movegear=50
        self.width = 0
        self.height = 0
        self.mag = 1 #サイズと表示の倍率(ボールを大きく見せるため)
        self.color = (255,255,255)
        self.image = image_man1

    #表示オン
    def on(self, image_type,game_flag=0):
        self.status = 1
        self.image_type = image_type
        if self.image_type == 0: #私
            self.jump_status = 1
            self.x = -200
            self.y = -10
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.width = 100
            self.height = 170
            self.image = image_man1_1


class Player:
    def __int___(self,pos,motion):
        self._pos = dict(pos)  # pos を辞書型として保存
        self._motion = dict(motion)  # motion を辞書型として保存
        # 初期化時0
        # pos={'x':x,'y':y,'z':z},motion={'v':v,'theta':theta 仰角,'phi':phi 方位角}

    def check_move(self,pos2,t):
        distance = math.sqrt((self._pos['x'] - pos2['x'])**2 +(self._pos['y'] -pos2['y']) **2)
        return distance <=max_distance(t): 

if __name__ == "__main__":
    main()
