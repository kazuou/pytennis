import pygame
from draw_context import DrawContext
import draw_module

# ...（他設定）...
ctx = DrawContext(
    screen=screen,
    scale=scale,
    field_width=field_width,
    field_height=field_height,
    court_rect=court_rect,
    center_x=center_x,
    center_y=center_y,
    fontname=fontname,
)

# ゲームループ内
draw_module.draw_court(ctx, lines)
draw_module.draw_slider(ctx, slider_x, z_slider_y, z_slider_val, BALL_VZMIN, BALL_VZMAX, "Z速度", slider_length, slider_height)