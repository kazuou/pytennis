""" opening.py """


from pygame.locals import *

import tennischaracter as tc
import draw
import pygame


#変数初期設定(タイトル)
def opening():
    a = 0
    counter = 0

    tc.damage = 0
    tc.counter_point = 0
    tc.combo = 0
    tc.seta = 2
    tc.setb = 2
    tc.gamea = 10
    tc.gameb = 10
    tc.pointa = 0
    tc.pointb = 0

    #すべてのキャラクターを消す
    for i in range(len(tc.character)):
        tc.character[i].status = 0
    #自分を表示する
    tc.character[0].on(0)

    #自分の座標をグローバール変数に渡す
    draw.mex = tc.character[0].x
    draw.mey = tc.character[0].y
    draw.mez = tc.character[0].z
    print(draw.mex,draw.mey,draw.mez)

    #相手プレーヤー表示オン　counter=1
    tc.character[1].on(4)

    #ボール表示オンcounter=2
    tc.character[2].on(3)

    #ネット表示オンcounter=3
    tc.character[3].on(2)
    if tc.doubles == 1:
        tc.character[3].width =  548+548+91.4+91.4

    #ペア表示オンcounter=4
    if tc.doubles == 1:
        tc.character[4].on(1)

    #相手プレーヤー2表示オンcounter=5
    if tc.doubles == 1 :
        tc.character[5].on(5)

    #オープニングメッセージ1
    tc.character[6].on(11)

    #オープニングメッセージ1
    tc.character[7].on(12)

    #オープニング表示
    draw.game_flag = 1

    #ループ1(タイトル画面)
    while draw.game_flag == 1:

        counter += 1

        #キャラクターの移動
        for i in range(1, len(tc.character)):
            if tc.character[i].status > 0:
                tc.character[i].move_opening()


        draw.draw_all()

        #キー入力判定
        pressed = pygame.key.get_pressed()

        if pressed[K_SPACE]:
            a = 1
        elif pressed[K_SPACE] == 0 and a == 1:
            a = 0
            draw.game_flag = 21
            tc.character[6].off()
            tc.character[7].off()

        draw.FPSCLOCK.tick(30)
