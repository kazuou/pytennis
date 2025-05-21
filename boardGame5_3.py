import pygame
import math
import copy
import random
import threading

ai_thinking = False
ai_result = None


# Minimaxで必要な関数
# is_terminal(state) 相手がボールを取れなければ勝ち
# evaluate_terminal(state)　勝ち+1,負け-1,引き分け0
# generate_legal_moves(state, player) 取れる位置や次の投げ方、移動先の組み合わせを列挙
# apply_move(state, move)　#新しい状態を作成
# minimax(state, depth, is_max_player) #AIが最善手を探索
# evaluate(state) 状態の善し悪しの判定
# minimax(state,depth,maximizing_player)

# 定数
WIDTH, HEIGHT = 800, 400
COURT_WIDTH = 100
COURT_HEIGHT = 50
SCALE_X = WIDTH / COURT_WIDTH
SCALE_Y = HEIGHT / COURT_HEIGHT
MAX_DEPTH = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()


# 状態クラス
class GameState:
    def __init__(self, ball_pos, ball_vel, player1_pos, player2_pos, turn):
        self.ball_pos = ball_pos
        self.ball_vel = ball_vel  # ボールの速度ベクトル
        self.player1_pos = player1_pos
        self.player2_pos = player2_pos
        self.turn = turn


def ai_worker(state):
    global ai_result, ai_thinking
    ai_result = minimax(state, MAX_DEPTH, True)
    ai_thinking = False


# アクション生成
def generate_possible_actions(state, player):
    actions = []
    for angle in range(0, 360, 45):
        for speed in [10, 15, 20]:
            vx = speed * math.cos(math.radians(angle))
            vy = speed * math.sin(math.radians(angle))
            actions.append((vx, vy))
    return actions


# アクション適用
def apply_action(state, action, player):
    new_state = copy.deepcopy(state)
    new_state.ball_vel = action
    new_state.turn = 2 if player == 1 else 4
    return new_state


# ボールの移動
def simulate_ball_motion(state):
    x, y = state.ball_pos
    vx, vy = state.ball_vel
    return (x + vx * 0.1, y + vy * 0.1)


# ゲーム終了判定
def is_terminal(state):
    x, y = state.ball_pos
    return not (0 <= x <= COURT_WIDTH and 0 <= y <= COURT_HEIGHT)


# 評価関数
def evaluate(state):
    if is_terminal(state):
        # ターンによって、誰がボールを取れなかったか判定
        if state.turn in [3, 4]:
            # プレイヤー2が取れなかった → AIの負け
            return -1e6
        else:
            # プレイヤー1が取れなかった → AIの勝ち
            return +1e6
    # 通常時は相手プレーヤーからボールが遠いほどスコアが高い。
    if state.turn in [3, 4]:
        px, py = state.player1_pos
    else:
        px, py = state.player2_pos
    bx, by = state.ball_pos
    return math.hypot(px - bx, py - by)


# Minimax
def minimax(state, depth, maximizing):
    if depth == 0 or is_terminal(state):
        return evaluate(state), None

    if maximizing:  # AIプレーヤ
        max_eval = float("-inf")  # 最小の値
        best_action = None
        for action in generate_possible_actions(state, 2):
            # generate_possine_action関数が出してきて、使えるアクション最大24通りをすべてやる。
            next_state = apply_action(state, action, 2)
            next_state.ball_pos = simulate_ball_motion(next_state)
            eval, _ = minimax(next_state, depth - 1, False)  # _は捨てている
            if eval > max_eval:
                max_eval = eval
                best_action = action
        return max_eval, best_action
    else:  # プレーヤー
        min_eval = float("inf")  # 最大の値
        best_action = None
        for action in generate_possible_actions(state, 1):
            next_state = apply_action(state, action, 1)
            next_state.ball_pos = simulate_ball_motion(next_state)
            eval, _ = minimax(next_state, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
        return min_eval, best_action


# 座標変換
def to_screen(pos):
    return int(pos[0] * SCALE_X), int(pos[1] * SCALE_Y)


# 描画
def draw(state):
    screen.fill((30, 130, 70))
    pygame.draw.circle(screen, (255, 255, 255), to_screen(state.ball_pos), 8)
    pygame.draw.rect(screen, (255, 100, 100), (*to_screen(state.player1_pos), 10, 10))
    pygame.draw.rect(screen, (100, 100, 255), (*to_screen(state.player2_pos), 10, 10))
    msg = font.render(f"Turn: {state.turn}", True, (255, 255, 255))
    screen.blit(msg, (10, 10))
    pygame.display.flip()


# メインループ
def main():
    global ai_result
    global ai_thinking
    state = GameState(
        ball_pos=(50, 25),
        ball_vel=(0, 0),
        player1_pos=(10, 25),
        player2_pos=(90, 25),
        turn=1,
    )

    running = True
    while running:
        clock.tick(30)
        draw(state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 終了条件
        if is_terminal(state):
            print("ゲーム終了: ボールがコート外に出た")
            break

        # AIの思考に入る
        if state.turn == 3 and not ai_thinking:
            print("AI 思考中...")
            ai_thinking = True
            threading.Thread(target=ai_worker, args=(copy.deepcopy(state),)).start()

        # AIの思考から出る
        if state.turn == 3 and ai_result:
            _, best_action = ai_result
            state = apply_action(state, best_action, player=2)
            ai_result = None

        # プレイヤー1 打つ（マウスクリックで方向指定）
        if state.turn == 1:
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                mx, my = pygame.mouse.get_pos()
                target = (mx / SCALE_X, my / SCALE_Y)
                dx = target[0] - state.player1_pos[0]
                dy = target[1] - state.player1_pos[1]
                dist = math.hypot(dx, dy)
                if dist > 0:
                    vx = 15 * dx / dist
                    vy = 15 * dy / dist
                    state = apply_action(state, (vx, vy), 1)

        # プレイヤー1 移動
        elif state.turn == 2:
            mx, my = pygame.mouse.get_pos()
            state.player1_pos = (mx / SCALE_X, my / SCALE_Y)
            state.ball_pos = simulate_ball_motion(state)
            state.turn = 3

        # プレイヤー2（AI）打つ
        elif state.turn == 3:
            _, action = minimax(state, MAX_DEPTH, True)
            if action:
                print("AI 打つ:", action)
                state = apply_action(state, action, 2)
            else:
                state.turn = 4

        # プレイヤー2 移動（ボールへ瞬間移動）
        elif state.turn == 4:
            state.ball_pos = simulate_ball_motion(state)
            state.player2_pos = state.ball_pos
            state.turn = 1

    pygame.quit()


if __name__ == "__main__":
    main()
