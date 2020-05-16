""" makepng.py """

#【メモ】
#テニスコートを描画
#スペースキーで保存

import math
import pygame
import random
import sys
import os
from pygame.locals import *

print(os.getcwd())
pygame.init()
pygame.key.set_repeat(5, 5)
#SURFACE = pygame.display.set_mode((1200, 600))
#SURFACE = pygame.display.set_mode((400, 600))
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("makepng")
sysfont = pygame.font.SysFont(None, 24)
image_shadow = pygame.image.load("shadow.gif")

baseline2 = 2377
baseline1 = 0
servieline2 = 1828.5
servieline1 = 548.5

court_data = (-548.5,0,543.5,2377)
fieldxl=-548-652
fieldxr=548+652
fieldy1= -612
fieldy2=2377+612
netline=1188.5
field_data = (fieldxl,fieldy1,fieldxr,fieldy2)
class Character:
    """キャラクターーオブジェクト"""
    def __init__(self):
        self.status = 0
        self.x = 999
        self.y = 0
        self.z = 0
        self.image_man = pygame.image.load("man.png")
        self.image_man3 = pygame.image.load("man3.png")
        self.image_net = pygame.image.load("net.png")
        self.image_ball = pygame.image.load("TennisBall.png")

    def on(self, image_type, x = 0, y = baseline2 ,z = 0):
        self.status = 1
        self.image_type = image_type
        if self.image_type == 0: #私
            self.x = 0
            self.y = 0
            self.z = 0
            self.width = 100
            self.height = 170
            self.image = self.image_man
        if self.image_type == 1: #対戦相手
            self.x = -200
            self.y = baseline2
            self.z = 0
            self.width = 100
            self.height = 100
            self.image = self.image_man3
        if self.image_type == 2: #ネット
            self.x = 0
            self.y = netline
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.width = 548+548+91.4+91.4
            self.height = 91.4
            self.image = self.image_net
        if self.image_type == 3: #ボール
            self.x = -200
            self.y = baseline2
            self.z = 40
            self.vx = 0
            self.vy = -70
            self.vz = -18.0
            self.width = 30
            self.height = 30
            self.color = (255,255,0)
            self.mag = 30
            self.image = self.image_ball

def location_in_view(x1, y1, z1, size_x, size_z, adj_x, adj_y, adj_z):
    """ 3D座標から2D上の座標算出 """
#    x2 = int((x1 + adj_x * y1) / (y1/10 + 1)) + 200 - int(size_x * 0.5 / (y1/10 + 1))
#    z2 = int((z1 + adj_z * y1) / (y1/10 + 1)) + 150 - int(size_z * 0.5 / (y1/10 + 1))

    #カメラの位置は0,0
    #フイルムの位置は0,-10m後ろ　600x600
#    az = 0.063
#    z1 = z1 +150
#view は　0,-10m,150cm
    az = 0.1

    #レンズは0,0,0
    xl = 100
    yl = -1000
    zl = 150

    #フイルムはレンズの -1000
    yf = 1000

    x1 = x1 - xl
    y1 = y1 - yl
    z1 = z1 - zl

    if y1 <= 0 :
        y1 = 0

    x2 = int((x1) / (y1/yf + 1))
    z2 = int((z1+az*y1) / (y1/yf + 1))

    x3 = (x2) + 300
    z3 = 500-zl - (z2)*2
#    z3 = 300 - (z2)/4
#    x1=x1/®2
#    y1=(y1+1000-adj_y)/100 #10m後ろからの視点
#    if(y1 <= 0):
#        y1 = 0
#    x2 = int((x1 + adj_x * y1) / (y1/10 + 1)) + 200 - int(size_x * 0.5 / (y1/10 + 1))
#    z2 = int((z1 + adj_z * y1) / (y1/10 + 1)) + 150 - int(size_z * 0.5 / (y1/10 + 1))
    return (x3, z3)

def size_in_view(x1,y1,z1, size_x, size_z):
    """ 3D座標から2D上のサイズ算出 """
#    az = 0
    (x2,z2) = location_in_view(x1-size_x/2,y1,z1,0,0,0,0,0)
    (x3,z3) = location_in_view(x1+size_x/2,y1,z1+size_z,0,0,0,0,0)
    return (abs(x3-x2), abs(z3-z2))

def size_in_view2(x1,y1,z1, size_x, size_y):
    """ 3D座標から2D上のサイズ算出 """
#    az = 0
    (x2,z2) = location_in_view(x1-size_x/2,y1-size_y/2,z1,0,0,0,0,0)
    (x3,z3) = location_in_view(x1+size_x/2,y1+size_y/2,z1,0,0,0,0,0)
    return (abs(x3-x2), abs(z3-z2))

def draw_character(image, x,  y, z, width, height, adjust_x, adjust_y, adjust_z):
    """ キャラクター描写 """
    #影表示
    if width < 300: #幅の狭いキャラクターのみ影表示
        c, d = size_in_view2(x,y,0, width, width)
        s_image = pygame.transform.scale(image_shadow, (c, d))
        s_image.set_alpha(80)
        a, b = location_in_view(x-width/2, y+width/2, 0, width, width, adjust_x, adjust_y, adjust_z)
        SURFACE.blit(s_image, (a, b))
        print("影",x,y,z,c,d,a,b)

    #キャラクター表示
    c, d = size_in_view(x,y,z,width, height)
#    if width >= 300 and width <= 350: #ロゴのみスムース縮小
#        image = pygame.transform.smoothscale(image, (c, d))
#    else:
    image = pygame.transform.scale(image, (c, d))
    a, b = location_in_view(x-width/2, y, z+height, width, height, adjust_x, adjust_y, adjust_z)
    SURFACE.blit(image, (a, b))
    print("キャラクタ",x,y,z,c,d,a,b)

