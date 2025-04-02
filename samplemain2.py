
# moduleObject3D.py
import pygame

class Object3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def move(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz

    def get_position(self):
        return self.x, self.y, self.z

    def draw(self, screen):
        # サブクラスでオーバーライドする
        pass

# modulePerson.py
from moduleObject3D import Object3D

class Person(Object3D):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.color = (255, 0, 0)  # 赤色

    def update(self, time):
        self.move(time * 0.1, 0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)

# moduleLeaf.py
from moduleObject3D import Object3D

class Leaf(Object3D):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.color = (0, 255, 0)  # 緑色

    def update(self, time):
        self.move(0, time * 0.1, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

# moduleGround.py
from moduleObject3D import Object3D

class Ground(Object3D):
    def __init__(self, x, y, z, width, height):
        super().__init__(x, y, z)
        self.width = width
        self.height = height
        self.color = (100, 100, 100)  # 灰色

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

# moduleScene.py
from modulePerson import Person
from moduleLeaf import Leaf
from moduleGround import Ground

class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, time):
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(time)

    def draw(self, screen):
        screen.fill((0, 0, 0))  # 画面を黒でクリア（背景）
        for obj in self.objects:
            obj.draw(screen)
        pygame.display.flip()

# main.py
import pygame
from moduleScene import Scene
from modulePerson import Person
from moduleLeaf import Leaf
from moduleGround import Ground

# Pygameを初期化
pygame.init()

# 画面サイズを設定
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('3D Scene with Moving Objects')

# シーンを作成
scene = Scene()

# オブジェクトを追加
ground = Ground(0, 550, 0, 800, 50)
scene.add_object(ground)

person = Person(100, 500, 0)
scene.add_object(person)

leaf = Leaf(200, 100, 0)
scene.add_object(leaf)

# メインループ
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 経過時間の算出
    time_elapsed = clock.get_time() / 1000  # 秒単位に変換

    # シーンの更新
    scene.update(time_elapsed)

    # シーンの描画
    scene.draw(screen)

    # フレームレートを設定
    clock.tick(30)

# Pygameを終了
pygame.quit()