import pygame
import sys
import math
import socket

# from core.status import GameState
from core.judge import adjust_target
import config


def rgb(r, g, b):
    return (r, g, b)


# 自分のホスト名からIPアドレスを取得
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)

# IPアドレスをドットで分割して、最後の部分を取得
last_octet = ip_address.split(".")[-1]


print(f"最後のIPアドレスの数字は: {last_octet}")

# if socket.gethostname() == "Cortina.local":
# if host_name == "Cortina.local":
keywords = ("Coltina", "Anber", "Wimbledon")
keywords2 = "Candace"

if any(keyword in host_name for keyword in keywords):
    print("in Cortina")
    # filename = "FontPygame72"
    fontname = "ヒラキノ角コシックw5"
elif any(keyword in host_name for keyword in keywords2):
    print("in candace")
    last_octet = 74
    fontname = "notosansmonocjkjp"
else:
    # filename = "FontPygame"
    fontname = "yugothic"

# 初期化
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
print("screen size=", screen_width, screen_height)
# スケーリング
scale = 20
field_width = int(20.97 * scale)
field_height = int(33.79 * scale)

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


# コート描画
court_width = int(10.97 * scale)
court_height = int(23.79 * scale)
court_rect = pygame.Rect(
    center_x - court_width // 2,
    center_y - court_height // 2,
    court_width,
    court_height,
)
court_top = 11.895
court_bottom = -11.895
court_l = -4.115
court_r = 4.116
service_line = 6.40

scoreBoard_y = 0
scoreBoard_rect = pygame.Rect(0, 0, field_width, 100)
controler_y = field_height + 100
controler_rect = pygame.Rect(0, controler_y, field_width, field_height + 200)
field_bottom = (center_y - field_height - 100) / scale
field_top = (center_y - 100) / scale
field_l = -16.89
field_r = 16.89


# プレイヤー設定
player_radius = 10
p1_pos = [0, -11.90]  # 手前
p2_pos = [0, 11.90]  # 奥
p1_pos_target = p1_pos[:]
p2_pos_target = p2_pos[:]
# player_vmax = 5

# field_width = int(2097 * scale)
# field_height = int(3379 * scale)
# controler_height = 100
ballhit = []


# ボール設定
BALL_RADIUS = 0.05
ball_pos = [p1_pos[0], p1_pos[1], 1.00]
ball_pos_target = [p1_pos[0], p1_pos[1], 1.00, 0]
ball_vx = 0
ball_vy = 0
ball_vz = 0
g = 9.8
ball_vmax = 30  # 時速100kmは秒速28mです。
ball_vzmax = 10  # 秒速9.9m/sで5m打ち上がる
ball_vzmin = 1

# 状態管理
turn = 0
ball_flying = False
ball_landing_pos = None
ball_landing_pos2 = None
current_player = p1_pos[:]
difensive_player = p2_pos[:]
current_ball = ball_pos[:]

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

z_slider_val = (ball_vzmax - ball_vzmax) // 2
h_slider_val = ball_vmax // 2

ok_button_x = slider_x + slider_length + 150
ok_button_y = controler_y + 20

# draw_slider(slider_x, z_slider_y, z_slider_val, 20, "Z速度")
# draw_slider(slider_x, h_slider_y, h_slider_val, 40, "水平速度")
message2 = "プレイ"


class Action:
    def __init__(self, hitpoint, ball_landing_pos, vz, target_pos):
        self.hitpoint = hitpoint  # [x, y, z, t]
        self.ball_landing_pos = ball_landing_pos  # [x, y]
        self.vz = vz
        self.target_pos = target_pos  # [x, y]


