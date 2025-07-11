import copy
from core.judge import adjust_target
import config


# 状態クラス
class GameState:
    def __init__(self, hitter_pos, defender_pos, defender_target_pos, ball_catch, turn):
        # この下がステート。
        self.hitter_pos = hitter_pos
        self.defender_pos = defender_pos
        self.defender_target_pos = defender_target_pos
        self.ball_catch = ball_catch
        self.turn = turn

        # この下はアクション。まだ決めてないので初期化する。。
        self.ball_pos = [0, 0, 0]  # 自分が打つボール
        self.vz = 0  # 自分が打つボールのVZ
        self.ball_landing_pos = None
        self.ball_landing_pos2 = None
        self.ballhit = []
        self.hitter_target_pos = None

    def GameStageChange(self):
        # GameStateをdeepcopyした後に、次のturnのstateにする。
        temp = self.defender_pos[:]
        self.defender_pos = self.hitter_pos[:]
        self.hitter_pos = temp[:]
        self.defender_target_pos = copy.copy(self.hitter_target_pos)
        self.ball_catch = copy.deepcopy(self.ballhit)

        # この下はアクション
        self.ball_pos = [0, 0, 0]  # 自分が打つボール
        self.vz = 0  # 自分が打つボールのVZ
        self.ball_landing_pos = None
        self.ball_landing_pos2 = None
        self.ballhit = []
        self.hitter_target_pos = None
        if self.turn == 1:
            # player1 receve ==> player2 sevice
            self.turn = 2
        elif self.turn == 2:
            # player2 service ==>player1 catch and hit
            self.turn = 11
        elif self.turn == 3:
            self.turn = 4
        elif self.turn == 4:
            self.turn = 13
        elif self.turn == 11:
            self.turn = 13
        elif self.turn == 13:
            self.turn = 11
        else:
            self.turn = 0

    def catch(self, hitpoint):
        # ボールをキャッチする。
        # hitter移動 defender_target_posへ向かって
        #
        x, y, z, t = hitpoint

        self.hitter_pos = [x, y]
        self.defender_pos = adjust_target(
            self.defender_pos, self.defender_target_pos, t
        )
        self.defender_target_pos = self.defender_pos[:]
        self.ball_pos = [x, y, z]

    def hit(self, ball_landing_pos, vz):
        #
        self.ball_landing_pos = ball_landing_pos
        self.vz = vz
        dx = self.ball_landing_pos[0] - self.ball_pos[0]
        dy = self.ball_landing_pos[1] - self.ball_pos[1]
        t_flight = (self.vz + math.sqrt(self.vz**2 + 2 * g * self.ball_pos[2])) / g

        ball_vx = dx / t_flight
        ball_vy = dy / t_flight
        ball_vz = self.vz

        # y=0の時間
        t0 = -self.ball_pos[1] / ball_vy
        a = 0.5 * g
        z0 = self.ball_pos[2] + ball_vz * t0 - a * t0 * t0
        x0 = self.ball_pos[0] + ball_vx * t0
        self.ballhit = []
        if self.check_net(x0, z0):
            v_land = ball_vz - g * t_flight  # 着地時の速度（負の値）
            v_rebound = -v_land * 0.8  # 跳ね返り初速（正の値）

            t_bounce = 2 * v_rebound / g  # 上下で対称な時間（頂点までと落下）
            t_flight2 = t_flight + t_bounce  # 2回目の着地時刻

            self.ball_landing_pos2 = (
                self.ball_pos[0] + ball_vx * t_flight2,
                self.ball_pos[1] + ball_vy * t_flight2,
            )

            for i in range(3, 20):
                z = i * 0.1

                b = -ball_vz
                c = z - self.ball_pos[2]
                discriminant = b**2 - 4 * a * c
                if discriminant > 0 and self.turn >= 11:
                    sqrt_d = math.sqrt(discriminant)
                    t1 = (-b - sqrt_d) / (2 * a)  # 上昇時
                    if t1 > t0:
                        x1 = self.ball_pos[0] + ball_vx * t1
                        y1 = self.ball_pos[1] + ball_vy * t1
                        ballhit.append((x1, y1, z, t1))
                    t2 = (-b + sqrt_d) / (2 * a)  # 下降時
                    if t2 > t0:
                        x2 = self.ball_pos[0] + ball_vx * t2
                        y2 = self.ball_pos[1] + ball_vy * t2
                        ballhit.append((x2, y2, z, t2))
                b = -v_rebound
                c = z  # 高さ0からの2バウンド目
                discriminant = b**2 - 4 * a * c
                if discriminant > 0:
                    sqrt_d = math.sqrt(discriminant)
                    t1 = (-b - sqrt_d) / (2 * a) + t_flight  # 上昇時
                    x1 = self.ball_pos[0] + ball_vx * t1
                    y1 = self.ball_pos[1] + ball_vy * t1
                    ballhit.append((x1, y1, z, t1))
                    t2 = (-b + sqrt_d) / (2 * a) + t_flight  # 下降時
                    x2 = self.ball_pos[0] + ball_vx * t2
                    y2 = self.ball_pos[1] + ball_vy * t2
                    ballhit.append((x2, y2, z, t2))
            # 4つ目の値（index 3）でソート
            self.ballhit = sorted(self.ballhit, key=lambda x: x[3])

        else:
            # ボールのlanding_makerはネットの位置
            self.self_landing_pos = x0, 0, z0, t0
            self.self_landing_pos2 = None

    def move(self, target_pos):
        self.hitter_target_pos = target_pos

    def check_net(self, x0, z0):
        # =(1.07-0.914)*abs(x)/5.029
        # =(1.07-0.914)*abs(x)/6.399
        # BALL_RADIUS = 0.05
        pole = 5.029  # シングルスの場合。ダブルスは6.399
        if x0 > pole + BALL_RADIUS:
            return True
        if x0 < -pole - BALL_RADIUS:
            return True
        if z0 > (1.07 - 0.914) * abs(x0) / pole + 0.914 + BALL_RADIUS:
            return True
        return False

    def is_terminal(self):
        if len(ballhit) == 0:
            return 1
        elif self.ball_landing_pos2 is None:
            return -1
        else:
            return 0

    def evelute(self):
        if len(ballhit) == 0:
            return 1
        elif self.ball_landing_pos2 is None:
            return -1
        else:
            return 0
