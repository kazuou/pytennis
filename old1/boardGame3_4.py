import pygame
import math

# 初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 色
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
GRAY = (100, 100, 100)

# プレーヤー情報
p1_pos = [200.0, 500.0]
p2_pos = [600.0, 100.0]
p1_vel = [0.0, 0.0]
p2_vel = [0.0, 0.0]
p1_target = p1_pos[:]
p2_target = p2_pos[:]

a = 0.5
maxspeed = 5.0

# ボール情報（x, y, z）と速度
ball_pos = [0.0, 0.0, 0.0]
ball_vel = [0.0, 0.0, 0.0]
gravity = 0.5
bounce = 0.8
ball_active = False

# ゲームのターン状態
turn_state = "P1_HIT"
p1_moving = False
p2_moving = False

def update_player(pos, target, vel):
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    dist = math.hypot(dx, dy)
    if dist < 1:
        vel[0] = 0
        vel[1] = 0
        return True
    dir_x = dx / dist
    dir_y = dy / dist
    vel[0] += dir_x * a
    vel[1] += dir_y * a
    speed = math.hypot(vel[0], vel[1])
    if speed > maxspeed:
        scale = maxspeed / speed
        vel[0] *= scale
        vel[1] *= scale
    pos[0] += vel[0]
    pos[1] += vel[1]
    return False

def hit_ball(from_pos, angle_xy_deg, angle_z_deg, speed):
    rad_xy = math.radians(angle_xy_deg)
    rad_z = math.radians(angle_z_deg)
    vx = math.cos(rad_xy) * speed * math.cos(rad_z)
    vy = math.sin(rad_xy) * speed * math.cos(rad_z)
    vz = speed * math.sin(rad_z)
    ball_pos[0] = from_pos[0]
    ball_pos[1] = from_pos[1]
    ball_pos[2] = 0
    ball_vel[0] = vx
    ball_vel[1] = vy
    ball_vel[2] = vz
    global ball_active
    ball_active = True

def update_ball():
    global ball_active
    if not ball_active:
        return
    for i in range(3):
        ball_pos[i] += ball_vel[i]
    ball_vel[2] -= gravity
    if ball_pos[2] < 0:
        ball_pos[2] = 0
        ball_vel[2] = -ball_vel[2] * bounce
        if abs(ball_vel[2]) < 1:
            ball_active = False

def draw_ball():
    shadow_x = int(ball_pos[0])
    shadow_y = int(ball_pos[1])
    shadow_size = max(2, 10 - int(ball_pos[2] / 5))
    pygame.draw.circle(screen, GRAY, (shadow_x, shadow_y), shadow_size)  # 影
    pygame.draw.circle(screen, RED, (shadow_x, shadow_y - int(ball_pos[2])), 10)  # ボール

def handle_input(pos):
    global turn_state, p1_target, p2_target, p1_moving, p2_moving
    if turn_state == "P1_HIT":
        hit_ball(p1_pos, angle_xy_deg=90, angle_z_deg=45, speed=12)
        turn_state = "P2_MOVE"
    elif turn_state == "P2_MOVE":
        p2_target = list(pos)
        p2_moving = True
    elif turn_state == "P2_HIT":
        hit_ball(p2_pos, angle_xy_deg=270, angle_z_deg=50, speed=11)
        turn_state = "P1_MOVE"
    elif turn_state == "P1_MOVE":
        p1_target = list(pos)
        p1_moving = True

# メインループ
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_input(pygame.mouse.get_pos())

    update_ball()

    if turn_state == "P2_MOVE" and p2_moving:
        if update_player(p2_pos, p2_target, p2_vel):
            p2_moving = False
            turn_state = "P2_HIT"
    elif turn_state == "P1_MOVE" and p1_moving:
        if update_player(p1_pos, p1_target, p1_vel):
            p1_moving = False
            turn_state = "P1_HIT"

    # プレーヤー描画
    pygame.draw.circle(screen, BLUE, (int(p1_pos[0]), int(p1_pos[1])), 15)
    pygame.draw.circle(screen, GREEN, (int(p2_pos[0]), int(p2_pos[1])), 15)

    draw_ball()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
