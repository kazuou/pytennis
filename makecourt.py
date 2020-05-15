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
SURFACE = pygame.display.set_mode((600, 900))
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("makepng")
sysfont = pygame.font.SysFont(None, 24)

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

def location_in_view(x1, y1, z1, size_x, size_z, adj_x, adj_y, adj_z):
    """ 3D座標から2D上の座標算出 """
    x2 = x1 /4 +600/2
    z2 = y1 /4 +612/4
#    x1=x1/®2
#    y1=(y1+1000-adj_y)/100 #10m後ろからの視点
#    if(y1 <= 0):
#        y1 = 0
#    x2 = int((x1 + adj_x * y1) / (y1/10 + 1)) + 200 - int(size_x * 0.5 / (y1/10 + 1))
#    z2 = int((z1 + adj_z * y1) / (y1/10 + 1)) + 150 - int(size_z * 0.5 / (y1/10 + 1))
    return (x2, z2)


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
    pygame.draw.polygon(SURFACE,(189, 104, 86), #テニスコート
                    (location_in_view(x1, y1, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                     location_in_view(x2, y1, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                     location_in_view(x2, y2, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                     location_in_view(x1, y2, 150, 0, 0, adjust_x, adjust_y, adjust_z)))

    #a, b = location_in_view(x2, y2 ,150, 0, 0, adjust_x, adjust_y, adjust_z) #地面
    #pygame.draw.rect(SURFACE, (189,104,86), (0, b, 400, 300))

    #テニスコートのサイズ　ネットの位置は1188.5
    #court_data = (-548.5,2377,543.5,0)
    x1,y1,x2,y2 = court_data

    pygame.draw.polygon(SURFACE,(18, 173, 43), #テニスコート
                        (location_in_view(x1, y1, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y1, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y2, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x1, y2, 150, 0, 0, adjust_x, adjust_y, adjust_z)))


    for i in range(len(line_data)): #ライン
        x1,y1,x2,y2 = line_data[i]
        pygame.draw.polygon(SURFACE,(255, 255, 255), #ライン描画
                        (location_in_view(x1, y1, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y1, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x2, y2, 150, 0, 0, adjust_x, adjust_y, adjust_z),
                         location_in_view(x1, y2, 150, 0, 0, adjust_x, adjust_y, adjust_z)))
def main():
    """ メインルーチン """
    #変数初期設定(基本)
    a, b, c, d = 0, 0, 0, 0
    round_data = [(50, 0, 0), (50, 0, 0), (0, 80, 0), (0, 70, 0), (50, 80, 0), (50, 70, 0), (10, 0, 0), (15, 0, 0), (0, 0, 100), (0, 0, 50),
                  (0, 30, 0), (0, 30, 0), (30, 0, 50), (30, 0, 50), (50, 50, 50), (50, 50, 50), (30, 40, 0), (15, 40, 40), (15, 30, 30), (0, 0, 0)]

    counter = 0
    print("Hello World")

    #マウスカーソル非表示
    pygame.mouse.set_visible(False)

    while True:

        #変数初期設定(タイトル)
        a = 0
        title_y = 1500
        adjust_x = 0
        adjust_y = 0
        adjust_z = 5
        gameover_flag = 3

        #背景描写
        draw_background(adjust_x, adjust_y, adjust_z, counter)

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

            #画面再描写(フルスクリーン対応)
            SURFACE.blit(filler, (0,0))


            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)


if __name__ == '__main__':
    main()
