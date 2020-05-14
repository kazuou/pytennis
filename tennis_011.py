""" tobi.py """

#【メモ】
#3D座標は x = 0, z = 0が画面の中心で、y = 0が画面の手前。キャラクターのx, z座標はキャラクターの中心。
#大きさ調整は、自分のy座標を-10、スクリーンのy座標を0(自分とスクリーンの距離10)とした場合、キャラクターのy座標が20の場合には3((20+10)÷10)で割り、30の場合には4((30+10)÷10)で割る計算。
#キャラクターの座標は、自分とスクリーンの距離を10とした場合、キャラクターのy座標が30の場合には、画面の中心の座標から、xを4((30+10)÷10)で割ったものを足し、キャラクターの大きさの半分を4((30+10)÷10)で割ったものをxから引く。zも同様。
#視点の調整は「係数 * y」を x や z に足す(その x や z をさらに上記の通りy座標の奥行きに合わせて割り算する)。

import math
import pygame
import random
import sys
import os
from pygame.locals import *

print(os.getcwd())
pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((400, 300))
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("Tobishokunin's Commuting")
sysfont = pygame.font.SysFont(None, 24)

#イメージ設定
image_background = pygame.image.load("background.jpg")
image_title = pygame.image.load("title.png")
image_start = pygame.image.load("start.png")
image_final_bonus = pygame.image.load("final_bonus.png")
image_gameover = pygame.image.load("gameover.png")
image_shadow = pygame.image.load("shadow.gif")

#効果音
sound_frog_jump = pygame.mixer.Sound("frog_jump.wav")
sound_frog_jump.set_volume(0.2)
sound_bird_fly = pygame.mixer.Sound("bird_fly.wav")
sound_bird_fly.set_volume(0.25)
sound_jump = pygame.mixer.Sound("jump.wav")
sound_jump.set_volume(0.25)
sound_eat = pygame.mixer.Sound("eat.wav")
sound_eat.set_volume(0.3)
sound_omusubi = pygame.mixer.Sound("omusubi.wav")
sound_omusubi.set_volume(0.6)
sound_crash = pygame.mixer.Sound("crash.wav")
sound_crash.set_volume(0.4)
sound_miss = pygame.mixer.Sound("miss.wav")
sound_miss.set_volume(0.6)
sound_finish = pygame.mixer.Sound("finish.wav")
sound_finish.set_volume(0.6)

#BGM
pygame.mixer.music.load("bgm.wav")

