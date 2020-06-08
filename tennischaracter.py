""" tennischaracter.py """
import pygame
import draw
import random


doubles = 0
game_flag = 0

counter = 0
score = 0
point_x = 0

damage = 0
counter_point = 0
combo = 0
seta = 2
setb = 2
gamea = 10
gameb = 10
pointa = 0
pointb = 0

class Character:
    """キャラクターーオブジェクト"""
    def __init__(self):
        self.status = 0
        self.jump_status = 0
        self.image_type = 0 #
        self.x = 0
        self.y = 0
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.rotx = 0
        self.roty = 0
        self.rotz = 0
        self.width = 0
        self.height = 0
        self.mag = 1 #サイズと表示の倍率(ボールを大きく見せるため)
        self.color = (255,255,255)
        self.image_man_bright = pygame.image.load("man1_1.png")
        self.image_man_failed = pygame.image.load("man1_1.png")
        self.image_man_smile = pygame.image.load("man1_1.png")

        self.image_man1_1 = pygame.image.load("man1_1.png")
        self.image_man1 = pygame.image.load("man1.png")
        self.image_man2 = pygame.image.load("man1.png")
        self.image_man3 = pygame.image.load("man3.png")
        self.image_man4 = pygame.image.load("man4.png")
        self.image_ball = pygame.image.load("TennisBall.png")

        self.image_net = pygame.image.load("net.png")
        self.image_omusubi = pygame.image.load("omusubi.gif")
        self.image_nipponichi = pygame.image.load("nipponichi.png")

    #表示オン
    def on(self, image_type,game_flag):
        self.status = 1
        self.image_type = image_type
        if self.image_type == 0: #私
            self.jump_status = 1
            self.x = -200
            self.y = -10
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.width = 100
            self.height = 170
            self.image = self.image_man1_1
        if self.image_type == 1: #ペア
            self.x = -200
            self.y = draw.servieline1
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.color = (0,0,0)
            self.width = 100
            self.height = 170
            self.image = self.image_man1
        if self.image_type == 2: #ネット
            self.x = 0
            self.y = draw.netline
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            if tc.doubles == 0:
                #シングルスネット
                self.width = 411.5+411.5+91.4+91.4
            else:
                #ダブルスネット
                self.width =  548+548+91.4+91.4

            self.height = 91.4
            self.image = self.image_net
        if self.image_type == 3: #ボール
            self.x = -200
            self.y = draw.baseline2
            self.z = 100
            self.vx = 0
            self.vy = -70
            self.vz = +18.0
            self.width = 30
            self.height = 30
            self.color = (255,255,0)
            self.mag = 30
            self.image = self.image_ball
        if self.image_type == 4: #相手プレーヤー
            self.x = -200
            self.y = draw.baseline2
            self.z = 0
            self.vx = 0
            self.vy = -2
            self.vz = (random.randint(0, 1) * 2 - 1) * 5
            self.width = 100
            self.height = 100
            self.color = (26,97,167)
            self.image = self.image_man3
        if self.image_type == 5: #相手プレーヤー2
            self.x = 200
            self.y = draw.servieline2-200
            self.z = 0
            self.vx = 0
            self.vy = -2
            self.vz = (random.randint(0, 1) * 2 - 1) * 5
            self.width = 100
            self.height = 100
            self.color =(255,0,0)
            self.image = self.image_man4
        if self.image_type == 10: #おむすび
            self.x = random.randint(-500, 500)
            self.y = draw.baseline2
            self.z = 0
            self.vx = 0
            self.vy = -50
            self.vz = +20
            self.width = 60
            self.height = 40
            self.image = self.image_omusubi
        if self.image_type == 11: #オープニングメッセージ1
            self.x = 0
            self.y = 1500
            self.z = 250
            self.vx = 0
            self.vy = -50
            self.vz = 0
            self.width = 700
            self.height = 200
            self.image = draw.image_title
        if self.image_type == 12: #オープニングメッセージ2
            self.x = 0
            self.y = draw.baseline2
            self.z = 70
            self.vx = 0
            self.vy = -50
            self.vz = 0
            self.width = 600
            self.height = 70
            self.image = draw.image_start

        if self.image_type == 20: #トロフィ
            self.x = 0
            self.y = draw.baseline2
            self.z = 0
            self.vx = 0
            self.vy = -10
            self.vz = 0
            self.width = 360
            self.height = 310
            self.image = self.image_nipponichi

    def off(self):
        self.status = 0

    #移動
    def move(self, x, y, z, status):
        if self.image_type == 20 : #トロファ
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz

        elif self.image_type == 10: #おむすび
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
            self.vz -= 1
            if self.z < 0 :
                self.vy = -20
                self.vz = -self.vz *0.1
                self.z = 0
        elif self.image_type == 11 : #オープニングメッセージ1
            selfy_old = self.y
            self.y += self.vy
            if self.y < 0:
                self.vy = 0
                self.y = 0
        elif self.image_type == 12: #オープニングメッセージ2
            selfy_old = self.y
            self.y += self.vy
            if self.y < 0:
                self.vy = 0
                self.y = 0

        elif self.image_type == 3: #ボール
            self.status += 1
            self.x += self.vx
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
            self.vz -= 1
            self.vy = self.vy * 0.98
            if self.z < 0 :
                self.vz = -self.vz *0.7
                self.z = 0
            if (self.y < y and self.vy < 0):
                self.vy = 80
                self.vz = +20
            if (self.y > draw.baseline2 and self.vy > 0):
                self.vy = -80
                self.vz = +20
