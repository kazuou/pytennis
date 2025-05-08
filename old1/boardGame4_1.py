# まず落下点を指定します。
# Z方向のスピードを入力する。===>自動的にvxとvyが決まる。
#
# y = 0で1m　以上かを判定する。
# 最大到達点が5m以下かを判定する。
#
# 0.5m,1m,1.5m,2mの高さに到達するx,y(y>0)点を列挙する。
#
import pygame
import sys
import math

# 初期化
pygame.init()

# スケーリング倍率（1m = 20px）
scale = 20
field_width = int(20.97 * scale)
field_height = int(33.77 * scale)

# 画面設定
screen = pygame.display.set_mode((field_width, field_height))
pygame.display.set_caption("テニスボードゲーム")
clock = pygame.time.Clock()

# 色定義
GREEN = (0, 128, 0)
BLUE = (0, 102, 204)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

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
input_target = False
ball_flying = False
ball_landing_pos = None

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if turn == 1 and my < center_y:
                # P1 打つターゲット指定（P2側）
                dx = mx - p1_pos[0]
                dy = my - p1_pos[1]
                target_dist = math.hypot(dx, dy)
                ball_vz = 10  # z方向初速仮
                t_flight = (ball_vz + math.sqrt(ball_vz**2 + 2 * g * ball_pos[2])) / g
                ball_vx = dx / t_flight
                ball_vy = dy / t_flight
                ball_flying = True
                ball_landing_pos = (mx, my)
                turn = 2

            elif turn == 3 and my > center_y:
                # P2 打つターゲット指定（P1側）
                dx = mx - p2_pos[0]
                dy = my - p2_pos[1]
                target_dist = math.hypot(dx, dy)
                ball_vz = 10
                t_flight = (ball_vz + math.sqrt(ball_vz**2 + 2 * g * ball_pos[2])) / g
                ball_vx = dx / t_flight
                ball_vy = dy / t_flight
                ball_flying = True
                ball_landing_pos = (mx, my)
                turn = 4

            elif turn == 2 and my > center_y:
                p2_pos = [mx, my]
                turn = 3

            elif turn == 4 and my < center_y:
                p1_pos = [mx, my]
                turn = 1

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

    pygame.display.flip()
    clock.tick(60)
