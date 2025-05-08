import pygame
import sys
import math

pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ターン制テニスボードゲーム")

clock = pygame.time.Clock()

# 色
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)

# プレイヤー初期位置
p1_pos = [200, 500]
p2_pos = [600, 100]

# プレイヤー移動用変数
p1_vel = [0, 0]
p2_vel = [0, 0]
p1_target = p1_pos[:]
p2_target = p2_pos[:]

# 移動パラメータ
a = 0.2
maxspeed = 5

# ボール
ball_pos = [400, 300]
ball_vel = [0, 0]
ball_active = False
gravity = 0.3
bounce_coeff = 0.8

# 状態管理
turn_state = "P1_HIT"  # 初期状態

font = pygame.font.SysFont(None, 28)

def draw():
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), 10)
    pygame.draw.circle(screen, BLUE, (int(p1_pos[0]), int(p1_pos[1])), 15)
    pygame.draw.circle(screen, GREEN, (int(p2_pos[0]), int(p2_pos[1])), 15)

    msg = f"ターン: {turn_state}"
    text = font.render(msg, True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.flip()

def update_player(pos, target, vel):
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    dist = math.hypot(dx, dy)

    if dist < 1:
        vel[0] = 0
        vel[1] = 0
        return True  # 到達

    dir_x = dx / dist
    dir_y = dy / dist

    # 加速
    vel[0] += dir_x * a
    vel[1] += dir_y * a

    # 最大速度制限
    speed = math.hypot(vel[0], vel[1])
    if speed > maxspeed:
        scale = maxspeed / speed
        vel[0] *= scale
        vel[1] *= scale

    pos[0] += vel[0]
    pos[1] += vel[1]

    return False

def update_ball():
    global ball_vel, ball_active

    if not ball_active:
        return

    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[1] >= HEIGHT - 10:
        ball_pos[1] = HEIGHT - 10
        ball_vel[1] = -ball_vel[1] * bounce_coeff

        # バウンド後ほぼ停止したら止める
        if abs(ball_vel[1]) < 1:
            ball_vel = [0, 0]
            ball_active = False

def handle_input(pos):
    global turn_state, ball_vel, ball_active, ball_pos
    global p1_target, p2_target

    if turn_state == "P1_HIT":
        # プレイヤー1が打つ：仮の速度と角度で発射
        angle_deg = 45
        speed = 10
        rad = math.radians(angle_deg)
        ball_vel = [math.cos(rad) * speed, -math.sin(rad) * speed]
        ball_pos = p1_pos[:]
        ball_active = True
        turn_state = "P2_MOVE"

    elif turn_state == "P2_MOVE":
        p2_target = list(pos)

    elif turn_state == "P2_HIT":
        angle_deg = 60
        speed = 9
        rad = math.radians(angle_deg)
        ball_vel = [math.cos(rad) * speed * -1, -math.sin(rad) * speed]
        ball_pos = p2_pos[:]
        ball_active = True
        turn_state = "P1_MOVE"

    elif turn_state == "P1_MOVE":
        p1_target = list(pos)

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_input(event.pos)

    update_ball()

    # ターン管理による移動処理
    if turn_state == "P2_MOVE":
        arrived = update_player(p2_pos, p2_target, p2_vel)
        if arrived:
            turn_state = "P2_HIT"

    elif turn_state == "P1_MOVE":
        arrived = update_player(p1_pos, p1_target, p1_vel)
        if arrived:
            turn_state = "P1_HIT"

    draw()
    clock.tick(60)