#            if self.y  character[1].y and self.vz > 0
#                self.vz = -80
#                self.vz = -20
        elif (self.image_type == 4 or self.image_type == 5): #相手プレーヤー
            self.x += self.vx
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
            if self.x > x:
                self.vx -= 1
            elif self.x < x:
                self.vx += 1
            if (self.x >= 300 and self.vx > 0) or (self.x <= 10 and self.vx < 0):
                self.vx = int(self.vx / 2)
            if (self.x >= 10 and self.vx > 0) or (self.x <= -300 and self.vx < 0):
                self.vx = int(self.vx / 2)

            if self.z > +110:
                self.z = +110
                self.vz = -self.vz
            elif self.z < 0:
                self.z = 0
                self.vz = -self.vz
            if self.y <= draw.netline + 10 and self.vy < 0 :
                self.vy = -self.vy
                self.y = draw.netline + 10
            if self.y >= draw.baseline2 and self.vy > 0:
                self.vy = -self.vy
                self.y = draw.baseline2

        #スクリーンより前面(y < 0)の場合には消去
        if self.y < draw.fieldy1 - 20:
            self.status = 0
            self.y = 0
            if self.image_type == 10:
                return(3, self.x)
            else:
                return(0, self.x)

        if status < 200 and self.image_type == 10: #おむすび取得
            if self.status > 0 and self.y <= y and selfy_old > y and abs(self.x - x) < self.width / 2  + 100 and abs(self.z - z) < self.height / 2 + 100:
                self.status = 0
                self.y = 0
                return(2, self.x)
            else:
                return(0, self.x)
        else:
            return(0, self.x)


    def moveball(self,checkcort):#ボールの移動
        #時速はMAX150km(早いプロ)
        #90km/h
        #初心者60km/h
        #重力加速度9.8m/s/s
        #xv,yv,zv共1=30cm/s=0.3m/s=1.08km/h
        #20=600cm/s=6m/s=3.6*6=21.6km/h
        #100=3000cm/s=30m/S=108km/h
        cx1,cy1,cx2,cy2 = checkcort #このボールのワンバンドすべきコート
        #ボールの中心点で判断するので+3.35広げてある。
        if self.z + slef.vz >0: #ボールがz=0を通過していない時
            self.x += self.vx
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
            self.vz -= 1
            self.vy = self.vy * 0.98
        else:   #ワンバウンド
            #着地点を判断するため、x,yはz=0を通過する点に
            self.x += self.vx * self.z/(-self.vz) #self.vzがマイナスなので
            self.y += self.y - self.vy * self.z/(-self.vz)

            self.vz = -self.vz *0.7
            self.z = 0
            if self.status == 3:
                self.status = 5
                return(5)   #打ったプレーヤーのポイント
            elif self.status == 2:
                if(self.x < cx1 or self.x > cx2 or self.y < cy1 or self.y > cy2):
                    self.status = 4
                    return(4)   #打ったプレーヤーのミス
                else:
                    self.status = 3
                                #インプレー続行
        return(self.status)


    #得点
    def finish(self):
        if self.image_type == 0:
            self.image = self.image_man_smile
    #失点
    def failure(self):
        if self.image_type == 0:
            self.image = self.image_man_failed
            self.status += 1
            if self.status >= 260:
                self.status = 10
                self.image = self.image_man

    #鼓舞する(点滅表示)
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
