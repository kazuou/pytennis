import math
import copy

# スケーリング倍-
scale = 20
field_width = int(20.97 * scale)
field_height = int(33.79 * scale)

# 原点定義
center_x = field_width // 2
center_y = field_height // 2 + 100

# コート描画
court_width = int(10.97 * scale)
court_height = int(23.79 * scale)
court_top = 11.895
court_bottom = -11.895
court_l = -4.115
court_r = 4.116
service_line = 6.40
controler_y = field_height + 100
field_bottom = (center_y - field_height - 100) / scale
field_top = (center_y - 100) / scale
field_l = -16.89
field_r = 16.89

g = 9.8

# プレイヤー設定
player_vmax = 5

# ボール設定
BALL_RADIUS = 0.05
ball_vmax = 30  # 時速100kmは秒速28mです。
ball_vzmax = 10  # 秒速9.9m/sで5m打ち上がる
ball_vzmin = -10

ballhit = []

# 状態管理
turn = 0

"""
# 0(ready) 次は1 or 3
# 1(Player1 recive move 次は3
# 2(Player2 service and move 次は11
#
# 3 Player2 receve move 次は4
# 4 Player1 service hite and move 次は13

# 4,11,12,13,14
# 11 player1 catch ,hit,move 次は13
# 20 player1 catch ,hit,move 次は11

# 20 win a point
"""


def adjust_target(p_pos, p_pos_target, time_limit):
    x1, y1 = p_pos
    x2, y2 = p_pos_target
    distance = math.hypot(x2 - x1, y2 - y1)
    max_distance = player_vmax * time_limit
    if distance <= max_distance:
        return [x2, y2]  # リスト形式で返却
    else:
        ratio = max_distance / distance
        new_x = x1 + (x2 - x1) * ratio
        new_y = y1 + (y2 - y1) * ratio
        return [new_x, new_y]


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


class Action:
    def __init__(self, hitpoint, ball_landing_pos, vz, target_pos):
        self.hitpoint = hitpoint  # [x, y, z, t]
        self.ball_landing_pos = ball_landing_pos  # [x, y]
        self.vz = vz
        self.target_pos = target_pos  # [x, y]


def check_net(ball_pos, ball_landing_pos, ball_vz):
    dx = ball_landing_pos[0] - ball_pos[0]
    dy = ball_landing_pos[1] - ball_pos[1]

    t_flight = (ball_vz + math.sqrt(ball_vz**2 + 2 * g * ball_pos[2])) / g

    ball_vx = dx / t_flight
    ball_vy = dy / t_flight

    # y=0の時間
    t0 = -ball_pos[1] / ball_vy
    a = 0.5 * g
    z0 = ball_pos[2] + ball_vz * t0 - a * t0 * t0
    x0 = ball_pos[0] + ball_vx * t0
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


# アクション適用
# p1どこで取るか。(x,y,z,t) ===>p1_pos
#                             p2_pos
# p1どこに打ち返すか(x,y,vz) ===>ball_pos,landing_pos,vz
# p1どこに移動するか p1_target_pos
#
# p1_pos
# ball_pos
# vz
# landing_pos
# p1_target_pos
# p2_pos
# p2_target_pos

# p2どこで取るか


# next_state = apply_action(state, action, 1)
def apply_action(state, action: Action, player):
    """
    action.p1_target_pos
    action.p2_target_pos
    action.landign_pos
    """
    new_state = copy.deepcopy(state)
    new_state.next_turn()
    new_state.catch(action.hitpoint)
    new_state.hit(action.ball_landing_pos, action.vz)
    new_state.move(action.target_pos)

    return new_state


def grid_points(x1, x2, interval=1.0, center=None):
    if center is None:
        center = round((x1 + x2) / 2, 2)
    # x, y 軸のメッシュリスト
    min_x, max_x = min(x1, x2), max(x1, x2)
    x_list = [center]
    x1 = center + interval
    x2 = center - interval
    while x1 <= max_x:
        x_list.append(round(x1, 2))
        x1 += interval

    while x2 >= min_x:
        x_list.append(round(x2, 2))
        x2 -= interval
    return x_list


