# draw_module.py
import pygame

def draw_court(ctx: 'DrawContext', lines):
    ctx.screen.fill(ctx.GREEN)
    pygame.draw.rect(ctx.screen, ctx.BLUE, ctx.court_rect)
    # 省略: 他のrectやlineもctx.screen, ctx.で呼び出し

    for start, end, width in lines:
        start_screen = (
            start[0] * ctx.scale + ctx.field_width // 2,
            start[1] * ctx.scale + ctx.center_y,
        )
        end_screen = (
            end[0] * ctx.scale + ctx.field_width // 2,
            end[1] * ctx.scale + ctx.center_y,
        )
        width_screen = round(width * ctx.scale)
        pygame.draw.line(ctx.screen, ctx.WHITE, start_screen, end_screen, width_screen)

def draw_slider(ctx: 'DrawContext', x, y, value, min_val, max_val, label, slider_length, slider_height):
    pygame.draw.rect(ctx.screen, ctx.GRAY, (x, y, slider_length, slider_height))
    ratio = (value - min_val) / (max_val - min_val)
    knob_x = int(x + max(0.0, min(1.0, ratio)) * slider_length)
    pygame.draw.rect(ctx.screen, ctx.RED, (knob_x - 5, y - 5, 10, slider_height + 10))
    font = pygame.font.SysFont(ctx.fontname, 16)
    text = font.render(f"{label}: {value:.1f}", True, ctx.BLACK)
    ctx.screen.blit(text, (x + slider_length + 10, y - 5))

# 他の描画系関数も同様にctxを渡して、色・位置・フォント取得をctx経由にする