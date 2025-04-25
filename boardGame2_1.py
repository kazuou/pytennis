import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Board Game")
clock = pygame.time.Clock()

# �F��`
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# �������
angle = 45
speed = 15
target_pos = None
move_pos = None
show_trajectory = False

font = pygame.font.SysFont(None, 24)

def draw_court():
    screen.fill(GREEN)
    pygame.draw.line(screen, WHITE, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2)
    # �l�b�g������
    pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, HEIGHT//2 - 30, 10, 60), 1)

def draw_text(text, pos):
    img = font.render(text, True, WHITE)
    screen.blit(img, pos)

def calculate_trajectory(start, target, speed, angle_deg):
    # �V���v���ȕ������O����`���i�d�͂Ƌp�̂݁j
    g = 0.5
    angle_rad = math.radians(angle_deg)
    vx = (target[0] - start[0]) / 20  # ���̑��x
    vy = -speed * math.sin(angle_rad)
    points = []
    x, y = start
    for t in range(40):
        x += vx
        vy += g
        y += vy
        points.append((int(x), int(y)))
    return points

running = True
while running:
    screen.fill((0, 0, 0))
    draw_court()

    draw_text(f"Angle: {angle}��", (10, 10))
    draw_text(f"Speed: {speed}", (10, 30))

    if target_pos:
        pygame.draw.circle(screen, RED, target_pos, 5)
        draw_text("Target", (target_pos[0]+5, target_pos[1]))

    if move_pos:
        pygame.draw.circle(screen, BLUE, move_pos, 5)
        draw_text("MoveTo", (move_pos[0]+5, move_pos[1]))

    if show_trajectory and target_pos:
        trajectory = calculate_trajectory((WIDTH//2, HEIGHT - 50), target_pos, speed, angle)
        for point in trajectory:
            pygame.draw.circle(screen, WHITE, point, 2)

    # OK�{�^��
    ok_rect = pygame.Rect(WIDTH - 100, HEIGHT - 40, 80, 30)
    pygame.draw.rect(screen, (100, 200, 100), ok_rect)
    draw_text("OK", (WIDTH - 75, HEIGHT - 35))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my < HEIGHT // 2:
                target_pos = (mx, my)
                show_trajectory = True
            elif my >= HEIGHT // 2 and not move_pos:
                move_pos = (mx, my)
            elif ok_rect.collidepoint(event.pos):
                if target_pos and move_pos:
                    print("���肳�ꂽ����:")
                    print(f"  �� �ł���: {target_pos}")
                    print(f"  �� �p: {angle}")
                    print(f"  �� �X�s�[�h: {speed}")
                    print(f"  �� �ړ���: {move_pos}")
                    # ��ԃ��Z�b�g�܂��͎��̃t�F�[�Y��
                    target_pos = None
                    move_pos = None
                    show_trajectory = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                angle = min(85, angle + 5)
            elif event.key == pygame.K_DOWN:
                angle = max(5, angle - 5)
            elif event.key == pygame.K_RIGHT:
                speed += 1
            elif event.key == pygame.K_LEFT:
                speed = max(1, speed - 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
