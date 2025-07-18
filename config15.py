import socket
import pygame


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
# スケーリング倍率
scale = 20
field_width = int(20.97 * scale)
field_height = int(33.79 * scale)

# 原点定義
center_x = field_width // 2
center_y = field_height // 2 + 100

# コート描画
court_width = int(10.97 * scale)
court_height = int(23.79 * scale)
court_rect = pygame.Rect(
    center_x - court_width // 2,
    center_y - court_height // 2,
    court_width,
    court_height,
)
court_top = 11.895
court_bottom = -11.895
# court_l = -4.115
# court_r = 4.116
service_line = 6.40

scoreBoard_y = 0
scoreBoard_rect = pygame.Rect(0, 0, field_width, 100)
controler_y = field_height + 100
controler_rect = pygame.Rect(0, controler_y, field_width, field_height + 150)
field_bottom = (center_y - field_height - 100) / scale
field_top = (center_y - 100) / scale
field_l = -16.89
field_r = 16.89


# スライダー設定
slider_length = 150
slider_height = 10


MARGIN_NET = 0.1
MARGIN_LINE = 0.5


# プレイヤー設定
player_radius = 10

# if gt == GameType.DOUBLES:
# PLAYER_VMAX = 4
# PLAYER_REACH = 0.8
# else:
PLAYER_VMAX = 5
PLAYER_REACH = 1

# ボール設定
BALL_RADIUS = 0.05

ball_vmax = 30  # 時速100kmは秒速28mです。
BALL_VZMAX = 10  # 秒速9.9m/sで5m打ち上がる
BALL_VZMIN = -3


# 自分のホスト名からIPアドレスを取得
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
print(host_name)
# IPアドレスをドットで分割して、最後の部分を取得
last_octet = ip_address.split(".")[-1]

# if socket.gethostname() == "Cortina.local":
# if host_name == "Cortina.local":
keyword72 = "Cortina"
keywords = {
    "Candace": ("notosansmonocjkjp", 74),
    "Amber": ("msgothic", 83),
    "W10029376A": ("yumincho", 70),
}

if keyword72 in host_name:
    print("in Cortina")
    # filename = "FontPygame72"
    fontname = "ヒラキノ角コシックw5"
elif (keyword := keywords.get(host_name)) is not None:
    fontname = keyword[0]
    last_octet = keyword[1]
else:
    # filename = "FontPygame"
    fontname = "notosansmonocjkjp"

print(f"最後のIPアドレスの数字は: {last_octet}")
print("font=", fontname)
