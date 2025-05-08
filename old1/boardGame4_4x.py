import pygame
import sys
import math

pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Board Game")

# 色定義
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# コートサイズとスケーリング
COURT_WIDTH = 20.97
COURT_HEIGHT = 33.77
SCALE = WIDTH / COURT_WIDTH
COURT_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

# プレーヤー初期位置
p1_pos = [0, -10]
p2_pos = [0, 10]

# プレーヤー移動先
p1_target = p1_pos[:]
p2_target = p2_pos[:]

# ボールのパラメータ
ball_pos = [0, 0, 0]
ball_vel = [0, 0, 0]
ball_in_air = False
bouncing = False

# ターン管理
turn = "p1_aim"  # "p1_aim", "p2_move", "p2_aim", "p1_move"

# 移動物理パラメータ
acc = 0.2
max_speed = 1.0
player_speed = [0, 0]

# スライダー初期値
slider_z = 10
slider_xy = 5

# フォント
# font = pygame.font.SysFont(None, 36)
font = pygame.font.SysFont("ヒラキノ角コシックw0", 16)


# テキスト描画
def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# 座標変換
def to_screen(x, y):
    sx = WIDTH // 2 + int(x * SCALE)
    sy = HEIGHT // 2 - int(y * SCALE)
    return sx, sy


# プレーヤー描画
def draw_players():
    pygame.draw.circle(screen, RED, to_screen(*p1_pos), 10)
    pygame.draw.circle(screen, BLUE, to_screen(*p2_pos), 10)


# ボール描画
def draw_ball():
    if ball_in_air:
        x, y, z = ball_pos
        sx, sy = to_screen(x, y)
        sy -= int(z * SCALE)
        pygame.draw.circle(screen, BLACK, (sx, sy), 6)


# スライダー描画と処理
def draw_slider(x, y, label, value, min_val, max_val):
    pygame.draw.rect(screen, BLACK, (x, y, 200, 10), 2)
    pos = int((value - min_val) / (max_val - min_val) * 200)
    pygame.draw.rect(screen, RED, (x, y, pos, 10))
    draw_text(f"{label}: {value:.1f}", x, y - 30)
    return x, y, 200, 10


# メインループ
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    # コート描画
    pygame.draw.rect(screen, GREEN, COURT_RECT)
    pygame.draw.rect(
        screen,
        BLUE,
        [
            WIDTH // 2 - 5.485 * SCALE,
            HEIGHT // 2 - 11.885 * SCALE,
            10.97 * SCALE,
            23.77 * SCALE,
        ],
    )

    # 情報ボード
    draw_text("セット: 0 ゲーム: 0 ポイント: 0", 700, 20)

    # 打つ指示表示
    if turn in ["p1_aim", "p2_aim"]:
        draw_text("ボールを打ってください", 700, 100)

    # スライダー描画
    if turn in ["p1_aim", "p2_aim"]:
        bar1 = draw_slider(700, 150, "Z速度", slider_z, 5, 20)
        bar2 = draw_slider(700, 200, "XY速度", slider_xy, 3, 15)

    # プレーヤーとボール描画
    draw_players()
    draw_ball()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if turn == "p1_aim":
                if mx < 700:
                    tx = (mx - WIDTH // 2) / SCALE
                    ty = (HEIGHT // 2 - my) / SCALE
                    ball_pos = [*p1_pos, 0]
                    ball_vel = [
                        slider_xy * (tx - p1_pos[0]) / 10,
                        slider_xy * (ty - p1_pos[1]) / 10,
                        slider_z,
                    ]
                    ball_in_air = True
                    turn = "p2_move"
                elif 150 <= my <= 160:
                    slider_z = 5 + 15 * (mx - 700) / 200
                    slider_xy = 3 + 12 * (1 - (slider_z - 5) / 15)  # 相関調整
                elif 200 <= my <= 210:
                    slider_xy = 3 + 12 * (mx - 700) / 200
                    slider_z = 5 + 15 * (1 - (slider_xy - 3) / 12)

            elif turn == "p2_aim":
                if mx < 700:
                    tx = (mx - WIDTH // 2) / SCALE
                    ty = (HEIGHT // 2 - my) / SCALE
                    ball_pos = [*p2_pos, 0]
                    ball_vel = [
                        slider_xy * (tx - p2_pos[0]) / 10,
                        slider_xy * (ty - p2_pos[1]) / 10,
                        slider_z,
                    ]
                    ball_in_air = True
                    turn = "p1_move"
                elif 150 <= my <= 160:
                    slider_z = 5 + 15 * (mx - 700) / 200
                    slider_xy = 3 + 12 * (1 - (slider_z - 5) / 15)
                elif 200 <= my <= 210:
                    slider_xy = 3 + 12 * (mx - 700) / 200
                    slider_z = 5 + 15 * (1 - (slider_xy - 3) / 12)

            elif turn == "p1_move" and my > HEIGHT // 2:
                p1_target = [(mx - WIDTH // 2) / SCALE, (HEIGHT // 2 - my) / SCALE]
                turn = "p2_aim"

            elif turn == "p2_move" and my < HEIGHT // 2:
                p2_target = [(mx - WIDTH // 2) / SCALE, (HEIGHT // 2 - my) / SCALE]
                turn = "p1_aim"

    # プレーヤー移動
    if turn == "p1_move":
        dx = p1_target[0] - p1_pos[0]
        dy = p1_target[1] - p1_pos[1]
        dist = math.hypot(dx, dy)
        if dist > 0.1:
            p1_pos[0] += max_speed * dx / dist
            p1_pos[1] += max_speed * dy / dist

    elif turn == "p2_move":
        dx = p2_target[0] - p2_pos[0]
        dy = p2_target[1] - p2_pos[1]
        dist = math.hypot(dx, dy)
        if dist > 0.1:
            p2_pos[0] += max_speed * dx / dist
            p2_pos[1] += max_speed * dy / dist

    # ボール更新
    if ball_in_air:
        ball_pos[0] += ball_vel[0] * 0.1
        ball_pos[1] += ball_vel[1] * 0.1
        ball_pos[2] += ball_vel[2] * 0.1
        ball_vel[2] -= 9.8 * 0.1

        if ball_pos[2] <= 0 and not bouncing:
            ball_vel[2] *= -0.8
            ball_pos[2] = 0
            bouncing = True
        elif ball_pos[2] <= 0 and bouncing:
            ball_in_air = False
            bouncing = False

    pygame.display.flip()
    clock.tick(60)
