""" endgame.py """

from pygame.locals import *

import tennischaracter as tc
import draw
import pygame

image_final_bonus = pygame.image.load("images/final_bonus.png")
image_gameover = pygame.image.load("images/gameover.png")

sound_finish = pygame.mixer.Sound("media/finish.wav")
sound_finish.set_volume(0.6)

#ゲームセット
def gameset():

        if counter > 5970:
            if character[0].x > 0:
                character[0].x -= 10
            elif character[0].x < 0:
                character[0].x += 10

        #勝利表示オン
        if counter == 5802:
            character[7].on(20)
        #フィニッシュ処理
        if counter == 6000:
            character[0].finish()
            score += 30000
            game_flag = 11
            sound_finish.play()

        #ゲームセット
        if game_flag == 11: #勝利
            SURFACE.blit(image_final_bonus, (125, 70))
        else: #敗北
            SURFACE.blit(image_gameover, (150, 129))

        #画面コピー
        filler = SURFACE.copy()

        #変数初期設定(ゲームオーバー)
        a = 0

        counter2 = 0

        #ループ3(ゲームオーバー)
        while game_flag >= 11:

            #カウンター(ゲームオーバー処理用)
            counter2 += 1
            if counter2 >= 210:
                game_flag = 0

            #BGMミュート＆停止
            if counter2 <= 120:
                pygame.mixer.music.set_volume(0.4 - counter2 / 300)
            else:
             	pygame.mixer.music.stop()

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

            #キー入力判定
            pressed = pygame.key.get_pressed()
            if pressed[K_SPACE] == 0 and a == 0:
                a = 1
            elif pressed[K_SPACE] and a == 1:
                a = 2
            elif pressed[K_SPACE] == 0 and a == 2:
                a = 0
                game_flag = 0

            #画面再描写(フルスクリーン対応)
            SURFACE.blit(filler, (0,0))

            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)
