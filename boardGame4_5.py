import pygame
import sys
import math


def rgb(r, g, b):
    return (r, g, b)


# 初期化
pygame.init()

# スケーリング倍-
scale = 0.2
field_width = int(2097 * scale)
field_height = int(3379 * scale)


# 画面設定
screen = pygame.display.set_mode((field_width, field_height + 200))
pygame.display.set_caption("テニスボードゲーム")
clock = pygame.time.Clock()

# 色定義
GREEN = rgb(0, 128, 0)
BLUE = rgb(0, 102, 204)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = rgb(200, 200, 200)
GRAY2 = rgb(150, 150, 150)
YELLOW = (255, 255, 0)

# 原点定義
center_x = field_width // 2
center_y = field_height // 2 + 100

# プレイヤー設定
player_radius = 10
p1_pos = [0, -1190]  # 手前
p2_pos = [0, 1190]  # 奥
p1_pos_target = p1_pos[:]
p2_pos_target = p2_pos[:]

# コート描画
court_width = int(1097 * scale)
court_height = int(2379 * scale)
court_rect = pygame.Rect(
    center_x - court_width // 2,
    center_y - court_height // 2,
    court_width,
    court_height,
)
scoreBoard_y = 0
scoreBoard_rect = pygame.Rect(0, 0, field_width, 100)
controler_y = field_height + 100
controler_rect = pygame.Rect(0, controler_y, field_width, field_height + 200)
field_bottom = (center_y - field_height - 100) / scale
field_top = (center_y - 100) / scale

# field_width = int(2097 * scale)
# field_height = int(3379 * scale)
# controler_height = 100
p_move_candidates = ((100, 500, 100, 2), (200, 550, 100, 1), (300, 600, 100, 2))

r = []  # 結果を入れるリスト


def draw_court():
    lines = (
        ((-548.5, 1189.5), (548.5, 1189.5), 10),  # ベースライン
        ((-411.5, 640), (411.5, 640), 5),  # サービスライン
        ((0, 1189.5), (0, 1178.5), 5),  # センターマーク
        ((-548.5, 1189.5), (-548.5, -1189.5), 5),  # サイドライン左
        ((-411.5, 1189.5), (-411.5, -1189.5), 5),  # シングルスライン左
        ((0, 640), (0, -640), 5),  # センターライン
        ((411.5, 1189.5), (411.5, -1189.5), 5),  # シングルスライン右
        ((548.5, 1189.5), (548.5, -1189.5), 5),  # サイドライン右
        ((0, -1189.5), (0, -1178.5), 5),  # センターマーク
        ((-411.5, -640), (411.5, -640), 5),  # シングルスライン右
        ((-5029, 0), (5029, 0), 10),  # ネットS
        ((-6399, 0), (6399, 0), 10),  # ネットD
        ((-548.5, -1189.5), (548.5, -1189.5), 10),  # ベースライン下
    )

    screen.fill(GREEN)
    pygame.draw.rect(screen, BLUE, court_rect)
    pygame.draw.rect(screen, GRAY2, scoreBoard_rect)
    pygame.draw.rect(screen, GRAY2, controler_rect)

    # pygame.draw.line(screen, WHITE, (0, center_y), (field_width, center_y), 2)
    for start, end, width in lines:
        start_screen = (
            start[0] * scale + field_width // 2,
            start[1] * scale + center_y,
        )
        end_screen = (
            end[0] * scale + field_width // 2,
            end[1] * scale + center_y,
        )
        width_screen = round(width * scale)
        pygame.draw.line(screen, WHITE, start_screen, end_screen, width_screen)


# ボール設定
ball_radius = 5
ball_pos = [p1_pos[0], p1_pos[1], 100]
ball_vx = 0
ball_vy = 0
ball_vz = 0
g = 9.8
ball_vmax = 30  # 時速100kmは秒速28mです。
ball_vzmax = 10  # 秒速9.9m/sで5mm打ち上がる

# 状態管理
turn = 1
ball_flying = False
ball_landing_pos = None
ball_landing_pos2 = None
current_player = p1_pos

p1_point = 0
p2_point = 0
p1_games = 0
p2_games = 0
shot = 0
coartChange = 0


# スライダー設定
slider_length = 150
slider_height = 10
slider_x = 50
z_slider_y = controler_y + 20
h_slider_y = controler_y + 60

z_slider_val = ball_vzmax // 2
h_slider_val = ball_vmax // 2

ok_button_x = slider_x + slider_length + 150
ok_button_y = controler_y + 20

# draw_slider(slider_x, z_slider_y, z_slider_val, 20, "Z速度")
# draw_slider(slider_x, h_slider_y, h_slider_val, 40, "水平速度")
message2 = "プレイ"


