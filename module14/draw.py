import pygame

# 初期化
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
print("screen size=", screen_width, screen_height)

# スケーリング倍率
scale = 20
field_width = int(20.97 * scale)
field_height = int(33.79 * scale)

# 画面設定
screen = pygame.display.set_mode((field_width, field_height + 150))
pygame.display.set_caption("テニスボードゲーム")
clock = pygame.time.Clock()


def rgb(r, g, b):
    return (r, g, b)


# 色定義
GREEN = rgb(0, 128, 0)
BLUE = rgb(0, 102, 204)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = rgb(200, 200, 200)
GRAY2 = rgb(150, 150, 150)
YELLOW = (255, 255, 0)


def draw_court():
    lines = (
        ((-5.485, 11.895), (5.485, 11.895), 0.10),  # ベースライン
        ((-4.115, 6.40), (4.115, 6.40), 0.05),  # サービスライン
        ((0, 11.895), (0, 11.785), 0.05),  # センターマーク
        ((-5.485, 11.895), (-5.485, -11.895), 0.05),  # サイドライン左
        ((-4.115, 11.895), (-4.115, -11.895), 0.05),  # シングルスライン左
        ((0, 6.40), (0, -6.40), 0.05),  # センターライン
        ((4.115, 11.895), (4.115, -11.895), 0.05),  # シングルスライン右
        ((5.485, 11.895), (5.485, -11.895), 0.05),  # サイドライン右
        ((0, -11.895), (0, -11.785), 0.05),  # センターマーク
        ((-4.115, -6.40), (4.115, -6.40), 0.05),  # シングルスライン右
        ((-gt.pole, 0), (gt.pole, 0), 0.10),  # ネットS
        # ((-6.399, 0), (6.399, 0), 0.10),  # ネットD
        ((-5.485, -11.895), (5.485, -11.895), 0.10),  # ベースライン下
    )

    screen.fill(GREEN)
    pygame.draw.rect(screen, BLUE, court_rect)
    pygame.draw.rect(screen, GRAY2, scoreBoard_rect)
    pygame.draw.rect(screen, GRAY2, controler_rect)

    # pygame.draw.line(screen, WHITE, (0, center_y), (field_width, center_y), 2)
    for start, end, width in lines:
        start_screen = (
            start[0] * scale + field_width // 2,
            start[1] * scale + center_y,
        )
        end_screen = (
            end[0] * scale + field_width // 2,
            end[1] * scale + center_y,
        )
        width_screen = round(width * scale)
        pygame.draw.line(screen, WHITE, start_screen, end_screen, width_screen)
