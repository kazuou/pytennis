import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Board Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 24)

# Game States
game_state = "P1_INPUT"  # P1_INPUT -> P1_MOVE -> P2_INPUT -> P2_MOVE


# Ball
def calculate_trajectory(start, target, speed, angle_deg):
    g = 0.5
    angle_rad = math.radians(angle_deg)
    vx = (target[0] - start[0]) / 20
    vy = -speed * math.sin(angle_rad)
    points = []
    x, y = start
    for t in range(40):
        x += vx
        vy += g
        y += vy
        points.append((int(x), int(y)))
    return points


# Player
class Player:
    def __init__(self, start_pos):
        self.pos = list(start_pos)
        self.target = list(start_pos)
        self.speed = 0
        self.max_speed = 5
        self.moving = False

    def update(self):
        if self.moving:
            dx = self.target[0] - self.pos[0]
            dy = self.target[1] - self.pos[1]
            distance = math.hypot(dx, dy)

            if distance < 1:
                self.moving = False
                self.speed = 0
                return

            if distance > 100:
                self.speed = min(self.speed + 0.2, self.max_speed)
            else:
                self.speed = max(self.speed - 0.3, 0.5)

            direction = math.atan2(dy, dx)
            self.pos[0] += math.cos(direction) * self.speed
            self.pos[1] += math.sin(direction) * self.speed

    def draw(self, color):
        pygame.draw.circle(screen, color, (int(self.pos[0]), int(self.pos[1])), 10)


# Setup
p1 = Player([WIDTH // 2, HEIGHT - 50])
p2 = Player([WIDTH // 2, 50])

angle = 45
speed = 15
target_pos = None
move_pos = None
show_trajectory = False
ball_trajectory = []
ball_index = 0
score = {"P1": 0, "P2": 0}

ok_rect = pygame.Rect(WIDTH - 100, HEIGHT - 40, 80, 30)


def draw_court():
    screen.fill(GREEN)
    pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, HEIGHT // 2 - 30, 10, 60), 1)
    draw_text(f"Score: P1 {score['P1']} - P2 {score['P2']}", (WIDTH // 2 - 60, 10))


def draw_text(text, pos):
    img = font.render(text, True, WHITE)
    screen.blit(img, pos)


running = True
while running:
    screen.fill(BLACK)
    draw_court()
    p1.draw(RED)
    p2.draw(BLUE)

    draw_text(f"Angle: {angle}", (10, 10))
    draw_text(f"Speed: {speed}", (10, 30))

    if target_pos:
        pygame.draw.circle(screen, RED, target_pos, 5)
        draw_text("Target", (target_pos[0] + 5, target_pos[1]))

    if move_pos:
        pygame.draw.circle(screen, BLUE, move_pos, 5)
        draw_text("MoveTo", (move_pos[0] + 5, move_pos[1]))

    if show_trajectory and ball_trajectory:
        for point in ball_trajectory:
            pygame.draw.circle(screen, WHITE, point, 2)

    pygame.draw.rect(screen, (100, 200, 100), ok_rect)
    draw_text("OK", (WIDTH - 75, HEIGHT - 35))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if game_state == "P1_INPUT":
                if my < HEIGHT // 2:
                    target_pos = (mx, my)
                elif my >= HEIGHT // 2:
                    move_pos = (mx, my)
                if ok_rect.collidepoint(event.pos) and target_pos and move_pos:
                    ball_trajectory = calculate_trajectory(
                        (p1.pos[0], p1.pos[1]), target_pos, speed, angle
                    )
                    ball_index = 0
                    p1.target = list(move_pos)
                    p1.moving = True
                    show_trajectory = True
                    game_state = "P1_MOVE"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                angle = min(85, angle + 5)
            elif event.key == pygame.K_DOWN:
                angle = max(5, angle - 5)
            elif event.key == pygame.K_RIGHT:
                speed += 1
            elif event.key == pygame.K_LEFT:
                speed = max(1, speed - 1)

    if game_state == "P1_MOVE":
        if ball_index < len(ball_trajectory):
            ball_index += 1
            p1.update()
        else:
            # Simulate P2 movement later (AI or random), assume catch failed
            score["P1"] += 1
            target_pos = None
            move_pos = None
            show_trajectory = False
            game_state = "P1_INPUT"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
