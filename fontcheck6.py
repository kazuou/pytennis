import pygame
import math
import socket


print(socket.gethostname())
# 自分のホスト名からIPアドレスを取得
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
print(host_name, ip_address)


# IPアドレスをドットで分割して、最後の部分を取得。文字列として取得している
last_octet = ip_address.split(".")[-1]

# if socket.gethostname() == "Cortina.local":
# if host_name == "Cortina.local":
keywords72 = "Coltina"
keywords = {
    "Candace": ("notosansmonocjkjp", 74),
    "Amber": ("msgothic", 83),
    "W10029376A!": ("yumincho", 70)
}

if any(keyword in host_name for keyword in keywords72):
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
filename = "FontPygame" + str(last_octet)

# 初期化
pygame.init()

# フォント一覧取得
fonts = sorted(pygame.font.get_fonts())
num_fonts = len(fonts)

# セルサイズと列・行数
cell_w, cell_h = 600, 20
cols = 1
rows = math.ceil(num_fonts / cols)

# 画面サイズ
screen_width = cols * cell_w
screen_height = (rows + 2) * cell_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pygameフォント一覧（日本語+abc）")

# 背景
screen.fill((255, 255, 255))

# ★ デフォルトフォントでフォント名表示
# default_font = pygame.font.SysFont("arial", 16)
# ★ デフォルトフォントを「ヒラギノ角ゴ W0」に指定
default_font = pygame.font.SysFont(fontname, 16)
text_surface = default_font.render(host_name, True, (0, 0, 0))
screen.blit(text_surface, (5, 2))
# 描画ループ
for i, fontname in enumerate(fonts):
    x = (i % cols) * cell_w
    y = (i // cols) * cell_h + 20

    # フォント名をデフォルトフォントで描画
    name_surface = default_font.render(fontname, True, (0, 0, 255))
    screen.blit(name_surface, (x + 5, y + 2))

    # "日本語 abc" をそのフォントで描画
    try:
        test_font = pygame.font.SysFont(fontname, 20)
        print(fontname)
        text_surface = test_font.render("こんにちは世界 HelloWorld!!", True, (0, 0, 0))
        screen.blit(text_surface, (x + 305, y + 2))
    except:
        # レンダリング失敗時はスキップ
        continue

# 描画・保存
pygame.display.flip()
pygame.image.save(screen, ".temp/" + filename + ".png")
pygame.time.wait(3000)
pygame.quit()
print("use font is ", fontname)
print("filesave to ", ".temp/" + filename + ".png")