def draw_slider(x, y, value, max_val, label):
    """スライダー描画"""
    pygame.draw.rect(screen, GRAY, (x, y, slider_length, slider_height))
    knob_x = int(x + (value / max_val) * slider_length)
    pygame.draw.rect(screen, RED, (knob_x - 5, y - 5, 10, slider_height + 10))
    # font = pygame.font.SysFont(None, 24)
    font = pygame.font.SysFont("ヒラキノ角コシックw3", 16)

    text = font.render(f"{label}: {value:.1f}", True, BLACK)
    screen.blit(text, (x + slider_length + 10, y - 5))


# OKボタン設定
ok_button_rect = pygame.Rect(ok_button_x, ok_button_y, 60, 30)


def draw_ok_button():
    # OKボタン設定
    pygame.draw.rect(screen, BLUE, ok_button_rect)
    font = pygame.font.SysFont("ヒラキノ角コシックw0", 18)
    text = font.render("OK", True, WHITE)
    text_rect = text.get_rect(center=ok_button_rect.center)
    screen.blit(text, text_rect)


def handle_slider_input(mouse_pos):
    """スライダー"""
    global z_slider_val, h_slider_val
    global message2
    mx, my = mouse_pos
    if not ball_landing_pos:
        return
    z1 = ball_pos[2] / 100
    dx = (ball_landing_pos[0] - current_player[0]) / 100
    dy = (ball_landing_pos[1] - current_player[1]) / 100
    # 時速100kmは秒速28mです。

    if z_slider_y <= my <= z_slider_y + slider_height + 10:
        # zスライダーを操作したときの処理
        ratio = (mx - slider_x) / slider_length
        z_slider_val = max(1, min(ball_vzmax, ratio * ball_vzmax))
        t = (z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * z1)) / g
        h_slider_val = math.hypot(dx, dy) / t  # h_slider_valの値を更新する。
        # message2 = "mys=" + f"{z_slider_val:.2f}" + " y=" + f"{h_slider_val:.2f}"
    elif h_slider_y <= my <= h_slider_y + slider_height + 10:
        # hスライダーを操作したときの思慮
        ratio = (mx - slider_x) / slider_length
        h_slider_val = max(1, min(ball_vmax, ratio * ball_vmax))
        t = math.hypot(dx, dy) / h_slider_val
        # z_slider_valの値を更新する。
        z_slider_val = (t * g - math.sqrt(t**2 * g**2 - 4 * g * z1)) / 2
        # message2 = "mys=" + f"{z_slider_val:.2f}" + " y=" + f"{h_slider_val:.2f}"


def draw_landing_marker():
    pos = ball_landing_pos
    if pos:
        x, y = int(center_x + pos[0] * scale), int(center_y - pos[1] * scale)
        pygame.draw.line(screen, RED, (x - 5, y), (x + 5, y), 2)
        pygame.draw.line(screen, RED, (x, y - 5), (x, y + 5), 2)

    pos = ball_landing_pos2
    if pos:
        x, y = int(center_x + pos[0] * scale), int(center_y - pos[1] * scale)
        pygame.draw.line(screen, RED, (x - 5, y), (x + 5, y), 2)
        pygame.draw.line(screen, RED, (x, y - 5), (x, y + 5), 2)


def draw_candidates(candidate_list):
    """ボールを受け取る場所をxで表示"""
    for x, y in candidate_list:
        if (x, y) == p2_pos_target:
            pygame.draw.line(screen, RED, (x - 5, y - 5), (x + 5, y + 5), 2)
            pygame.draw.line(screen, RED, (x - 5, y + 5), (x + 5, y - 5), 2)
        else:
            pygame.draw.line(screen, BLACK, (x - 5, y - 5), (x + 5, y + 5), 2)
            pygame.draw.line(screen, BLACK, (x - 5, y + 5), (x + 5, y - 5), 2)


def TargetArea1(z1):
    areaShot = (
        ((-411.5, 1189.5), (411.5, 100)),  # エリエリア
        ((-411.5, -1189.5), (411.5, -100)),  # エリエリア
    )
    areaService = (
        ((-411.5, 640), (0, 100)),  # サービス手前からduce
        ((0, 640), (411.5, 100)),  # エリエリア手前からad
        ((-411.5, -100), (0, -640)),  # エリエリア奥からad
        ((0, -100), (411.5, -640)),  # エリエリア奥からduce
    )
    if shot == 0:
        return areaService((p1_games + p2_games) % 2)
    else:
        return areaShot(shot % 2)


