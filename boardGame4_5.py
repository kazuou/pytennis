import pygame
import sys
import math


def rgb(r, g, b):
    return (r, g, b)


# 初期化
pygame.init()

# スケーリング倍率
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
p1_pos = [0, -1190]
p2_pos = [0, 1190]

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

# field_width = int(2097 * scale)
# field_height = int(3379 * scale)
# controler_height = 100


def draw_court():
    lines = (
        ((-548.5, 1188.5), (548.5, 1188.5), 10),  # ベースライン
        ((-411.5, 640), (411.5, 640), 5),  # サービスライン
        ((0, 1188.5), (0, 1178.5), 5),  # センターマーク
        ((-548.5, 1188.5), (-548.5, -1188.5), 5),  # サイドライン左
        ((-411.5, 1188.5), (-411.5, -1188.5), 5),  # シングルスライン左
        ((0, 640), (0, -640), 5),  # センターライン
        ((411.5, 1188.5), (411.5, -1188.5), 5),  # シングルスライン右
        ((548.5, 1188.5), (548.5, -1188.5), 5),  # サイドライン右
        ((0, -1188.5), (0, -1178.5), 5),  # センターマーク
        ((-411.5, -640), (411.5, -640), 5),  # シングルスライン右
        ((-5029, 0), (5029, 0), 10),  # ネットS
        ((-6399, 0), (6399, 0), 10),  # ネットD
        ((-548.5, -1188.5), (548.5, -1188.5), 10),  # ベースライン下
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

# 状態管理
turn = 1
ball_flying = False
ball_landing_pos = None
current_player = p1_pos

# スライダー設定
slider_length = 150
slider_height = 10
slider_x = 50
z_slider_y = controler_y + 20
h_slider_y = controler_y + 60

z_slider_val = 10
h_slider_val = 20

ok_button_x = slider_x + slider_length + 150
ok_button_y = controler_y + 20

# draw_slider(slider_x, z_slider_y, z_slider_val, 20, "Z速度")
# draw_slider(slider_x, h_slider_y, h_slider_val, 40, "水平速度")


def draw_slider(x, y, value, max_val, label):
    """スライダー描画"""
    pygame.draw.rect(screen, GRAY, (x, y, slider_length, slider_height))
    knob_x = int(x + (value / max_val) * slider_length)
    pygame.draw.rect(screen, RED, (knob_x - 5, y - 5, 10, slider_height + 10))
    # font = pygame.font.SysFont(None, 24)
    font = pygame.font.SysFont("ヒラキノ角コシックw0", 16)

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
    mx, my = mouse_pos
    if not ball_landing_pos:
        return
    dx = ball_landing_pos[0] - current_player[0]
    dy = ball_landing_pos[1] - current_player[1]
    if z_slider_y <= my <= z_slider_y + slider_height + 10:
        ratio = (mx - slider_x) / slider_length
        z_slider_val = max(1, min(20, ratio * 20))
        t = (z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * 1.0)) / g
        h_slider_val = math.hypot(dx, dy) / t
    elif h_slider_y <= my <= h_slider_y + slider_height + 10:
        ratio = (mx - slider_x) / slider_length
        h_slider_val = max(1, min(40, ratio * 40))
        t = math.hypot(dx, dy) / h_slider_val
        z_slider_val = (t * g - math.sqrt(t**2 * g**2 - 4 * g * 1.0)) / 2


def draw_landing_marker(pos):
    if pos:
        x, y = int(pos[0]), int(pos[1])
        pygame.draw.line(screen, WHITE, (x - 5, y), (x + 5, y), 1)
        pygame.draw.line(screen, WHITE, (x, y - 5), (x, y + 5), 1)


def draw_trajectory(start_pos, vx, vy, vz, z0=1.0, steps=50):
    path = []
    t = 0.0
    dt = 0.05
    while True:
        z = z0 + vz * t - 0.5 * g * t**2
        if z < 0:
            break
        x = start_pos[0] + vx * t
        y = start_pos[1] + vy * t
        path.append((int(x), int(y)))
        t += dt
    if len(path) >= 2:
        pygame.draw.lines(screen, YELLOW, False, path, 2)


# メインループ
while True:
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
            mx, my = pygame.mouse.get_pos()

            # OKボタンクリックでターンを進める（打ち終わり時にのみ）
            if ok_button_rect.collidepoint(mx, my):
                if turn == 4:
                    turn = 1
                else:
                    turn += 1

            if turn == 1:
                if my > center_y:
                    """
                    プレーヤー1のターン
                    プレーヤー1はy>0に打つ
                    プレーヤー1はy<0に移動する
                    """
                    ball_landing_pos = (mx, my)
                    current_player = p1_pos
                    handle_slider_input((mx, my))
                    dx = mx - p1_pos[0]
                    dy = my - p1_pos[1]
                    t_flight = (
                        z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * ball_pos[2])
                    ) / g
                    ball_vx = dx / t_flight
                    ball_vy = dy / t_flight
                    ball_vz = z_slider_val
                    ball_flying = True
                else:
                    p1_pos_target = [mx, my]

            elif turn == 3:
                if my < center_y:
                    ball_landing_pos = (mx, my)
                    current_player = p2_pos
                    handle_slider_input((mx, my))
                    dx = mx - p2_pos[0]
                    dy = my - p2_pos[1]
                    t_flight = (
                        z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * ball_pos[2])
                    ) / g
                    ball_vx = dx / t_flight
                    ball_vy = dy / t_flight
                    ball_vz = z_slider_val
                    ball_flying = True
                else:
                    p2_pos_target = [mx, my]

            elif turn == 2 and my > center_y:
                """
                    プレーヤー2のターン
                    プレーヤー1はy>0に打った
                    """
                p2_pos_target = [mx, my]

            elif turn == 4 and my < center_y:
                p1_pos_target = [mx, my]

            elif turn in (1, 3):
                handle_slider_input((mx, my))

    # ボール更新
    if ball_flying:
        ball_pos[0] += ball_vx
        ball_pos[1] += ball_vy
        ball_pos[2] += ball_vz
        ball_vz -= g * 0.1
        if ball_pos[2] <= 0:
            ball_pos[2] = 0
            ball_flying = False

    # 描画処理
    draw_court()

    pygame.draw.circle(
        screen,
        RED,
        (int(p1_pos[0] * scale + center_x), int(p1_pos[1]) * scale + center_y),
        player_radius,
    )
    pygame.draw.circle(
        screen,
        BLACK,
        (int(p2_pos[0] * scale + center_x), int(p2_pos[1]) * scale + center_y),
        player_radius,
    )

    if ball_flying:
        pygame.draw.circle(
            screen, YELLOW, (int(ball_pos[0]), int(ball_pos[1])), ball_radius
        )

    if ball_landing_pos:
        draw_landing_marker(ball_landing_pos)

    if turn in (1, 3) and ball_landing_pos:
        dx = ball_landing_pos[0] - current_player[0]
        dy = ball_landing_pos[1] - current_player[1]
        t_flight = (z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * 1.0)) / g
        vx = dx / t_flight
        vy = dy / t_flight
        vz = z_slider_val
        draw_trajectory(current_player, vx, vy, vz)

    if turn in (1, 3):
        draw_slider(slider_x, z_slider_y, z_slider_val, 20, "Z速度")
        draw_slider(slider_x, h_slider_y, h_slider_val, 40, "水平速度")

    draw_ok_button()

    pygame.display.flip()
    clock.tick(60)