class Character:
    """キャラクターーオブジェクト"""
    def __init__(self):
        self.status = 0
        self.jump_status = 0
        self.image_type = 0
        self.x = 999
        self.z = 999
        self.y = 0
        self.vx = 0
        self.vz = 0
        self.vy = 0
        self.width = 0
        self.height = 0
        self.image_man = pygame.image.load("man.gif")
        self.image_man_bright = pygame.image.load("man_bright.gif")
        self.image_man_failed = pygame.image.load("man_failed.gif")
        self.image_man_smile = pygame.image.load("man_smile.gif")
        self.image_tree = pygame.image.load("tree.gif")
        self.image_stopper = pygame.image.load("stopper.gif")
        self.image_frog = pygame.image.load("frog.gif")
        self.image_frog_jump1 = pygame.image.load("frog_jump1.gif")
        self.image_frog_jump2 = pygame.image.load("frog_jump2.gif")
        self.image_bird_right = pygame.image.load("bird_right.gif")
        self.image_bird_left = pygame.image.load("bird_left.gif")
        self.image_omusubi = pygame.image.load("omusubi.gif")
        self.image_house = pygame.image.load("house.gif")
        self.image = self.image_frog

    #表示オン
    def on(self, image_type, x = 0, z = 0, y = 200):
        self.status = 1
        self.image_type = image_type
        if self.image_type == 0: #私
            self.jump_status = 1
            self.x = 0
            self.z = 100
            self.y = 0
            self.vx = 0
            self.vz = 0
            self.vy = 0
            self.width = 40
            self.height = 100
            self.image = self.image_man
        if self.image_type == 1: #味方
            self.x = 50
            self.z = 100
            self.y = 10
            self.vx = 0
            self.vz = 0
            self.vy = 0
            self.width = 40
            self.height = 100
            self.image = self.image_man
        if self.image_type == 2: #ネット
            self.x = 0
            self.z = 115
            self.y = 40
            self.vx = 0
            self.vz = 0
            self.vy = 0
            self.width = 600
            self.height = 70
            self.image = self.image_stopper
        if self.image_type == 3: #ボール
            self.x = random.randint(-160, 160)
            self.z = 110
            self.y = y
            self.vx = 0
            self.vz = 0
            self.vy = -1
            self.width = 80
            self.height = 80
            self.image = self.image_frog
        if self.image_type == 4: #相手プレーヤー
            self.x = 50
            self.z = 40
            self.y = 60
            self.vx = 0
            self.vz = (random.randint(0, 1) * 2 - 1) * 5
            self.vy = -2
            self.width = 80
            self.height = 80
            self.image = self.image_bird_right
        if self.image_type == 5: #相手プレーヤー2
            self.x = -50
            self.z = 40
            self.y = 80
            self.vx = 0
            self.vz = (random.randint(0, 1) * 2 - 1) * 5
            self.vy = -2
            self.width = 80
            self.height = 80
            self.image = self.image_bird_left

        if self.image_type == 10: #おむすび
            self.x = random.randint(-170, 170)
            self.z = 130
            self.y = y
            self.vx = 0
            self.vz = 0
            self.vy = -1
            self.width = 60
            self.height = 40
            self.image = self.image_omusubi
        if self.image_type == 20: #家
            self.x = -20
            self.z = -5
            self.y = y
            self.vx = 0
            self.vz = 0
            self.vy = -1
            self.width = 360
            self.height = 310
            self.image = self.image_house

    #移動
    def move(self, x, z, y, status):
        if self.image_type == 1 or self.image_type == 2 or self.image_type == 10 or self.image_type == 20: #樹木、ストッパー、おむすび、家
            self.y += self.vy
            self.z += self.vz
        elif self.image_type == 3: #蛙
            self.status += 1
            self.x += self.vx
            self.z += self.vz
            self.y += self.vy
            if self.status >= 5 and self.status < 20 and random.randint(0, 10) == 0: #ジャンプ前
                self.status = 20
            if self.status >= 20 and self.status <= 22: #ジャンプ動作1
                self.image = self.image_frog_jump1
            elif self.status == 23: #ジャンプ動作2に移行
                if self.y <= 150:
                    sound_frog_jump.play()
                self.image = self.image_frog_jump2
                self.vz = -26
                self.vy = 2 if self.vy > 0 else -2
                if self.x > x:
                    self.vx = random.randint(-10, 0)
                else:
                    self.vx = random.randint(0, 10)
            elif self.status >= 24: #ジャンプ動作2
                self.vz += 2
                if self.z > 110:
                    self.z = 110
                    self.status = 1
                    self.vx = 0
                    self.vz = 0
                    self.vy = 1 if self.vy > 0 else -1
                    self.image = self.image_frog
            if self.y <= 2 and self.vy < 0 :
                self.vy = -self.vy
                self.y = 2
            if self.y >= 198 and self.vy > 0:
                self.vy = -self.vy
                self.y = 198

        elif (self.image_type == 4 or self.image_type == 5): #鳥
            self.x += self.vx
            self.z += self.vz
            self.y += self.vy
            if self.x > x:
                self.vx -= 1
            elif self.x < x:
                self.vx += 1
            if (self.x >= 100 and self.vx > 0) or (self.x <= -100 and self.vx < 0):
                self.vx = int(self.vx / 2)
            if self.vx >= 0:
                self.image = self.image_bird_right
            else:
                self.image=  self.image_bird_left
            if self.z < -110:
                self.z = -110
                self.vz = -self.vz
            elif self.z > 40:
                self.z = 40
                self.vz = -self.vz
            if self.y == 40:
                sound_bird_fly.play()
            if self.y <= 42 and self.vy < 0 :
                self.vy = -self.vy
                self.y = 42
            if self.y >= 84 and self.vy > 0:
                self.vy = -self.vy
                self.y = 84

        #スクリーンより前面(y < 0)の場合には消去
        if self.y < 0:
            self.status = 0
            self.y = 0
            if self.image_type == 10:
                return(3, self.x)
            else:
                return(0, self.x)

        #衝突判定
        if status == 1 and self.image_type <= 9: #敵衝突ミス
            if self.status > 0 and self.y <= 1 and abs(self.x - x) < self.width / 2  + 10 and abs(self.z - z) < self.height / 2 + 40:
                self.y = 0
                return(1, self.x)
            else:
                return(0, self.x)
        elif status < 200 and self.image_type == 10: #おむすび取得
            if self.status > 0 and self.y <= 1 and abs(self.x - x) < self.width / 2  + 10 and abs(self.z - z) < self.height / 2 + 40:
                self.status = 0
                self.y = 0
                return(2, self.x)
            else:
                return(0, self.x)
        else:
            return(0, self.x)

    #とび職男ミス
    def failure(self):
        if self.image_type == 0:
            self.image = self.image_man_failed
            self.status += 1
            if self.status >= 260:
                self.status = 10
                self.image = self.image_man

    #とび職男ミス復帰(点滅表示)
    def blink(self):
        if self.image_type == 0:
            self.status += 1
            if self.status % 10 < 5:
                self.image = self.image_man_bright
            else:
                self.image = self.image_man
            if self.status >= 70:
                self.status = 1
                self.image = self.image_man

    #とび職男フィニシュ
    def finish(self):
        if self.image_type == 0:
            self.image = self.image_man_smile

