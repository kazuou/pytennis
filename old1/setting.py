import pygame
import sys

pygame.init()

# 画面サイズ・基本設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("設定画面（vmaxとモード選択）")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("yugothic", 32)
# --- 色 ---
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# --- 歯車アイコンの領域（右上に 50x50 の四角）---
gear_rect = pygame.Rect(WIDTH - 60, 10, 50, 50)


# 状態管理
show_settings = False
vmax_str = "10"  # テキスト入力
active_input = False
mode = "シングルス"  # シングルス or ダブルス


def draw_text(text, pos, color=(0, 0, 0)):
    text_surf = FONT.render(text, True, color)
    screen.blit(text_surf, pos)


def draw_radio_button(x, y, label, selected):
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 10, 2)
    if selected:
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 6)
    draw_text(label, (x + 20, y - 10))
    return pygame.Rect(x - 10, y - 10, 20, 20)


def draw_input_box(x, y, w, h, text, active):
    color = (0, 0, 0) if active else (150, 150, 150)
    pygame.draw.rect(screen, color, (x, y, w, h), 2)
    draw_text(text, (x + 5, y + 5))
    return pygame.Rect(x, y, w, h)


# メインループ
while True:
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()
    click = False
    key_input = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pygame.KEYDOWN:
            key_input = event

    if show_settings:
        # 設定画面
        draw_text("設定画面", (WIDTH // 2 - 60, 40))

        # vmax 入力欄
        draw_text("vmax:", (100, 120))
        input_rect = draw_input_box(180, 115, 100, 35, vmax_str, active_input)
        if click and input_rect.collidepoint(mouse_pos):
            active_input = True
        elif click:
            active_input = False

        if active_input and key_input:
            if key_input.key == pygame.K_BACKSPACE:
                vmax_str = vmax_str[:-1]
            elif key_input.unicode.isdigit():
                vmax_str += key_input.unicode

        # ラジオボタン：シングルス / ダブルス
        draw_text("モード:", (100, 200))
        single_rect = draw_radio_button(180, 210, "シングルス", mode == "シングルス")
        double_rect = draw_radio_button(180, 250, "ダブルス", mode == "ダブルス")
        if click:
            if single_rect.collidepoint(mouse_pos):
                mode = "シングルス"
            elif double_rect.collidepoint(mouse_pos):
                mode = "ダブルス"

        # 戻るボタン
        back_rect = pygame.Rect(WIDTH - 150, HEIGHT - 70, 120, 40)
        pygame.draw.rect(screen, (0, 0, 0), back_rect)
        draw_text("戻る", (back_rect.x + 35, back_rect.y + 8), (255, 255, 255))
        if click and back_rect.collidepoint(mouse_pos):
            show_settings = False

    else:

        # 歯車マークの描画（シンプルな〇と線）
        pygame.draw.ellipse(screen, GRAY, gear_rect)
        center = gear_rect.center
        for angle in range(0, 360, 45):
            rad = angle * 3.14 / 180
            dx = 15 * pygame.math.Vector2(1, 0).rotate(angle).x
            dy = 15 * pygame.math.Vector2(1, 0).rotate(angle).y
            pygame.draw.line(screen, BLACK, center, (center[0] + dx, center[1] + dy), 2)

        #        pygame.draw.ellipse(screen, (180, 180, 180), gear_rect)
        #        pygame.draw.circle(screen, (100, 100, 100), gear_rect.center, 5)
        if click and gear_rect.collidepoint(mouse_pos):
            show_settings = True

        # 現在の設定の確認表示
        draw_text(f"vmax: {vmax_str}", (100, 100))
        draw_text(f"モード: {mode}", (100, 140))

    pygame.display.flip()
    clock.tick(60)