def TargetArea3():
    areaPlayer = (
        ((-1048.5, 1689.5), (1048.5, 100)),  # エリエリア
        ((-1048.5, -1689.5), (1048.5, -100)),  # エリエリア
        ((-411.5, 1190), (0, 1200)),  # エリエリア サービス奥duce
        ((0, 1190), (411.5, 1200)),  # エリエリア  サービス奥ad
        ((0, -1190), (411.5, -1200)),  # エリエリア サービス奥duce
        ((-411.5, -1190), (0, -1200)),  # エリエリア サービス手前ad
    )
    return areaPlayer(shot % 2)


def compute_vz(z1, z0, t):
    return (z0 - z1 + 0.5 * g * t**2) / t


def maxvz(z1):
    """高さz1から天井5mに当たらないように投げるときの最大vz"""
    z_max = 500
    return math.sqrt(2 * g * (z_max - z1))


def time_to_z(z1, vz, z, g=9.8):
    a = 0.5 * g
    b = -vz
    c = z1 - z

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None  # 1.5m に到達しない

    sqrt_d = math.sqrt(discriminant)
    # t1 = (-b - sqrt_d) / (2 * a) # 上昇時
    t2 = (-b + sqrt_d) / (2 * a)  # 下降時
    return t2


def draw_trajectory(start_pos, vx, vy, vz, z0=1.0, steps=50):
    """ボールの軌道を表示"""
    path = []
    t = 0.0
    dt = 0.05
    g = 9.8
    coef = 0.8
    # 1回目のバウンドまでの時間
    t1 = (vz + math.sqrt(vz**2 + 2 * g * z0)) / g

    # バウンド直前の速度（下向き）
    vz_impact = math.sqrt(vz**2 + 2 * g * z0)

    # 反射後の上向き速度
    vz2 = coef * vz_impact

    # 2回目のバウンドまでの時間（上昇＋落下）
    t2 = 2 * vz2 / g + t1

    while True:
        if t > t2:
            # z = z0 + vz * t - 0.5 * g * t**2
            # if z < 0:
            break
        x = center_x + (start_pos[0] + vx * t) * scale
        y = center_y - (start_pos[1] + vy * t) * scale
        path.append((int(x), int(y)))
        t += dt
    if len(path) >= 2:
        pygame.draw.lines(screen, YELLOW, False, path, 2)


def format_point(p):
    return ["0", "15", "30", "40", "G"][min(p, 4)]