def location_in_view(x1, z1, y1, size_x, size_z, adj_x, adj_z):
    """ 3D座標から2D上の座標算出 """
    x2 = int((x1 + adj_x * y1) / (y1/10 + 1)) + 200 - int(size_x * 0.5 / (y1/10 + 1))
    z2 = int((z1 + adj_z * y1) / (y1/10 + 1)) + 150 - int(size_z * 0.5 / (y1/10 + 1))
    return (x2, z2)

def size_in_view(y1, size_x, size_z):
    """ 3D座標から2D上のサイズ算出 """
    size_x2 = int(size_x / (y1/10 + 1))
    size_z2 = int(size_z / (y1/10 + 1))
    return (size_x2, size_z2)


def draw_background(adjust_x, adjust_z, counter):
    """ 背景描写 """
    line_data = [(-548.5,2377,-543.5,0),(-411.5,2377,-406.5,0),
                (-2.5,1828.5,2.5,548.5),(543.5,2377,548.5,0),
                (406.5,2377,411.5,0),(-548.5,2377,548.5,2367),
                (-2.5,2377,2.5,2357),(-411.5,1828.5,411.5,1823.5),
                (-411.5,553.5,411.5,548.5),(-2.5,20,2.5,0),
                (-548.5,10,548.5,0)]
    #テニスコートのサイズは

    a, b = location_in_view(0, 0, 200, 0, 0, adjust_x, adjust_z) #遠景
    SURFACE.blit(image_background,(a - 300, b - 320))
    a, b = location_in_view(-200, 150, 200, 0, 0, adjust_x, adjust_z) #地面
    pygame.draw.rect(SURFACE, (189,104,86), (0, b, 400, 300))

    court_data = (-548.5,2377,543.5,0)
    x1,y1,x2,y2 = court_data
    x1=x1/2
    x2=x2/2
    y1=y1/100+10
    y2=y2/100+10

    pygame.draw.polygon(SURFACE,(0, 128, 0), #テニスコート
                        (location_in_view(x1, 150, y1, 0, 0, adjust_x, adjust_z),
                        location_in_view(x2, 150, y1, 0, 0, adjust_x, adjust_z),
                         location_in_view(x2, 150, y2, 0, 0, adjust_x, adjust_z),
                         location_in_view(x1, 150, y2, 0, 0, adjust_x, adjust_z)))


    for i in range(len(line_data)): #ライン
        x1,y1,x2,y2 = line_data[i]
        x1=x1/2
        x2=x2/2
        y1=y1/100+10
        y2=y2/100+10
        pygame.draw.polygon(SURFACE,(255, 255, 255), #テニスコート
                        (location_in_view(x1, 150, y1, 0, 0, adjust_x, adjust_z),
                        location_in_view(x2, 150, y1, 0, 0, adjust_x, adjust_z),
                         location_in_view(x2, 150, y2, 0, 0, adjust_x, adjust_z),
                         location_in_view(x1, 150, y2, 0, 0, adjust_x, adjust_z)))


