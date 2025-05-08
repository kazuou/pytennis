import pygame
import sys
import math

pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("テニスボードゲーム")

clock = pygame.time.Clock()

# 色
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# プレイヤー位置・移動パラメータ
player_pos = [200, 500]
player_target = player_pos[:]
player_vel = [0, 0]
a = 0.2
maxspeed = 5

# ボールの状態
ball_pos = [400, 300]
ball_vel = [0, 0]
gravity = 0.3
bounce_coeff = 0.8
ball_active = False

font = pygame.font.SysFont(None, 32)

def draw():
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), 10)
    pygame.draw.circle(screen, BLUE, (int(player_pos[0]), int(player_pos[1])), 15)

    text = font.render("クリックで目的地、右クリックで打球 (速度+角度)", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

def update_player():
    dx = player_target[0] - player_pos[0]
    dy = player_target[1] - player_pos[1]

    dist = math.hypot(dx, dy)
    if dist < 1:
        player_vel[0] = 0
        player_vel[1] = 0
        return

    # 単位ベクトル方向に加速
    dir_x = dx / dist
    dir_y = dy / dist

    # 加速
    player_vel[0] += dir_x * a
    player_vel[1] += dir_y * a

    # 最大速度制限
    speed = math.hypot(player_vel[0], player_vel[1])
    if speed > maxspeed:
        scale = maxspeed / speed
        player_vel[0] *= scale
        player_vel[1] *= scale

    # 位置更新
    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]

def update_ball():
    global ball_vel, ball_active

    if not ball_active:
        return

    # 重力追加
    ball_vel[1] += gravity

    # 位置更新
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # バウンド（床は y = HEIGHT）
    if ball_pos[1] >= HEIGHT - 10:
        ball_pos[1] = HEIGHT - 10
        ball_vel[1] = -ball_vel[1] * bounce_coeff

        # 弱くなったら止める
        if abs(ball_vel[1]) < 1:
            ball_vel = [0, 0]
            ball_active = False

def handle_input(event):
    global player_target, ball_vel, ball_active

    if event.button == 1:  # 左クリック → 移動先
        player_target = list(event.pos)

    elif event.button == 3:  # 右クリック → ボールを打つ
        target_x, target_y = event.pos
        dx = target_x - player_pos[0]
        dy = target_y - player_pos[1]

        angle = math.atan2(-dy, dx)  # 角度（上向きがマイナス）
        speed = 10  # 仮定：固定速度
        ball_vel = [math.cos(angle) * speed, -math.sin(angle) * speed]
        ball_pos[0], ball_pos[1] = player_pos[0], player_pos[1]
        ball_active = True

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_input(event)

    update_player()
    update_ball()
    draw()
    clock.tick(60)
