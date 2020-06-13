""" tennis.py """

import math
import pygame
import random
import sys
import os
from pygame.locals import *

import tennischaracter as tc
import opening
import playgame
import gameset
import draw

print(os.getcwd())
#SURFACE = pygame.display.set_mode((1200, 600))




#BGM
pygame.mixer.music.load("media/bgm.wav")

def main():
    """ メインルーチン """
    #変数初期設定(基本)
    a, b, c, d = 0, 0, 0, 0
    tc.character = [tc.Character() for i in range(20)]
    tc.character_copy = []
    fullscreen_flag = 0

    #マウスカーソル非表示
    pygame.mouse.set_visible(True)

    while True:
        opening.opening()

        playgame.playgame()

        gameset.gameset()

if __name__ == '__main__':
    main()
