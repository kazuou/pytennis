# draw_context.py
import pygame

class DrawContext:
    def __init__(self,
                 screen,
                 scale,
                 field_width, field_height,
                 court_rect,
                 center_x, center_y,
                 fontname,
                 ):
        self.screen = screen
        self.scale = scale
        self.field_width = field_width
        self.field_height = field_height
        self.court_rect = court_rect
        self.center_x = center_x
        self.center_y = center_y
        self.fontname = fontname

        # 色定義
        self.GREEN = (0, 128, 0)
        self.BLUE = (0, 102, 204)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GRAY2 = (150, 150, 150)
        self.YELLOW = (255, 255, 0)