def draw_character(image, x, z, y, width, height, adjust_x, adjust_z):
    """ キャラクター描写 """
    #影表示
    if width < 300: #幅の狭いキャラクターのみ影表示
        c, d = size_in_view(y, width, width)
        s_image = pygame.transform.scale(image_shadow, (c, d))
        s_image.set_alpha(80)
        a, b = location_in_view(x, 147, y, width, width, adjust_x, adjust_z)
        SURFACE.blit(s_image, (a, b))

    #キャラクター表示
    c, d = size_in_view(y, width, height)
#    if width >= 300 and width <= 350: #ロゴのみスムース縮小
#        image = pygame.transform.smoothscale(image, (c, d))
#    else:
    image = pygame.transform.scale(image, (c, d))
    a, b = location_in_view(x, z, y, width, height, adjust_x, adjust_z)
    SURFACE.blit(image, (a, b))

def score_indication(seta,setb,gamea,gameb,pointa,pointb):
    image = sysfont.render( #スコア
        "Sets", True, (255, 255, 255))
    SURFACE.blit(image, (120, 2))
    image = sysfont.render(
        "{:0>1}-{:0>1}".format(seta,setb), True, (255, 255, 255))
    SURFACE.blit(image, (147, 17))
    image = sysfont.render( #距離
        "Game", True, (255, 255, 255))
    SURFACE.blit(image, (230, 2))
    image = sysfont.render(
        "{:0>1}-{:0>1}".format(gamea,gameb), True, (255, 255, 255))
    SURFACE.blit(image, (248, 17))
    image = sysfont.render( #ダメージ
        "Points", True, (255, 255, 255)) #sysfontで"Damage"と表示,ならめらかにする、色
    SURFACE.blit(image, (322, 2))
    image = sysfont.render(
        "{:>2}-{:>2}".format(pointa,pointb), True, (255, 255, 255))
    SURFACE.blit(image, (340, 17))


def score_indication2(score, best_score, counter, damage):
    """ スコア表示 """
    #image = sysfont.render( #ベストスコア
    #    "Best Score", True, (255, 255, 255))
    #SURFACE.blit(image, (10, 2))
    #image = sysfont.render(
    #    "{:0>6}".format(best_score), True, (255, 255, 255))
    #SURFACE.blit(image, (36, 17))
    image = sysfont.render( #スコア
        "Sets", True, (255, 255, 255))
    SURFACE.blit(image, (120, 2))

