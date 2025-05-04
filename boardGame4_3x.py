import pygame
import math

# 初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Board Game")
clock = pygame.time.Clock()

# 色定義
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# コートの実寸とスケール変換
COURT_WIDTH, COURT_HEIGHT = 10.97, 23.77
TOTAL_WIDTH, TOTAL_HEIGHT = 20.97, 33.77
SCALE = HEIGHT / TOTAL_HEIGHT  # m -> px

# 中心座標を画面中央に
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2


def world_to_screen(x, y):
    return int(CENTER_X + x * SCALE), int(CENTER_Y - y * SCALE)


class Player:
    def __init__(self, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.radius = 10
        self.max_speed = 6  # m/s
        self.acceleration = 0.5

    def update(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0.1:
            dir_x = dx / dist
            dir_y = dy / dist
            self.vx += self.acceleration * dir_x
            self.vy += self.acceleration * dir_y
            speed = math.hypot(self.vx, self.vy)
            if speed > self.max_speed:
                scale = self.max_speed / speed
                self.vx *= scale
                self.vy *= scale
            self.x += self.vx * 0.1
            self.y += self.vy * 0.1
        else:
            self.vx = 0
            self.vy = 0

    def draw(self):
        px, py = world_to_screen(self.x, self.y)
        pygame.draw.circle(screen, self.color, (px, py), self.radius)


class Ball:
    def __init__(self):
        self.x = 0
        self.y = -10
        self.z = 1
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.gravity = -9.8
        self.bounce_coef = 0.8
        self.active = False

    def serve(self, x1, y1, x2, y2, vz):
        self.x = x1
        self.y = y1
        self.z = 1
        dx = x2 - x1
        dy = y2 - y1
        t = 2 * vz / -self.gravity
        self.vx = dx / t
        self.vy = dy / t
        self.vz = vz
        self.active = True

    def update(self):
        if not self.active:
            return
        dt = 0.1
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt + 0.5 * self.gravity * dt**2
        self.vz += self.gravity * dt
        if self.z < 0:
            self.z = -self.z
            self.vz = -self.vz * self.bounce_coef

    def draw(self):
        if self.active:
            px, py = world_to_screen(self.x, self.y)
            r = max(2, int(5 * (self.z + 0.1)))
            pygame.draw.circle(screen, RED, (px, py), r)


# スライダーの関数定義
def draw_slider(label, x, y, value, min_val, max_val):
    pygame.draw.rect(screen, WHITE, (x, y, 200, 20), 2)
    pos = int((value - min_val) / (max_val - min_val) * 200)
    pygame.draw.rect(screen, RED, (x, y, pos, 20))
    font = pygame.font.SysFont(None, 24)
    txt = font.render(f"{label}: {value:.1f}", True, WHITE)
    screen.blit(txt, (x + 210, y))


def update_sliders_from_vz():
    global slider_vz, slider_vxy
    t = 2 * slider_vz / 9.8
    slider_vxy = distance / t


def update_vz_from_slider_vxy():
    global slider_vz, slider_vxy
    t = distance / slider_vxy
    slider_vz = 0.5 * 9.8 * t


# プレイヤーとボール生成
p1 = Player("P1", 0, -15, WHITE)
p2 = Player("P2", 0, 15, BLUE)
ball = Ball()

# 初期値
turn = 1
slider_vz = 5.0
slider_vxy = 5.0
distance = 1.0  # 仮の距離
selected_slider = None

running = True
while running:
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            wx = (mx - CENTER_X) / SCALE
            wy = (CENTER_Y - my) / SCALE

            if turn == 1 and wy > 0:
                distance = math.hypot(wx - p1.x, wy - p1.y)
                update_sliders_from_vz()
                ball.serve(p1.x, p1.y, wx, wy, slider_vz)
                turn = 2
            elif turn == 3 and wy < 0:
                distance = math.hypot(wx - p2.x, wy - p2.y)
                update_sliders_from_vz()
                ball.serve(p2.x, p2.y, wx, wy, slider_vz)
                turn = 0
            elif turn == 2:
                if wy > 0:
                    p2.target_x = wx
                    p2.target_y = wy
                    turn = 3
            elif turn == 0:
                if wy < 0:
                    p1.target_x = wx
                    p1.target_y = wy
                    turn = 1

        elif event.type == pygame.MOUSEBUTTONUP:
            selected_slider = None

        elif event.type == pygame.MOUSEMOTION:
            if selected_slider:
                mx, _ = pygame.mouse.get_pos()
                new_value = (mx - 100) / 200 * 10
                new_value = max(0.1, min(10.0, new_value))
                if selected_slider == "vz":
                    slider_vz = new_value
                    update_sliders_from_vz()
                elif selected_slider == "vxy":
                    slider_vxy = new_value
                    update_vz_from_slider_vxy()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 100 <= mx <= 300:
                if 500 <= my <= 520:
                    selected_slider = "vz"
                elif 530 <= my <= 550:
                    selected_slider = "vxy"

    # コート描画
    pygame.draw.rect(
        screen,
        BLUE,
        (
            *world_to_screen(-5.485, -11.885)[0:2],
            int(10.97 * SCALE),
            int(23.77 * SCALE),
        ),
    )
    pygame.draw.line(
        screen, WHITE, world_to_screen(-10.485, 0), world_to_screen(10.485, 0), 2
    )

    # オブジェクト更新と描画
    if turn in [2, 0]:
        p1.update()
        p2.update()

    p1.draw()
    p2.draw()
    ball.update()
    ball.draw()

    # スライダー表示
    if turn in [1, 3]:
        draw_slider("vz", 100, 500, slider_vz, 0.1, 10.0)
        draw_slider("vxy", 100, 530, slider_vxy, 0.1, 10.0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
