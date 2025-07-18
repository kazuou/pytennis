import pygame
import config15 as config
import math


def draw_court(screen, gt, court_rect, scoreBoard_rect, controler_rect):
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

    screen.fill(config.GREEN)
    pygame.draw.rect(screen, config.BLUE, court_rect)
    pygame.draw.rect(screen, config.GRAY2, scoreBoard_rect)
    pygame.draw.rect(screen, config.GRAY2, controler_rect)

    # pygame.draw.line(screen, WHITE, (0, center_y), (field_width, center_y), 2)
    for start, end, width in lines:
        start_screen = (
            start[0] * config.scale + config.field_width // 2,
            start[1] * config.scale + config.center_y,
        )
        end_screen = (
            end[0] * config.scale + config.field_width // 2,
            end[1] * config.scale + config.center_y,
        )
        width_screen = round(width * config.scale)
        pygame.draw.line(screen, config.WHITE, start_screen, end_screen, width_screen)


def draw_slider(screen, x, y, value, min_val, max_val, label):
    """スライダー描画"""
    pygame.draw.rect(
        screen, config.GRAY, (x, y, config.slider_length, config.slider_height)
    )

    # 正規化されたratio (0.0〜1.0)
    ratio = (value - min_val) / (max_val - min_val)
    ratio = max(0.0, min(1.0, ratio))  # 安全のためクリップ

    # ノブのX位置を計算
    knob_x = int(x + ratio * config.slider_length)

    # ノブを描画
    pygame.draw.rect(
        screen, config.RED, (knob_x - 5, y - 5, 10, config.slider_height + 10)
    )
    # font = pygame.font.SysFont(None, 24)
    font = pygame.font.SysFont(config.fontname, 16)

    text = font.render(f"{label}: {value:.1f}", True, config.BLACK)
    screen.blit(text, (x + config.slider_length + 10, y - 5))


def draw_ok_button(screen, ok_button_rect):
    # OKボタン設定
    pygame.draw.rect(screen, config.BLUE, ok_button_rect)
    font = pygame.font.SysFont(config.fontname, 18)
    text = font.render("OK", True, config.WHITE)
    text_rect = text.get_rect(center=ok_button_rect.center)
    screen.blit(text, text_rect)


def draw_landing_marker(screen, pos, COLOR, cross=False):
    # 場所にcross=True 「+」
    if pos:
        xs, ys = int(config.center_x + pos[0] * config.scale), int(
            config.center_y - pos[1] * config.scale
        )
        if cross:
            pygame.draw.line(screen, COLOR, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
            pygame.draw.line(screen, COLOR, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)
        else:
            pygame.draw.line(screen, COLOR, (xs - 5, ys), (xs + 5, ys), 2)
            pygame.draw.line(screen, COLOR, (xs, ys - 5), (xs, ys + 5), 2)


def draw_candidates(screen, candidate_list, ballcatch, ballcatchb, pos_target):
    """ボールを受け取る場所をxで表示"""

    for x, y, z, t in candidate_list:
        xs = config.center_x + x * config.scale
        ys = config.center_y - y * config.scale
        pygame.draw.line(screen, config.GRAY2, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
        pygame.draw.line(screen, config.GRAY2, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)

    for x, y, z, t in ballcatch:
        xs = config.center_x + x * config.scale
        ys = config.center_y - y * config.scale
        pygame.draw.line(screen, config.BLACK, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
        pygame.draw.line(screen, config.BLACK, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)
        if math.hypot(x - pos_target[0], y - pos_target[1]) < 0.1:
            pygame.draw.line(screen, config.RED, (xs - 5, ys - 5), (xs + 5, ys + 5), 2)
            pygame.draw.line(screen, config.RED, (xs - 5, ys + 5), (xs + 5, ys - 5), 2)

    for x, y, z, t in ballcatchb:
        xs = config.center_x + x * config.scale
        ys = config.center_y - y * config.scale
        pygame.draw.line(screen, config.BLACK, (xs - 5, ys), (xs + 5, ys), 2)
        pygame.draw.line(screen, config.BLACK, (xs, ys - 5), (xs, ys + 5), 2)


def draw_trajectory(screen, start_pos, vx, vy, vz, tbound, tend):
    """ボールの軌道を表示"""
    path = []
    t = 0.0
    dt = 0.05
    g = 9.8

    while True:
        if t > tend:
            # z = z0 + vz * t - 0.5 * g * t**2
            # if z < 0:
            break
        if t < tbound:
            z = start_pos[2] + vz * t - 0.5 * g * t**2
        else:
            z = -(vz - g * tbound) * 0.8 * (t - tbound) - 0.5 * g * (t - tbound) ** 2
        x = config.center_x + (start_pos[0] + vx * t + z * 1.0) * config.scale
        y = config.center_y - (start_pos[1] + vy * t + z * 1.0) * config.scale
        path.append((int(x), int(y)))
        t += dt
    if len(path) >= 2:
        pygame.draw.lines(screen, config.YELLOW, False, path, 2)
        # print("len(path)=", len(path), path)


def format_point(p):
    return ["0", "15", "30", "40", "G"][min(p, 4)]


def draw_scoreboard(screen, message20, message2, gs):
    message = ""
    font = pygame.font.SysFont("Arial", 24)

    score_text = (
        f"P1: {format_point(gs.p1_point)} ({gs.p1_games})  -  "
        f"P2: {format_point(gs.p2_point)} ({gs.p2_games})"
    )

    score_surface = font.render(score_text, True, config.BLUE)
    screen.blit(
        score_surface, (config.field_width // 2 - score_surface.get_width() // 2, 10)
    )
    msg_font = pygame.font.SysFont(config.fontname, 18)

    if gs.turn == 0:
        message = "P1 P2 位置についてださい"
    elif gs.turn == 2:
        message = "P2 サーブを打ってください"
    elif gs.turn == 3:
        message = "P1 取りに行ってください"
    elif gs.turn == 4:
        message = "P1 サーブを打ってください"
    elif gs.turn == 5:
        message = "P2 取りに行ってください"

    elif gs.turn == 11:  # <==4
        message = "P1 取りに行ってください"
    elif gs.turn == 12:  # <==1
        message = "P1 打ってください"
    elif gs.turn == 13:  # <==2
        message = "P2 取りに行ってください"
    elif gs.turn == 14:  # <==3
        message = "P2 打ってください"
    elif gs.turn == 20:  # <==5
        message = message20
    elif gs.turn == 21:  # <==5
        if gs.p1_games >= 4:
            message = "P1 Win Game End"
        else:
            message = "P2 Win Game End"
        pass
    else:
        message = ""

    msg_surface = msg_font.render(message, True, config.BLACK)
    screen.blit(
        msg_surface, (config.field_width // 2 - msg_surface.get_width() // 2, 45)
    )
    msg_surface = msg_font.render(message2, True, config.BLACK)
    screen.blit(
        msg_surface, (config.field_width // 2 - msg_surface.get_width() // 2, 65)
    )