def draw_court():
    lines = (
        ((-5.485, 11.895), (5.485, 11.895), 0.10),  # ベースライン
        ((-4.115, 6.40), (4.115, 6.40), 0.05),  # サービスライン
        ((0, 11.895), (0, 11.785), 0.05),  # センターマーク
        ((-5.485, 11.895), (-5.485, -11.895), 0.05),  # サイドライン左
        ((-4.115, 11.895), (-4.115, -11.895), 0.05),  # シングルスライン左
        ((0, 6.40), (0, -6.40), 0.05),  # センターライン
        ((4.115, 11.895), (4.115, -11.895), 0.05),  # シングルスライン右
        ((5.485, 11.895), (5.485, -11.895), 0.05),  # サイドライン右
        ((0, -11.895), (0, -11.785), 0.05),  # センターマーク
        ((-4.115, -6.40), (4.115, -6.40), 0.05),  # シングルスライン右
        ((-5.029, 0), (5.029, 0), 0.10),  # ネットS
        ((-6.399, 0), (6.399, 0), 0.10),  # ネットD
        ((-5.485, -11.895), (5.485, -11.895), 0.10),  # ベースライン下
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


def AIstart():
    global ai_result, ai_thinking
    print("AIstart")
    # ai_result = minimax(state, MAX_DEPTH, True)
    ai_thinking = False


def initplay():
    global p1_pos, p2_pos, p1_pos_target, p2_pos_target, ball_pos, ball_pos_target
    global current_player, difensive_player, current_ball
    global ball_flying, ball_landing_pos, ball_landing_pos2
    global shot
    global p1_point, p2_point, p1_games, p2_games, turn
    p1_pos = [0, -11.90]  # 手前
    p2_pos = [0, 11.90]  # 奥
    p1_pos_target = p1_pos[:]
    p2_pos_target = p2_pos[:]
    ball_pos = [p1_pos[0], p1_pos[1], 1.00]
    ball_pos_target = [p1_pos[0], p1_pos[1], 1.00, 0]
    current_player = p1_pos[:]
    difensive_player = p2_pos[:]
    current_ball = ball_pos[:]
    ball_flying = False
    ball_landing_pos = None
    ball_landing_pos2 = None
    shot = 0
    if p1_point >= 4:
        p1_point = 0
        p2_point = 0
        p1_games += 1

    if p2_point >= 4:
        p1_point = 0
        p2_point = 0
        p2_games += 1
    if p1_games >= 4 or p2_games >= 4:
        turn = 22
    else:
        turn = 0


def draw_slider(x, y, value, min_val, max_val, label):
    """スライダー描画"""
    pygame.draw.rect(screen, GRAY, (x, y, slider_length, slider_height))
    knob_x = int(x + (value / (max_val - min_val) * slider_length))
    pygame.draw.rect(screen, RED, (knob_x - 5, y - 5, 10, slider_height + 10))
    # font = pygame.font.SysFont(None, 24)
    font = pygame.font.SysFont(fontname, 16)

    text = font.render(f"{label}: {value:.1f}", True, BLACK)
    screen.blit(text, (x + slider_length + 10, y - 5))


# OKボタン設定
ok_button_rect = pygame.Rect(ok_button_x, ok_button_y, 60, 30)


def draw_ok_button():
    # OKボタン設定
    pygame.draw.rect(screen, BLUE, ok_button_rect)
    font = pygame.font.SysFont(fontname, 18)
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
    z1 = current_ball[2]
    dx = ball_landing_pos[0] - current_player[0]
    dy = ball_landing_pos[1] - current_player[1]
    # 時速100kmは秒速28mです。

    if z_slider_y <= my <= z_slider_y + slider_height + 10:
        # zスライダーを操作したときの処理
        ratio = (mx - slider_x) / slider_length
        z_slider_val = max(
            ball_vzmin, min(ball_vzmax, ratio * (ball_vzmax - ball_vzmin) + ball_vzmin)
        )
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


def draw_landing_marker(pos, COLOR, cross=False):
    # 場所にcross=True 「+」
    if pos:
        xs, ys = int(center_x + pos[0] * scale), int(center_y - pos[1] * scale)
        if cross:
            pygame.draw.line(screen, COLOR, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
            pygame.draw.line(screen, COLOR, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)
        else:
            pygame.draw.line(screen, COLOR, (xs - 5, ys), (xs + 5, ys), 2)
            pygame.draw.line(screen, COLOR, (xs, ys - 5), (xs, ys + 5), 2)


def draw_candidates(candidate_list, pos, pos_target):
    """ボールを受け取る場所をxで表示"""
    for x, y, z, t in candidate_list:
        xs = center_x + x * scale
        ys = center_y - y * scale
        if math.hypot(x - pos[0], y - pos[1]) < config.PLAYER_VMAX * t:
            if math.hypot(x - pos_target[0], y - pos_target[1]) < 0.1:
                pygame.draw.line(screen, RED, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
                pygame.draw.line(screen, RED, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)
            else:
                pygame.draw.line(screen, BLACK, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
                pygame.draw.line(screen, BLACK, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)
        else:
            pygame.draw.line(screen, GRAY2, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
            pygame.draw.line(screen, GRAY2, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)


def check_net(x0, z0):
    # =(1.07-0.914)*abs(x)/5.029
    # =(1.07-0.914)*abs(x)/6.399
    ball = 0.05
    pole = 5.029  # シングルスの場合。ダブルスは6.399
    if x0 > pole + ball:
        return True
    if x0 < -pole - ball:
        return True
    if z0 > (1.07 - 0.914) * abs(x0) / pole + 0.914 + ball:
        return True
    return False


def draw_trajectory(start_pos, vx, vy, tend):
    """ボールの軌道を表示"""
    path = []
    t = 0.0
    dt = 0.05

    while True:
        if t > tend:
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
    global message
    global message2
    font = pygame.font.SysFont("Arial", 24)

    score_text = f"P1: {format_point(p1_point)} ({p1_games})  -  P2: {format_point(p2_point)} ({p2_games})"
    score_surface = font.render(score_text, True, BLUE)
    screen.blit(score_surface, (field_width // 2 - score_surface.get_width() // 2, 10))

    msg_font = pygame.font.SysFont(fontname, 18)

    if turn == 0:
        message = "P1 P2 位置についてださい"
    elif turn == 2:
        message = "P2 サーブを打ってください"
    elif turn == 4:
        message = "P1 サーブを打ってください"

    elif turn == 11:  # <==4
        message = "P1 取りに行って"
    elif turn == 12:  # <==1
        message = "P1 打ってください"
    elif turn == 13:  # <==2
        message = "P2 取りに行って"
    elif turn == 14:  # <==3
        message = "P2 打ってください"
    elif turn == 20:  # <==5
        pass
    elif turn == 21:  # <==5
        if p1_games >= 4:
            message = "P1 Win Game End"
        else:
            message = "P2 Win Game End"
        pass
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
            # message2 = "mys=" + f"{mys:.2f}" + " y=" + f"{my:.2f}"

            # OKボタンクリックでターンを進める（打ち終わり時にのみ）
            if ok_button_rect.collidepoint(mxs, mys):
                print("turn=", turn, "bal_landing_pos", ball_landing_pos2)
                if turn in (4, 12) and ball_landing_pos2:
                    turn = 13
                    p2_pos_target = p2_pos[:]
                    # AIstart()
                elif turn in (2, 14) and ball_landing_pos2:
                    turn = 11
                    p1_pos_target = p1_pos[:]
                elif turn == 13 and p2_pos_target:
                    print(ball_pos_target)
                    print(ball_pos_target[3])
                    p1_pos_target = adjust_target(
                        p1_pos, p1_pos_target, ball_pos_target[3]
                    )
                    ball_flying = True
                elif turn == 11 and p1_pos_target:
                    p2_pos_target = adjust_target(
                        p2_pos, p2_pos_target, ball_pos_target[3]
                    )
                    ball_flying = True
                elif turn == 20:
                    initplay()
                elif turn == 0:
                    ball_landing_pos = None
                    ball_landing_pos2 = None
                    if (p1_games + p2_games) % 2 == 0:
                        turn = 4  # player1 service
                        current_player = p1_pos[:]
                        difensive_player = p2_pos[:]
                    else:
                        turn = 2  # player2 service
                        current_player = p2_pos[:]
                        difensive_player = p1_pos[:]
                    ball_pos = [current_player[0], current_player[1], 2.00]
                    ball_pos_target = [current_player[0], current_player[1], 2.00, 0]
                    current_ball = ball_pos[:]
                print("turn=", turn)

            if turn == 0:
                if (p1_games + p2_games) % 2 == 0:
                    # プレーヤー1はサービスをする場所を決める
                    # プレーヤー2は受け取る場所を決める
                    b2 = +1.00
                    t2 = field_top
                    l2 = field_l
                    r2 = field_r

                    b1 = court_bottom - 1
                    t1 = court_bottom
                    if (p1_point + p2_point) % 2 == 0:
                        l1 = 0
                        r1 = court_r
                    else:
                        l1 = court_l
                        r1 = 0
                else:
                    # プレーヤー2はサービスをする場所を決める
                    # プレーヤー1は受け取る場所を決める
                    b1 = field_bottom
                    t1 = -1.00
                    l1 = field_l
                    r1 = field_r

                    b2 = court_top
                    t2 = court_top + 1
                    if (p1_point + p2_point) % 2 == 0:
                        l2 = court_l
                        r2 = 0
                    else:
                        l2 = 0
                        r2 = court_r

                print("t2,my,b2=", t2, my, b2, l2, mx, r2)
                if t1 > my > b1 and l1 < mx < r1:
                    p1_pos = [mx, my]
                    p1_pos_target = p1_pos[:]
                    print("set p1_pos")
                elif t2 > my > b2 and l2 < mx < r2:
                    p2_pos = [mx, my]
                    p2_pos_target = p2_pos[:]
                    print("set p2_pos")

            if turn == 4:
                # プレーヤー1はサービスを打つ場所と移動先を指定する。
                if (p1_point + p2_point) % 2 == 0:
                    t1 = service_line
                    b1 = 1.00
                    l1 = court_l
                    r1 = 0
                else:
                    t1 = service_line
                    b1 = 1.00
                    l1 = 0
                    r1 = court_r

                if my < field_bottom:
                    handle_slider_input((mxs, mys))
                elif b1 < my < t1 and l1 < mx < r1:
                    """
                    プレーヤー1のターン
                    プレーヤー1はy>0に打つ
                    プレーヤー1はy<0に移動する
                    """
                    ball_landing_pos = (mx, my)
                elif field_bottom < my < -1.00:
                    p1_pos_target = [mx, my]

            elif turn == 2:
                # プレーヤー2はサービスを打つ場所と移動先を指定する。
                if (p1_point + p2_point) % 2 == 0:
                    t2 = -1.00
                    b2 = service_line
                    l2 = 0
                    r2 = court_r
                else:
                    t2 = -1.00
                    b2 = service_line
                    l2 = court_l
                    r2 = 0

                if my < field_bottom:
                    handle_slider_input((mxs, mys))
                elif b2 < my < t2 and l2 < mx < r2:
                    ball_landing_pos = (mx, my)  # ボールの着地点
                elif 1.00 < my < field_top:
                    p2_pos_target = [mx, my]

            if turn == 12:
                print("shot", shot)

                t1 = court_top
                l1 = court_l
                r1 = court_r
                b1 = 1.00

                if my < field_bottom:
                    handle_slider_input((mxs, mys))
                elif b1 < my < t1 and l1 < mx < r1:
                    """
                    プレーヤー1のターン
                    プレーヤー1はy>0に打つ
                    プレーヤー1はy<0に移動する
                    """
                    ball_landing_pos = (mx, my)
                elif field_bottom < my < -1.00:
                    p1_pos_target = [mx, my]

            elif turn == 14:
                b2 = court_bottom
                l2 = court_l
                r2 = court_r
                t2 = -1.00
                if my < field_bottom:
                    handle_slider_input((mxs, mys))
                elif b2 < my < t2 and l2 < mx < r2:
                    ball_landing_pos = (mx, my)  # ボールの着地点
                elif 1.00 < my < field_top:
                    p2_pos_target = [mx, my]

            elif turn == 13 and 1.00 < my < field_top:
                # プレーヤー2のターン　取りに行く
                n = 0
                for x, y, z, t in ballhit:
                    if (
                        math.hypot(x - p2_pos[0], y - p2_pos[1])
                        < config.PLAYER_VMAX * t
                    ):
                        n = n + 1
                        if math.hypot(mx - x, my - y) < 0.5:
                            p2_pos_target = [x, y]
                            ball_pos_target = [x, y, z, t]
                            break
                if n == 0:
                    turn = 20
                    message = "プレーヤー1 Point"
                    p1_point += 1
                    if p1_point >= 4:
                        p1_point = 0
                        p2_point = 0
                        p1_games += 1
                        message = "プレーヤー1 Get Game"
                    if p1_games >= 4:
                        turn = 21
                        message = "プレーヤー1 Win Game End"

            elif turn == 11 and field_bottom < my < -1.00:
                n = 0
                for x, y, z, t in ballhit:
                    if (
                        math.hypot(x - p1_pos[0], y - p1_pos[1])
                        < config.PLAYER_VMAX * t
                    ):
                        n = n + 1
                        if math.hypot(mx - x, my - y) < 0.5:
                            p1_pos_target = [x, y]
                            ball_pos_target = [x, y, z, t]
                            break
                if n == 0:
                    turn = 20
                    message = "プレーヤー2 Point"
                    p2_point += 1

                    if p2_point >= 4:
                        p1_point = 0
                        p2_point = 0
                        p2_games += 1
                        message = "プレーヤー2 Game"
                    if p2_games >= 4:
                        turn = 21
                        message = "プレーヤー2 Win Game End"

            message2 = "mx=" + f"{mx:.2f}" + "my=" + f"{my:.2f}"

    # ボール更新と
    if ball_flying:
        t = t + 0.02
        ball_pos[0] += ball_vx * 0.02
        ball_pos[1] += ball_vy * 0.02
        ball_pos[2] += ball_vz * 0.02
        ball_vz -= g * 0.02

        if turn in (13, 11):
            if t > ball_pos_target[3]:
                t = 0
                ball_flying = False
        if not ball_flying:
            if turn == 13:
                turn = 14
                ball_landing_pos = None
                ball_landing_pos2 = None
                p1_pos = p1_pos_target[:]
                p2_pos = p2_pos_target[:]
                ball_pos = ball_pos_target[0:3]
                current_player = p2_pos[:]
                difensive_player = p1_pos[:]
                current_ball = ball_pos[:]
                shot += 1
            elif turn == 11:
                # player1が取る位置を決めた後。
                turn = 12
                ball_landing_pos = None
                ball_landing_pos2 = None
                p1_pos = p1_pos_target[:]
                p2_pos = p2_pos_target[:]
                ball_pos = ball_pos_target[0:3]  # 0 1 2
                current_player = p1_pos[:]
                difensive_player = p2_pos[:]
                current_ball = ball_pos[:]
                shot += 1
    else:
        t = 0

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
    draw_landing_marker(p1_pos_target, RED, cross=True)

    # プレーヤー2描画
    pygame.draw.circle(
        screen,
        BLACK,
        (int(center_x + p2_pos[0] * scale), int(center_y - p2_pos[1] * scale)),
        player_radius,
    )
    draw_landing_marker(p2_pos_target, BLACK, cross=True)

    if ball_flying:
        # 飛んでいる時にボールを描画
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(center_x + ball_pos[0] * scale), int(center_y - ball_pos[1] * scale)),
            BALL_RADIUS * scale,
        )

    if ball_landing_pos:
        dx = ball_landing_pos[0] - current_ball[0]
        dy = ball_landing_pos[1] - current_ball[1]

        t_flight = (
            z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * current_ball[2])
        ) / g

        ball_vx = dx / t_flight
        ball_vy = dy / t_flight
        ball_vz = z_slider_val

        # y=0の時間
        t0 = -current_ball[1] / ball_vy
        a = 0.5 * g
        z0 = current_ball[2] + ball_vz * t0 - a * t0 * t0
        x0 = current_ball[0] + ball_vx * t0
        ballhit = []
        if check_net(x0, z0):
            v_land = ball_vz - g * t_flight  # 着地時の速度（負の値）
            v_rebound = -v_land * 0.8  # 跳ね返り初速（正の値）

            t_bounce = 2 * v_rebound / g  # 上下で対称な時間（頂点までと落下）
            t_flight2 = t_flight + t_bounce  # 2回目の着地時刻

            ball_landing_pos2 = (
                current_ball[0] + ball_vx * t_flight2,
                current_ball[1] + ball_vy * t_flight2,
            )

            for i in range(3, 20):
                z = i * 0.1

                b = -ball_vz
                c = z - current_ball[2]
                discriminant = b**2 - 4 * a * c
                if discriminant > 0 and shot >= 1:
                    sqrt_d = math.sqrt(discriminant)
                    t1 = (-b - sqrt_d) / (2 * a)  # 上昇時
                    if t1 > t0:
                        x1 = current_ball[0] + ball_vx * t1
                        y1 = current_ball[1] + ball_vy * t1
                        ballhit.append((x1, y1, z, t1))
                    t2 = (-b + sqrt_d) / (2 * a)  # 下降時
                    if t2 > t0:
                        x2 = current_ball[0] + ball_vx * t2
                        y2 = current_ball[1] + ball_vy * t2
                        ballhit.append((x2, y2, z, t2))
                b = -v_rebound
                c = z  # 高さ0からの2バウンド目
                discriminant = b**2 - 4 * a * c
                if discriminant > 0:
                    sqrt_d = math.sqrt(discriminant)
                    t1 = (-b - sqrt_d) / (2 * a) + t_flight  # 上昇時
                    x1 = current_ball[0] + ball_vx * t1
                    y1 = current_ball[1] + ball_vy * t1
                    ballhit.append((x1, y1, z, t1))
                    t2 = (-b + sqrt_d) / (2 * a) + t_flight  # 下降時
                    x2 = current_ball[0] + ball_vx * t2
                    y2 = current_ball[1] + ball_vy * t2
                    ballhit.append((x2, y2, z, t2))
            # 4つ目の値（index 3）でソート
            ballhit = sorted(ballhit, key=lambda x: x[3])

            draw_landing_marker(ball_landing_pos, RED)
            draw_landing_marker(ball_landing_pos2, RED)
            # ボールの軌跡を表示する
            draw_trajectory(current_player, ball_vx, ball_vy, t_flight2)
        else:
            # ボールのlanding_makerはネットの位置
            ball_landing_pos2 = None
            draw_landing_marker((x0, 0), RED)
            # ボールの軌跡を表示する。ネットまで
            draw_trajectory(current_player, ball_vx, ball_vy, t0)

    if turn in (2, 4, 12, 14) and ball_landing_pos:
        # スライダーを表示する。
        draw_slider(slider_x, z_slider_y, z_slider_val, ball_vzmin, ball_vzmax, "Z速度")
        draw_slider(slider_x, h_slider_y, h_slider_val, 0, ball_vmax, "水平速度")

    if turn == 13:
        # キャッチできるポイントを表示
        draw_candidates(ballhit, difensive_player, p2_pos_target)
    if turn == 11:
        draw_candidates(ballhit, difensive_player, p1_pos_target)

    draw_ok_button()  # OKボタンを表示する。

    draw_scoreboard()  # スコアーボードを表示する。

    pygame.display.flip()
    clock.tick(60)
