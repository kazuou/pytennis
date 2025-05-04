import pygame
import sys
import math


def rgb(r, g, b):
    """0〜255の値を受け取り、pygameなどで使えるRGBタプルを返す"""
    return (r, g, b)


# 初期化
pygame.init()

# スケーリング倍率（1m = 20px）
scale = 20
field_width = int(20.97 * scale)
field_height = int(33.77 * scale)

# 画面設定
screen = pygame.display.set_mode(
    (field_width, field_height + 100)
)  # スライダー用に高さ追加
pygame.display.set_caption("テニスボードゲーム")
clock = pygame.time.Clock()

# 色定義
GREEN = rgb(0, 128, 0)
BLUE = rgb(0, 102, 204)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# プレイヤー設定
player_radius = 10
p1_pos = [field_width // 2, int(field_height * 0.25)]
p2_pos = [field_width // 2, int(field_height * 0.75)]

# コート描画用
center_x = field_width // 2
center_y = field_height // 2
court_width = int(10.97 * scale)
court_height = int(23.77 * scale)
court_rect = pygame.Rect(
    center_x - court_width // 2, center_y - court_height // 2, court_width, court_height
)


def draw_court():
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLUE, court_rect)
    pygame.draw.line(screen, WHITE, (0, center_y), (field_width, center_y), 2)


# ボール設定
ball_radius = 5
ball_pos = [p1_pos[0], p1_pos[1], 1.0]  # z=1m からスタート
ball_vx = 0
ball_vy = 0
ball_vz = 0
g = 9.8

# 状態管理
turn = 1  # 1: P1打つ → 2: P2移動 → 3: P2打つ → 4: P1移動
ball_flying = False
ball_landing_pos = None

# スライダー設定
slider_length = 200
slider_height = 10
slider_x = 50
z_slider_y = field_height + 20
h_slider_y = field_height + 60

z_slider_val = 10
h_slider_val = 20


def draw_slider(x, y, value, max_val, label):
    pygame.draw.rect(screen, GRAY, (x, y, slider_length, slider_height))
    knob_x = int(x + (value / max_val) * slider_length)
    pygame.draw.rect(screen, RED, (knob_x - 5, y - 5, 10, slider_height + 10))
    # font = pygame.font.SysFont(None, 24)
    font = pygame.font.SysFont("ヒラキノ角コシックw0", 16)
    text = font.render(f"{label}: {value:.1f}", True, BLACK)
    screen.blit(text, (x + slider_length + 10, y - 5))


def handle_slider_input(mouse_pos):
    global z_slider_val, h_slider_val
    mx, my = mouse_pos
    if z_slider_y <= my <= z_slider_y + slider_height + 10:
        ratio = (mx - slider_x) / slider_length
        z_slider_val = max(1, min(20, ratio * 20))
        h_slider_val = max(
            1,
            math.hypot(
                ball_landing_pos[0] - current_player[0],
                ball_landing_pos[1] - current_player[1],
            )
            / (z_slider_val + math.sqrt(z_slider_val**2 + 2 * g * 1.0) / g),
        )
    elif h_slider_y <= my <= h_slider_y + slider_height + 10:
        ratio = (mx - slider_x) / slider_length
        h_slider_val = max(1, min(40, ratio * 40))
        z_slider_val = max(
            1,
            (
                math.hypot(
                    ball_landing_pos[0] - current_player[0],
                    ball_landing_pos[1] - current_player[1],
                )
                / h_slider_val
                - math.sqrt(1.0)
            )
            * g
            / 2,
        )


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
            if turn == 1 and my < center_y:
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
                turn = 2

            elif turn == 3 and my > center_y:
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
                turn = 4

            elif turn == 2 and my > center_y:
                p2_pos = [mx, my]
                turn = 3

            elif turn == 4 and my < center_y:
                p1_pos = [mx, my]
                turn = 1

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

    # 描画
    draw_court()
    pygame.draw.circle(screen, RED, (int(p1_pos[0]), int(p1_pos[1])), player_radius)
    pygame.draw.circle(screen, RED, (int(p2_pos[0]), int(p2_pos[1])), player_radius)

    if ball_flying:
        pygame.draw.circle(
            screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), ball_radius
        )
    elif ball_landing_pos:
        pygame.draw.circle(
            screen,
            WHITE,
            (int(ball_landing_pos[0]), int(ball_landing_pos[1])),
            ball_radius,
        )

    if turn in (1, 3):
        draw_slider(slider_x, z_slider_y, z_slider_val, 20, "Z速度")
        draw_slider(slider_x, h_slider_y, h_slider_val, 40, "水平速度")

    pygame.display.flip()
    clock.tick(60)