def draw_background(adjust_x, adjust_y, adjust_z, counter):
    """ 背景描写 """
    line_data = [(-548.5,0,-543.5,2377),(-411.5,0,-406.5,2377),
                (-2.5,548.5,2.5,1828.5),(543.5,0,548.5,2377),
                (406.5,0,411.5,2377),(-548.5,2367,548.5,2377),
                (-2.5,2357,2.5,2377),(-411.5,1823.5,411.5,1828.5),
                (-411.5,548.5,411.5,553.5),(-2.5,0,2.5,20),
                (-548.5,0,548.5,10),
                (-543.5-91.4,1188.5-1,548.5+91.4,1188.5+1)]

    #フィールドのサイズ
    x1,y1,x2,y2 = field_data
    pygame.draw.polygon(SURFACE,(189, 104, 86), #テニスコート茶色の部分
                    (location_in_view(x1, y1, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                     location_in_view(x2, y1, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                     location_in_view(x2, y2, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                     location_in_view(x1, y2, 0, 0, 0, adjust_x, adjust_y, adjust_z)))

    #a, b = location_in_view(x2, y2 ,150, 0, 0, adjust_x, adjust_y, adjust_z) #地面
    #pygame.draw.rect(SURFACE, (189,104,86), (0, b, 400, 300))

    #テニスコートのサイズ　ネットの位置は1188.5
    #court_data = (-548.5,2377,543.5,0)
    x1,y1,x2,y2 = court_data
    pygame.draw.polygon(SURFACE,(18, 173, 43), #テニスコート緑色の部分
                        (location_in_view(x1, y1, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y1, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y2, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x1, y2, 0, 0, 0, adjust_x, adjust_y, adjust_z)))


    for i in range(len(line_data)): #ライン
        x1,y1,x2,y2 = line_data[i]
        pygame.draw.polygon(SURFACE,(255, 255, 255), #ライン描画
                        (location_in_view(x1, y1, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y1, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y2, 0, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x1, y2, 0, 0, 0, adjust_x, adjust_y, adjust_z)))
def main():
    """ メインルーチン """
    #変数初期設定(基本)
    character_copy = []
    counter = 0
    print("Hello World")
    character = [Character() for i in range(4)]
    for i in range(len(character)):
        character[i].status = 0

    #自分を表示する
    character[0].on(0)
    character[1].on(1)
    character[2].on(2)
    character[3].on(3)


    for i in range(len(character)):
        print("character ",i,"=",character[i].x,character[i].y,character[i].z)

    #マウスカーソル非表示
    pygame.mouse.set_visible(False)

    while True:

        #変数初期設定(タイトル)
        a = 0
        title_y = 1500
        adjust_x = 0
        adjust_y = 0
        adjust_z = 0
        gameover_flag = 3

        #背景描写
        pygame.draw.polygon(SURFACE,(125,125,125), ((0,0),(0,599),(599,599),(599,0)))


        draw_background(adjust_x, adjust_y, adjust_z, counter)

        (x,y) = location_in_view(0, 0, 0, 0, 0, adjust_x, adjust_y, adjust_z)
        pygame.draw.circle(SURFACE, (255,255,255),(x,y), 10, width=0)

        (x,y) = location_in_view(548, 0, 0, 0, 0, adjust_x, adjust_y, adjust_z)
        pygame.draw.circle(SURFACE, (255,0,0),(x,y), 10, width=0)

        (x,y) = location_in_view(0, netline, 0, 0, 0, adjust_x, adjust_y, adjust_z)
        pygame.draw.circle(SURFACE, (0,0,255),(x,y), 10, width=0)

        (x,y) = location_in_view(0, netline, 150, 0, 0, adjust_x, adjust_y, adjust_z)
        pygame.draw.circle(SURFACE, (0,255,255),(x,y), 10, width=0)

        (x,y) = location_in_view(0, baseline1, 200, 0, 0, adjust_x, adjust_y, adjust_z)
        pygame.draw.circle(SURFACE, (255,255,0),(x,y), 10, width=0)

        (x,y) = location_in_view(0, netline, 300, 0, 0, adjust_x, adjust_y, adjust_z)
        pygame.draw.circle(SURFACE, (255,125,0),(x,y), 10, width=0)

        pygame.draw.polygon(SURFACE,(0,0,0), ((0,300),(599,300),(599,301),(0,301)))
        pygame.draw.polygon(SURFACE,(0,0,0), ((300,0),(300,599),(301,599),(301,0)))

        #キャラクター描写
        character_copy = character
        for i in range(len(character_copy)):
            if character_copy[i].status > 0:
                draw_character(character_copy[i].image, character_copy[i].x, character_copy[i].y, character_copy[i].z,character_copy[i].width, character_copy[i].height, adjust_x, adjust_y, adjust_z)



        #画面コピー
        filler = SURFACE.copy()

        #ループ1(タイトル画面)
        while gameover_flag == 3:

            #ウィンドウ閉じるボタン
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_F11:
                    #F11でフルスクリーンモードへの切り替え
                    fullscreen_flag = not fullscreen_flag
                    if fullscreen_flag:
                        screen = pygame.display.set_mode((400, 300), FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((400, 300), 0)

            #キー入力判定
            pressed = pygame.key.get_pressed()
            if pressed[K_SPACE]:
                a = 1
            elif pressed[K_SPACE] == 0 and a == 1:
                a = 0
                pygame.image.save(SURFACE,"image.png")
                gameover_flag = 0
                pygame.quit()
                sys.exit()
            elif pressed[K_ESCAPE]:
                pygame.quit()
                sys.exit()


            #画面再描写(フルスクリーン対応)
            SURFACE.blit(filler, (0,0))


            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)


if __name__ == '__main__':
    main()
