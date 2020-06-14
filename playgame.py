""" playgame.py """


import tennischaracter as tc
import draw
import pygame
from pygame.locals import *

#判定範囲(この中にボールの中心がきていればOK。3.3cm大きくしている)
judge_s1d=(-414.8,1831.8,5.8,1188.5)
judge_s1a=(414.8,1831.8,-5.8,1188.5)
judge_s2d=(-414.8,1188.5,5.8,545.2)
judge_s2a=(414.8,1188.5,-5.8,545.2)

judge_d1=(-551.8,2380.3,551.8,1188.5)
judge_d2=(-551.8,1188.5,551.8,-3.3)

judge_s1=(-414.8,2380.3,414.8,1188.5)
judge_s2=(-414.8,1188.5,414.8,-3.3)
#効果音

sound_jump = pygame.mixer.Sound("media/jump.wav")
sound_jump.set_volume(0.25)
sound_eat = pygame.mixer.Sound("media/eat.wav")
sound_eat.set_volume(0.3)
sound_omusubi = pygame.mixer.Sound("media/omusubi.wav")
sound_omusubi.set_volume(0.6)

sound_crash = pygame.mixer.Sound("media/crash.wav")
sound_crash.set_volume(0.4)
sound_miss = pygame.mixer.Sound("media/miss.wav")
sound_miss.set_volume(0.6)

#変数初期設定(タイトル)
def playgame():
    #変数初期設定(ゲーム)
    print("start playgame")
    tc.seta = 2
    tc.setb = 2
    tc.gamea = 10
    tc.gameb = 10
    tc.pointa = 0
    tc.pointb = 0
    tc.score = 0
    tc.damage = 0
    counter = 0

    #BGM再生
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    tc.character[0].image=tc.image_man1

    #ループ2(ゲームメインループ)
    while draw.game_flag > 20:

        #キー入力判定＆とび職人移動
        if character[0].status < 200 and counter <= 5970:
            pressed = pygame.key.get_pressed()
            if pressed[K_LEFT] and character[0].x > fieldxl+50:
                character[0].x -= 20
            if pressed[K_RIGHT] and character[0].x < fieldxr-50:
                character[0].x += 20
            if pressed[K_UP] and character[0].y < netline-50:
                character[0].y += 20
            if pressed[K_DOWN] and character[0].y > fieldy1+50:
                character[0].y -= 20
            if pressed[K_SPACE] and character[0].jump_status == 1:
                sound_jump.play()
                character[0].jump_status = 2
                character[0].vz = +26
        if character[0].jump_status == 2:
            character[0].z += character[0].vz
            character[0].vz -= 2
            if character[0].z <= 0:
                character[0].z = 0
                character[0].jump_status = 1
        #adjust_x = character[0].x / 30
        #adjust_z = character[0].z / 20
        #adjust_x = character[0].x /1000
        #adjust_y = character[0].y
        #adjust_z = 0.1+character[0].z /1000
        mex = character[0].x
        mey = character[0].y
        mez = character[0].z


        #おむすび表示オン
        if counter > 300 and counter < 5900 and counter % 600 == 150:
            if character[6].status == 0:
                character[6].on(10)




        #キャラクター移動
        if character[0].status < 200 and counter < 6000:
            for i in range(1, len(character)):
                if character[i].status > 0:
                    a, b = character[i].move(character[0].x, character[0].y, character[0].z, character[0].status)
                    if a == 1: #ミス処理開始
                        character[0].status = 200
                        character[0].jump_status = 2
                        character[0].vx = 0
                        character[0].vz = -24
                        damage += 25
                        sound_crash.play()
                        sound_miss.play()
                    if a == 2: #得点処理
                        combo += 1
                        score += 1000 * combo
                        counter_point = 1
                        point_x = b - 40
                        sound_eat.play()
                        sound_omusubi.play()
                    if a == 3: #おむすび取り逃し(コンボ消滅)
                        combo = 0

        #ミス処理
        if character[0].status >= 200:
            character[0].failure()
            if damage == 100 and character[0].status == 259:
                drow.game_flag = 11
        elif character[0].status >= 10:
            character[0].blink()

        #ポイント表示
        if counter_point > 0:
            counter_point += 1
            a, b = location_in_view(point_x, character[0].y,0)
            image = sysfont.render(
                "{:^10}".format("1000 x " + str(combo)), True, (255, 0, 0))
            SURFACE.blit(image, (a, b))
            if counter_point > 30:
                counter_point = 0


        draw.draw_all()

        #BGM再生確認&リピート
        if pygame.mixer.music.get_busy() == 0:
            pygame.mixer.music.play()
