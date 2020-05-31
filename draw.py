""" draw.py """

import pygame



pygame.init()
pygame.key.set_repeat(5, 5)
VideoInfo = pygame.display.Info()
# current_h, current_w:  現在のビデオモードでのウィンドウの幅と高さの値です。
# display.set_modeを実行する前にこの値を取得すると、パソコンのモニターの幅と高さの値が得られます。
print("h,w=",VideoInfo.current_h,VideoInfo.current_w)
SURFACE = pygame.display.set_mode((600+600, 300+600)) #1000x900 1366x768
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("AI Tennis")
sysfont = pygame.font.SysFont(None, 24)

image_background = pygame.image.load("background1.png")
image_shadow = pygame.image.load("shadow.gif")
image_court = pygame.image.load("court.png")
image_board = pygame.image.load("board.png")
image_title = pygame.image.load("title.png")
image_start = pygame.image.load("start.png")

fieldxl=-548.5-652
fieldxr=548.5+652
fieldy1= -612
fieldy2=2377+612
baseline2 = 2377
baseline1 = 0
servieline2 = 1828.5
servieline1 = 548.5

netline=1188.5
field_data = (fieldxl,fieldy1,fieldxr,fieldy2)
court_data = (-548.5,0,543.5,2377)



def location_in_view(x1, y1, z1):
    """ 3D座標から2D上の座標算出 """
    #ピンホールカメラの原理で表示
    #レンズ(ピンホール)の位置
    #詳しくはzahyotest.pyを参照

    xl = mex
    yl = mey-1250 #-1000で足元が見える
    zl = mez+150 #目の高さ

    adj_x = mex/2000 #見る角度　tanθで表現
    adj_z = mez/1000

    #フイルムの位置。レンズの -1000 近いと広角　遠いと望遠
    yf = 1000

    x1 = x1 - xl
    y1 = y1 - yl
    z1 = z1 - zl

    if y1 <= 0: #レンズより後ろは、そのモノをY軸に沿って、レンズの位置に来た所を返信
                #y軸と平行な線のみこれでちゃんと描画できる。
        y1 = 0

    x2 = int((x1+adj_x * y1) / (y1/yf + 1))
    z2 = int((z1+adj_z*y1) / (y1/yf + 1))

    #スクリーノ大きさと位置を調整。カットアンドトライで決めた
    x3 = (x2) + 300
    z3 = int(600-zl - (z2)*2)
    return (x3, z3)

def size_in_view(x1,y1,z1, size_x, size_z):
    """ 3D座標から2D上のサイズ算出 """
    #イメージの左上の座標と、右下の座標からサイズを計算
    #垂直の画像用
    (x2,z2) = location_in_view(x1-size_x/2,y1,z1)
    (x3,z3) = location_in_view(x1+size_x/2,y1,z1+size_z)
    return (abs(x3-x2), abs(z3-z2))

def size_in_view2(x1,y1,z1, size_x, size_y):
    """ 3D座標から2D上のサイズ算出 """
    #イメージの左上の座標と、右下の座標からサイズを計算
    #水平の画像用
    (x2,z2) = location_in_view(x1-size_x/2,y1-size_y/2,z1)
    (x3,z3) = location_in_view(x1+size_x/2,y1+size_y/2,z1)
    return (abs(x3-x2), abs(z3-z2))

def draw_character(image, x,  y, z, width, height):
    """ キャラクター描写 """
    #影表示
    if width < 300: #幅の狭いキャラクターのみ影表示
        c, d = size_in_view2(x,y,0, width, width)
        s_image = pygame.transform.scale(image_shadow, (c, d))
        s_image.set_alpha(80)
        a, b = location_in_view(x-width/2, y+width/2, 0)
        SURFACE.blit(s_image, (a, b))

    #キャラクター表示
    c, d = size_in_view(x,y,z,width, height)
    image = pygame.transform.scale(image, (c, d))
    a, b = location_in_view(x-width/2, y, z+height)
    SURFACE.blit(image, (a, b))

def draw_foreground():

    if tc.doubles == 1:
        chara=(tc.character[0],tc.character[1],tc.character[4],tc.character[5])
    else:
        chara=(tc.character[0],tc.character[1])


    #右のコート表示
    SURFACE.blit(image_court, (600, 0))

    #ポジションのまるを書く
    for i in chara:
        pos =(int(i.x/4+900),int(900-i.y/4-612/4))
        col=i.color
        pygame.draw.circle(SURFACE, col, pos, 10, 0)

    #コントロール領域を白く表示。(開発中)
    pygame.draw.rect(SURFACE, (254,254,254), (0, 600, 600, 900))

