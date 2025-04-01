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