def draw_scoreboard():
    font = pygame.font.SysFont("Arial", 24)

    score_text = f"P1: {format_point(p1_point)} ({p1_games})  -  P2: {format_point(p2_point)} ({p2_games})"
    score_surface = font.render(score_text, True, BLUE)
    screen.blit(score_surface, (field_width // 2 - score_surface.get_width() // 2, 10))

    msg_font = pygame.font.SysFont("ヒラキノ角コシックw3", 18)

    if turn == 1:
        message = "P1 打ってください"
    elif turn == 2:
        message = "P2 取りに行って"
    elif turn == 3:
        message = "P2 打ってください"
    elif turn == 4:
        message = "P1 取りに行って"
    elif turn == 5:
        message = ""
    else:
        message = ""

    msg_surface = msg_font.render(message, True, BLACK)
    screen.blit(msg_surface, (field_width // 2 - msg_surface.get_width() // 2, 45))

    msg_surface = msg_font.render(message2, True, BLACK)
    screen.blit(msg_surface, (field_width // 2 - msg_surface.get_width() // 2, 65))


# メインループ
while True:
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
            mxs, mys = pygame.mouse.get_pos()

            mx = (mxs - center_x) / scale
            my = (center_y - mys) / scale
            print(
                "turn=",
                turn,
                "mx,my,mxs,mys=",
                mx,
                my,
                mxs,
                mys,
                center_y,
                field_top,
                field_bottom,
            )
            # message2 = "mys=" + f"{mys:.2f}" + " y=" + f"{my:.2f}"

            # OKボタンクリックでターンを進める（打ち終わり時にのみ）
            if ok_button_rect.collidepoint(mxs, mys):
                if turn == 1:
                    turn = 2
                elif turn == 3:
                    turn = 4
                elif turn == 2:
                    ball_flying = True
                elif turn == 4:
                    ball_flying = True

            if turn == 1:
                print("turn=1", my, field_bottom, field_top)
                if my < field_bottom:
                    handle_slider_input((mxs, mys))
                elif field_top > my > 100:
                    """
                    プレーヤー1のターン
                    プレーヤー1はy>0に打つ
                    プレーヤー1はy<0に移動する
                    """
                    print("turn=1 ballhit")
                    ball_landing_pos = (mx, my)
                    current_player = p1_pos
                    dx = (mx - ball_pos[0]) / 100
                    dy = (my - ball_pos[1]) / 100
                    t_flight = (
                        z_slider_val
                        + math.sqrt(z_slider_val**2 + 2 * g * ball_pos[2] / 100)
                    ) / g

                    ball_vx = dx / t_flight
                    ball_vy = dy / t_flight
                    ball_vz = z_slider_val

                    v_land = ball_vz - g * t_flight  # 着地時の速度（負の値）
                    v_rebound = -v_land * 0.8  # 跳ね返り初速（正の値）

                    t_bounce = 2 * v_rebound / g  # 上下で対称な時間（頂点までと落下）
                    t_flight2 = t_flight + t_bounce  # 2回目の着地時刻

                    ball_landing_pos2 = (
                        ball_pos[0] + ball_vx * t_flight2 * 100,
                        ball_pos[1] + ball_vy * t_flight2 * 100,
                    )

                elif field_bottom < my < -100:
                    p1_pos_target = [mx, my]

            elif turn == 3:
                print("turn=1", my, field_bottom, field_top)
                if my < field_bottom:
                    handle_slider_input((mxs, mys))
                elif field_bottom < my < -100:
                    ball_landing_pos = (mx, my)  # ボールの着地点
                    current_player = p2_pos  # プレーヤーの場所
                    dx = (mx - p2_pos[0]) / 100
                    dy = (my - p2_pos[1]) / 100
                    t_flight = (
                        z_slider_val
                        + math.sqrt(z_slider_val**2 + 2 * g * ball_pos[2] / 100)
                    ) / g

                    ball_vx = dx / t_flight
                    ball_vy = dy / t_flight
                    ball_vz = z_slider_val

                elif 100 < my < field_top:
                    p2_pos_target = [mx, my]

            elif turn == 2 and 100 < my < field_top:
                """
                    プレーヤー2のターン
                    プレーヤー1はy>0に打った
                """
                print("turn=2 player2 move")
                for candidate in p_move_candidates:
                    if math.hypot(mx - candidate[0], my - candidate[1]) < 10:
                        p2_pos_target = candidate
                        break
                p2_pos_target = [mx, my]

            elif turn == 4 and field_bottom < my < -100:
                p1_pos_target = [mx, my]

    message2 = "p1x=" + f"{p1_pos_target[0]:.2f}" + "p1y=" + f"{p1_pos_target[1]:.2f}"
    # ボール更新
    if ball_flying:
        ball_pos[0] += ball_vx * 2
        ball_pos[1] += ball_vy * 2
        ball_pos[2] += ball_vz * 2
        ball_vz -= g * 0.02

        if turn == 2:
            if ball_pos[1] > p2_pos[1]:
                ball_flying = False
        if turn == 4:
            if ball_pos[2] < p1_pos[1]:
                ball_flying = False
        if not ball_flying:
            if turn == 2:
                turn = 3
                ball_landing_pos = None
                ball_landing_pos2 = None
                p1_pos = p1_pos_target
                p2_pos = p2_pos_target
                ball_pos = [p2_pos_target[0], p2_pos_target[1], 50]
            elif turn == 4:
                turn = 1
                ball_landing_pos = None
                ball_landing_pos2 = None
                p1_pos = p1_pos_target
                p2_pos = p2_pos_target
                ball_pos = [p1_pos_target[0], p1_pos_target[1], 50]
            print(turn)

    # 描画処理
    # コート描画
    draw_court()

    # プレーヤー2描画
    pygame.draw.circle(
        screen,
        RED,
        (int(center_x + p1_pos[0] * scale), int(center_y - p1_pos[1] * scale)),
        player_radius,
    )
    # プレーヤー2描画
    pygame.draw.circle(
        screen,
        BLACK,
        (int(center_x + p2_pos[0] * scale), int(center_y - p2_pos[1] * scale)),
        player_radius,
    )

    if ball_flying:
        # 飛んでいるボールを描画
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(center_x + ball_pos[0] * scale), int(center_y - ball_pos[1] * scale)),
            ball_radius,
        )

    if ball_landing_pos:
        draw_landing_marker()

    if turn in (1, 3) and ball_landing_pos:
        dx = ball_landing_pos[0] - current_player[0]
        dy = ball_landing_pos[1] - current_player[1]
        t_flight = (z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * 1.0)) / g
        vx = dx / t_flight
        vy = dy / t_flight
        vz = z_slider_val
        draw_trajectory(current_player, vx, vy, vz)

    if turn in (1, 3) and ball_landing_pos:
        draw_slider(slider_x, z_slider_y, z_slider_val, ball_vzmax, "Z速度")
        # 初速9.9m/sで5m打ち上げられる
        draw_slider(slider_x, h_slider_y, h_slider_val, ball_vmax, "水平速度")
        #

    if turn in (2, 4):
        p_move_candidates = [(100, 500), (200, 550), (300, 600)]
        draw_candidates(p_move_candidates)

    draw_ok_button()

    draw_scoreboard()

    pygame.display.flip()
    clock.tick(60)