def draw_background(stage):
    """ 背景描写 """
    global seta,setb,gamea,gameb,pointa,pointb
    #テニスコートのラインのデータ。
    line_data = [(-548.5,0,-543.5,2377),(-411.5,0,-406.5,2377),
                (-2.5,548.5,2.5,1828.5),(543.5,0,548.5,2377),
                (406.5,0,411.5,2377),(-548.5,2367,548.5,2377),
                (-2.5,2357,2.5,2377),(-411.5,1823.5,411.5,1828.5),
                (-411.5,548.5,411.5,553.5),(-2.5,0,2.5,20),
                (-548.5,0,548.5,10)]

    a, b = location_in_view(0, 2377,0) #遠景

    image = pygame.transform.scale(image_background, (1200, 600))
    SURFACE.blit(image,(a - 600, b - 600))

    #フィールドのサイズ
    x1,y1,x2,y2 = field_data
    a, b = location_in_view(x2, y2 ,0) #地面
    pygame.draw.polygon(SURFACE, (189,104,86), ((0, b),(600,b),(600,600),(0,600)))

    #テニスコートのサイズ　ネットの位置は1188.5
    x1,y1,x2,y2 = court_data
    pygame.draw.polygon(SURFACE,(0, 128, 0), #テニスコート
                        (location_in_view(x1, y1, 0),
                         location_in_view(x2, y1, 0),
                         location_in_view(x2, y2, 0),
                         location_in_view(x1, y2, 0)))

    #テニスコートにラインを引く
    for i in range(len(line_data)): #ライン
        x1,y1,x2,y2 = line_data[i]
        pygame.draw.polygon(SURFACE,(255, 255, 255), #ライン描画
                        (location_in_view(x1, y1, 0),
                         location_in_view(x2, y1, 0),
                         location_in_view(x2, y2, 0),
                         location_in_view(x1, y2, 0)))
    if stage == 0:
        SURFACE.blit(image_board,(0,0))
    else :
        #スコアーを表示する。
        image = sysfont.render( #セット
            "Sets", True, (255, 255, 255))
        SURFACE.blit(image, (120, 2))
        image = sysfont.render(
            "{:0>1}-{:0>1}".format(seta,setb), True, (255, 255, 255))
        SURFACE.blit(image, (125, 17))
        image = sysfont.render( #ゲーム
            "Game", True, (255, 255, 255))
        SURFACE.blit(image, (230, 2))
        image = sysfont.render(
            "{:0>2}-{:0>2}".format(gamea,gameb), True, (255, 255, 255))
        SURFACE.blit(image, (235, 17))
        image = sysfont.render( #ポイント
            "Points", True, (255, 255, 255))

        SURFACE.blit(image, (320, 2))
        image = sysfont.render(
            "{:>2}-{:>2}".format(pointa,pointb), True, (255, 255, 255))
        SURFACE.blit(image, (325, 17))

def drow_credit():
    #クレジット表示
    image = sysfont.render(
        "c 2020 KAZUOU", True, (255, 255, 255))
    SURFACE.blit(image, (250,  560))


def draw_all():

    #背景描写
    draw_background(0)

    #キャラクター描写
    character_copy = tc.character
    character_copy = sorted(character_copy, key=lambda i: i.y, reverse=True)

    for i in range(len(character_copy)):
        if character_copy[i].status > 0:
            draw.draw_character(character_copy[i].image, character_copy[i].x, character_copy[i].y, character_copy[i].z,
                           character_copy[i].width, character_copy[i].height)

    drow_credit()

    #右の平面図を表示する。
    draw_foreground()

    #画面コピー
    filler = SURFACE.copy()

    #画面再描写(フルスクリーン対応)
    SURFACE.blit(filler, (0,0))

    #画面アップデート
    pygame.display.update()

    #ウィンドウ閉じるボタン
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_F11:
            #F11でフルスクリーンモードへの切り替え
            fullscreen_flag = not fullscreen_flag
            if fullscreen_flag:
                screen = pygame.display.set_mode((1200, 900), FULLSCREEN)
            else:
                screen = pygame.display.set_mode((1200, 900), 0)
