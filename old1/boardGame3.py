import pygame
import sys

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

# プレイヤー位置
player1_pos = [200, 500]
player2_pos = [600, 100]
ball_pos = [400, 300]

# 状態管理
turn_state = "P1_HIT"  # P1_HIT → P2_MOVE → P2_HIT → P1_MOVE

font = pygame.font.SysFont(None, 36)

def draw():
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, ball_pos, 10)
    pygame.draw.circle(screen, BLUE, player1_pos, 15)
    pygame.draw.circle(screen, GREEN, player2_pos, 15)

    msg = f"ターン: {turn_state}"
    text = font.render(msg, True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.flip()

def handle_input(pos):
    global turn_state, ball_pos, player1_pos, player2_pos

    if turn_state == "P1_HIT":
        ball_pos = list(pos)
        print("P1が打ったボール位置:", pos)
        turn_state = "P2_MOVE"

    elif turn_state == "P2_MOVE":
        player2_pos = list(pos)
        print("P2が移動した位置:", pos)
        turn_state = "P2_HIT"

    elif turn_state == "P2_HIT":
        ball_pos = list(pos)
        print("P2が打ったボール位置:", pos)
        turn_state = "P1_MOVE"

    elif turn_state == "P1_MOVE":
        player1_pos = list(pos)
        print("P1が移動した位置:", pos)
        turn_state = "P1_HIT"

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_input(event.pos)

    draw()
    clock.tick(60)