def mesh_points(range_xy, interval=1.0):
    """
    指定矩形範囲内をinterval間隔のグリッドで全ポイントを返す。
    範囲の中心点を必ず含むように調整する。

    range_xy: ((x1, y1), (x2, y2))
    interval: メッシュ間隔（デフォルト1.0）

    戻り値: [(x, y), ...]
    """
    (x1, y1), (x2, y2) = range_xy
    # x, y 軸のメッシュ用リスト
    x_list = grid_points(x1, x2, interval)
    y_list = grid_points(y1, y2, interval)

    # 全点の組み合わせ
    """
    result = []
    for x in x_list:
        for y in y_list:
            result.append((x, y))
    """
    points = [(x, y) for x in x_list for y in y_list]
    return points


def rangeB(turn):
    rangeB1 = ((court_l, 1), (court_r, court_top))
    rangeB1S1 = ((court_l, 1), (0, service_line))
    rangeB1S2 = ((0, 1), (court_r, service_line))
    rangeB2 = ((court_l, court_bottom), (court_r, -1))
    rangeB2S1 = ((0, -service_line), (court_r, -1))
    rangeB2S2 = ((court_l, -service_line), (0, -1))
    if turn == 1:
        return rangeB1S1
    if turn == 2:
        return rangeB1S2
    if turn == 3:
        return rangeB2S1
    if turn == 4:
        return rangeB2S2
    if turn == 12:
        return rangeB1
    if turn == 14:
        return rangeB2


def rangeP1(turn):
    rangeP1 = ((field_l, field_bottom), (field_r, -1))
    rangeP1S1 = ((0, court_bottom - 1), (court_r, court_bottom))
    rangeP1S2 = ((court_l, court_bottom - 1), (0, court_bottom))

    if turn == 1:
        return rangeP1S1
    elif turn == 2:
        return rangeP1S2
    else:
        return rangeP1


def rangeP2(turn):
    rangeP2 = ((field_l, 1), (field_r, field_top))
    rangeP2S1 = ((court_l, court_top), (0, court_top + 1))
    rangeP2S2 = ((0, court_top), (court_r, court_top + 1))
    if turn == 3:
        return rangeP2S1
    elif turn == 4:
        return rangeP2S2
    else:
        return rangeP2


# メインループ
def main():
    state = GameState(
        p1_pos=(0, -11.90),  # 手前
        p2_pos=(0, 11.90),  # 奥
        ball_pos=(0, -11.90, 1.00),
        vz=1,
        turn=1,
    )

    for turn in (1, 2, 3, 4, 12, 14):
        print("turn=", turn)
        print("rangeB =", rangeB(turn))
        print("rangeP1=", rangeP1(turn))
        print("rangeP2=", rangeP2(turn))

    # アクション生成
    # def generate_possible_actions(state, player):
    catch = ((0, -10, 0.5, 1), (1, -10, 1, 0.5, 1))
    ab = mesh_points(rangeB(state.turn), interval=3.0)
    ap1 = mesh_points(rangeB(state.turn), interval=3.0)
    i = 0
    for p1 in catch:
        for lp in ab:
            for vz in (5, 10):
                if check_net(p1[0:3], lp, vz):
                    for p1t in ap1:
                        i = i + 1
                        new_action = Action(p1, lp, vz, p1t)
                        print("===i===", i)
                        print(new_action.hitpoint)
                        print(new_action.ball_landing_pos)
                        print(new_action.vz)
                        print(new_action.target_pos)
    print("len(catch)=", len(catch))
    print("len(ball)=", len(ab))
    print("len(playter1)=", len(ap1))
    print(len(ap1))


if __name__ == "__main__":
    main()
