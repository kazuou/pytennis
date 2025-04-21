import pygame
import math
import sys

# 初期設定
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Throw Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# スケール：24m × 36m を画面にマッピング
scale = WIDTH / 24.0
gravity = 9.8  # m/s^2

# プレイヤー状態
player1_pos = [12.0, 2.0]  # 中央
player2_pos = [12.0, 34.0]

# プレイヤー移動設定
MAX_SPEED = 6.0  # m/s
ACCEL = 3.0  # m/s^2


def draw_field():
    screen.fill((30, 200, 30))
    # テニスコート
    court_color = (255, 255, 255)
    net_y = HEIGHT // 2
    pygame.draw.rect(
        screen, court_color, (WIDTH / 6, net_y - 80, WIDTH * 2 / 3, 160), 2
    )
    pygame.draw.line(screen, court_color, (0, net_y), (WIDTH, net_y), 2)


def simulate_throw(start_pos, v0, angle_deg, azimuth_deg):
    angle = math.radians(angle_deg)
    azimuth = math.radians(azimuth_deg)
    vx = v0 * math.cos(angle) * math.sin(azimuth)
    vy = v0 * math.cos(angle) * math.cos(azimuth)
    vz = v0 * math.sin(angle)
    x, y, z = start_pos[0], start_pos[1], 2.0  # 高さ2m

    dt = 0.05
    path = []
    bounce = False
    while True:
        x += vx * dt
        y += vy * dt
        vz -= gravity * dt
        z += vz * dt
        if z <= 0:
            if bounce:
                break
            else:
                z = -z
                vz = -vz * 0.8
                bounce = True
        if x < 0 or x > 24 or y < 0 or y > 36:
            break
        path.append((x, y, z))
    return path


def draw_ball(pos):
    x, y, _ = pos
    pygame.draw.circle(
        screen, (255, 255, 0), (int(x * scale), int(HEIGHT - y * scale)), 5
    )


def get_throw_input(player_name):
    v0 = float(input(f"{player_name} 投球速度(m/s): "))
    angle = float(input(f"{player_name} 仰角(度): "))
    azimuth = float(input(f"{player_name} 方向(度, y軸が0°): "))
    tx = float(input(f"{player_name} が移動するx座標(0~24): "))
    ty = float(input(f"{player_name} が移動するy座標(0~36): "))
    return v0, angle, azimuth, tx, ty


def find_candidates(ball_path, height):
    candidates = []
    for i in range(1, len(ball_path)):
        z1 = ball_path[i - 1][2]
        z2 = ball_path[i][2]
        if (z1 - height) * (z2 - height) <= 0:
            candidates.append(ball_path[i])
    return candidates


def time_to_reach(start, target):
    dx = start[0] - target[0]
    dy = start[1] - target[1]
    d = math.hypot(dx, dy)
    t_to_max = MAX_SPEED / ACCEL
    d_accel = 0.5 * ACCEL * t_to_max**2
    if d <= 2 * d_accel:
        return math.sqrt(4 * d / ACCEL)
    d_flat = d - 2 * d_accel
    return 2 * t_to_max + d_flat / MAX_SPEED


def move_player_to(player_pos, x, y):
    player_pos[0] = x
    player_pos[1] = y


# ゲームループ（1投ずつ交互）
turn = 1
ball_path = []
ball_index = 0
ball_active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_field()

    if not ball_active:
        if turn == 1:
            v0, angle, azimuth, tx, ty = get_throw_input("プレーヤー1")
            ball_path = simulate_throw(player1_pos, v0, angle, azimuth)
            move_player_to(player1_pos, tx, ty)
            ball_index = 0
            ball_active = True
            turn = 2
        else:
            # プレーヤー2がキャッチ入力
            h = float(input("プレーヤー2 キャッチ高さを入力(0.5 / 1.0 / 1.5 / 2.0): "))
            candidates = find_candidates(ball_path, h)
            if not candidates:
                print("指定高さを通過しませんでした。失点。")
                turn = 1
                continue
            print("候補点:")
            for i, (x, y, z) in enumerate(candidates):
                print(f"{i + 1}: x={x:.2f}, y={y:.2f}, 高さ={z:.2f}")
            choice = int(input("どの点でキャッチする？ 番号で選んでください: ")) - 1
            target = candidates[choice]
            x, y, _ = target
            t_needed = time_to_reach(player2_pos, (x, y))
            t_ball = (choice + 1) * 0.05  # 簡易時間（インデックス × dt）

            if t_needed <= t_ball:
                print("✅ 間に合った！キャッチ成功")
                move_player_to(player2_pos, x, y)
            else:
                print("❌ 間に合わず失点")
            # プレーヤー2が投球
            v0, angle, azimuth, tx, ty = get_throw_input("プレーヤー2")
            ball_path = simulate_throw(player2_pos, v0, angle, azimuth)
            move_player_to(player2_pos, tx, ty)
            ball_index = 0
            ball_active = True
            turn = 1

    # ボール描画と進行
    if ball_active and ball_index < len(ball_path):
        draw_ball(ball_path[ball_index])
        ball_index += 1
    else:
        ball_active = False

    # プレイヤー描画
    pygame.draw.circle(
        screen,
        (0, 0, 255),
        (int(player1_pos[0] * scale), int(HEIGHT - player1_pos[1] * scale)),
        10,
    )
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (int(player2_pos[0] * scale), int(HEIGHT - player2_pos[1] * scale)),
        10,
    )

    pygame.display.flip()
    clock.tick(30)
