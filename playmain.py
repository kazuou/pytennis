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