def main():
    """ メインルーチン """
    #変数初期設定(基本)
    a, b, c, d = 0, 0, 0, 0
    round_data = [(50, 0, 0), (50, 0, 0), (0, 80, 0), (0, 70, 0), (50, 80, 0), (50, 70, 0), (10, 0, 0), (15, 0, 0), (0, 0, 100), (0, 0, 50),
                  (0, 30, 0), (0, 30, 0), (30, 0, 50), (30, 0, 50), (50, 50, 50), (50, 50, 50), (30, 40, 0), (15, 40, 40), (15, 30, 30), (0, 0, 0)]
    character = [Character() for i in range(50)]
    character_copy = []
    counter = 0
    best_score = 0
    score = 0
    point_x = 0
    fullscreen_flag = 0
    doubles = 0

    #マウスカーソル非表示
    pygame.mouse.set_visible(False)

    while True:

        #変数初期設定(タイトル)
        a = 0
        title_y = 150
        adjust_x = 0
        adjust_z = 5
        gameover_flag = 3
        damage = 0
        counter_character = 1
        counter_point = 0
        combo = 0
        tree_lr = -1
        seta = 0
        setb = 0
        gamea = 0
        gameb = 0
        pointa = 0
        pointb = 0

        for i in range(len(character)):
            character[i].status = 0
        character[0].on(0)
        rate_stopper, rate_frog, rate_bird = round_data[0]


        #樹木初期表示オン
        #for i in range (0, 201, 20):
        #    character[counter_character].on(1, tree_lr * 270, 0, i)
        #    tree_lr = -tree_lr
        #    counter_character += 1

        #背景描写
        draw_background(adjust_x, adjust_z, counter)

        #ペア表示オン
        if doubles == 1:
            character[counter_character].on(1)
            counter_character += 1

        #ネット表示オン
        character[counter_character].on(2)
        counter_character += 1

        #蛙ではなくてボール表示オン
        character[counter_character].on(3)
        counter_character += 1

        #鳥ではなくて相手プレーや表示オン
        character[counter_character].on(4)
        counter_character += 1

        #鳥ではなくて相手プレー2や表示オン
        if doubles == 1 :
            character[counter_character].on(5)
            counter_character += 1

        #キャラクター描写
        character_copy = character
        for i in range(1, len(character_copy)):
            if character_copy[i].status > 0:
                draw_character(character_copy[i].image, character_copy[i].x, character_copy[i].z, character_copy[i].y,
                               character_copy[i].width, character_copy[i].height, adjust_x, adjust_z)

        #スコア表示
        score_indication(seta,setb,gamea,gameb,pointa,pointb)

        #クレジット表示
        image = sysfont.render(
            "© 2020 KAZUOU", True, (255, 255, 255))
        SURFACE.blit(image, (125,  270))

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
                gameover_flag = 0

            #画面再描写(フルスクリーン対応)
            SURFACE.blit(filler, (0,0))

            #タイトル3D表示
            title_y -= 5 if title_y > 0 else 0
            draw_character(image_title, 0, -52, title_y, 350, 103, adjust_x, adjust_z)
            draw_character(image_start, 0, 52, title_y, 300, 35, adjust_x, adjust_z)

            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)

        #変数初期設定(ゲーム)
        seta = 2
        setb = 1
        gamea = 5
        gameb = 3
        pointa = 15
        pointb = 0
        score = 0
        damage = 0
        counter = 0

        #BGM再生
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()

        #ループ2(ゲームメインループ)
        while gameover_flag == 0:

            #ラウンドデータ読み込み
            if counter % 300 == 0 and counter < 6000:
                    rate_stopper, rate_frog, rate_bird = round_data[int(counter/300)]

            #カウンター
            if character[0].status < 200 and counter < 6000:
                counter += 1
                score += 10

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

            #キー入力判定＆とび職人移動
            if character[0].status < 200 and counter <= 5970:
                pressed = pygame.key.get_pressed()
                if pressed[K_LEFT] and character[0].x > -280:
                    character[0].x -= 20
                if pressed[K_RIGHT] and character[0].x < 280:
                    character[0].x += 20
                if pressed[K_UP] and character[0].y < 35:
                    character[0].y += 1
                if pressed[K_DOWN] and character[0].y > 0:
                    character[0].y -= 1
                if pressed[K_SPACE] and character[0].jump_status == 1:
                    sound_jump.play()
                    character[0].jump_status = 2
                    character[0].vz = -26
            if character[0].jump_status == 2:
                character[0].z += character[0].vz
                character[0].vz += 2
                if character[0].z >= 100:
                    character[0].z = 100
                    character[0].jump_status = 1
            adjust_x = character[0].x / 30
            adjust_z = character[0].z / 20
            if counter > 5970:
                if character[0].x > 0:
                    character[0].x -= 10
                elif character[0].x < 0:
                    character[0].x += 10

            #キャラクター表示オン
            if character[0].status < 200:

                #樹木表示オン
                #if counter % 20 == 0:
                #    if character[counter_character].status == 0:
                #        character[counter_character].on(1, tree_lr * 280)
                #        tree_lr = -tree_lr
                #    counter_character += 1
                #    if counter_character >= len(character):
                #        counter_character = 1

                #ストッパー表示オン
                #if rate_stopper > 0 and random.randint(0, rate_stopper) == 0:
                #    if character[counter_character].status == 0:
                #        character[counter_character].on(2)
                #    counter_character += 1
                #    if counter_character >= len(character):
                #        counter_character = 1

                #蛙表示オン
                #if rate_frog > 0 and random.randint(0, rate_frog) == 0:
                #    if character[counter_character].status == 0:
                #        character[counter_character].on(3)
                #    counter_character += 1
                #    if counter_character >= len(character):
                #        counter_character = 1

                #鳥表示オン
                #if rate_bird > 0 and random.randint(0, rate_bird) == 0:
                #    if character[counter_character].status == 0:
                #        character[counter_character].on(4)
                #    counter_character += 1
                #    if counter_character >= len(character):
                #        counter_character = 1

                #おむすび表示オン
                if counter > 300 and counter < 5900 and counter % 600 == 150:
                    if character[counter_character].status == 0:
                        character[counter_character].on(10)
                    counter_character += 1
                    if counter_character >= len(character):
                        counter_character = 1

                #家表示オン
                if counter == 5802:
                    character[counter_character].on(20)
                    if counter_character >= len(character):
                        counter_character = 1

            #背景描写
            draw_background(adjust_x, adjust_z, counter)

            #キャラクター移動
            if character[0].status < 200 and counter < 6000:
                for i in range(1, len(character)):
                    if character[i].status > 0:
                        a, b = character[i].move(character[0].x, character[0].z, character[0].y, character[0].status)
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
                    gameover_flag = 2
            elif character[0].status >= 10:
                character[0].blink()

            #フィニッシュ処理
            if counter == 6000:
                character[0].finish()
                score += 30000
                gameover_flag = 1
                sound_finish.play()

            #キャラクター描写順番調整(キャラクターオブジェクトをコピーしてy座標を降順で並び替え)
            character_copy = character
            #character_copy[0].y = -100 #とび職人を強制的に一番手前に
            character_copy = sorted(character_copy, key=lambda i: i.y, reverse=True)
            #character_copy[len(character_copy)-1].y = 0 #とび職人のy座標を0に戻す

            #キャラクター描写
            for i in range(len(character_copy)):
                if character_copy[i].status > 0:
                    draw_character(character_copy[i].image, character_copy[i].x, character_copy[i].z, character_copy[i].y,
                                   character_copy[i].width, character_copy[i].height, adjust_x, adjust_z)

            #ポイント表示
            if counter_point > 0:
                counter_point += 1
                a, b = location_in_view(point_x, 100, 0, 0, 0, adjust_x, adjust_z)
                image = sysfont.render(
                    "{:^10}".format("1000 x " + str(combo)), True, (255, 0, 0))
                SURFACE.blit(image, (a, b))
                if counter_point > 30:
                    counter_point = 0

            #スコア表示
            if score > best_score:
                best_score = score
            score_indication(seta,setb,gamea,gameb,pointa,pointb)

            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)

            #BGM再生確認&リピート
            if pygame.mixer.music.get_busy() == 0:
                pygame.mixer.music.play()

        #仕事場到着またはゲームオーバー表示
        if gameover_flag == 1:
            SURFACE.blit(image_final_bonus, (25, 70))
        else:
            SURFACE.blit(image_gameover, (50, 129))

        #画面コピー
        filler = SURFACE.copy()

        #変数初期設定(ゲームオーバー)
        a = 0
        counter2 = 0

        #ループ3(ゲームオーバー)
        while gameover_flag <= 2:

            #カウンター(ゲームオーバー処理用)
            counter2 += 1
            if counter2 >= 210:
                gameover_flag = 3

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
                        screen = pygame.display.set_mode((400, 300), FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((400, 300), 0)

            #キー入力判定
            pressed = pygame.key.get_pressed()
            if pressed[K_SPACE] == 0 and a == 0:
                a = 1
            elif pressed[K_SPACE] and a == 1:
                a = 2
            elif pressed[K_SPACE] == 0 and a == 2:
                a = 0
                gameover_flag = 3

            #画面再描写(フルスクリーン対応)
            SURFACE.blit(filler, (0,0))

            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
