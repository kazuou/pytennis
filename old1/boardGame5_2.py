import math
import copy
import random

# =========================
# 定数
# =========================
MAX_DEPTH = 2  # Minimaxの探索深さ
COURT_WIDTH = 100
COURT_HEIGHT = 50


# =========================
# 状態クラス
# =========================
class GameState:
    def __init__(self, ball_pos, ball_vel, player1_pos, player2_pos, turn):
        self.ball_pos = ball_pos  # (x, y)
        self.ball_vel = ball_vel  # (vx, vy)
        self.player1_pos = player1_pos
        self.player2_pos = player2_pos
        self.turn = turn  # 1: プレイヤー1が打つ, 2: プレイヤー1移動, 3: プレイヤー2が打つ, 4: プレイヤー2移動


# =========================
# ゲームロジック
# =========================
def generate_possible_actions(state, player):
    actions = []
    for angle in range(0, 360, 45):
        for speed in [10, 15, 20]:
            vx = speed * math.cos(math.radians(angle))
            vy = speed * math.sin(math.radians(angle))
            actions.append((vx, vy))
    return actions


def apply_action(state, action, player):
    new_state = copy.deepcopy(state)
    new_state.ball_vel = action
    new_state.turn = 2 if player == 1 else 4
    return new_state


def simulate_ball_motion(state):
    x, y = state.ball_pos
    vx, vy = state.ball_vel
    new_x = x + vx
    new_y = y + vy
    return (new_x, new_y)


def is_terminal(state):
    x, y = state.ball_pos
    return not (0 <= x <= COURT_WIDTH and 0 <= y <= COURT_HEIGHT)


def evaluate(state):
    # 相手プレイヤーからボールが遠いほどスコアが高い
    if state.turn in [3, 4]:
        # AIのターン → 相手はプレイヤー1
        px, py = state.player1_pos
    else:
        px, py = state.player2_pos
    bx, by = state.ball_pos
    distance = math.hypot(px - bx, py - by)
    return distance  # 大きいほど良い


def minimax(state, depth, maximizing_player):
    if depth == 0 or is_terminal(state):
        return evaluate(state), None

    if maximizing_player:
        max_eval = float("-inf")
        best_action = None
        for action in generate_possible_actions(state, player=2):
            next_state = apply_action(state, action, player=2)
            next_state.ball_pos = simulate_ball_motion(next_state)
            eval, _ = minimax(next_state, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_action = action
        return max_eval, best_action
    else:
        min_eval = float("inf")
        best_action = None
        for action in generate_possible_actions(state, player=1):
            next_state = apply_action(state, action, player=1)
            next_state.ball_pos = simulate_ball_motion(next_state)
            eval, _ = minimax(next_state, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
        return min_eval, best_action


# =========================
# メインループ
# =========================
def main():
    # 初期状態
    state = GameState(
        ball_pos=(50, 25),
        ball_vel=(0, 0),
        player1_pos=(10, 25),
        player2_pos=(90, 25),
        turn=1,
    )

    while True:
        print(f"\n=== ターン: {state.turn} ===")
        print(f"ボール位置: {state.ball_pos}")
        print(f"Player1位置: {state.player1_pos}, Player2位置: {state.player2_pos}")

        if is_terminal(state):
            print("ボールがコート外に出ました。ゲーム終了。")
            break

        # プレイヤー1が打つ
        if state.turn == 1:
            try:
                angle = float(input("角度（0〜360度）を入力: "))
                speed = float(input("スピード（例: 10〜20）を入力: "))
                vx = speed * math.cos(math.radians(angle))
                vy = speed * math.sin(math.radians(angle))
                state = apply_action(state, (vx, vy), player=1)
            except:
                print("入力エラー。ランダムなボールで代用。")
                state = apply_action(
                    state, random.choice(generate_possible_actions(state, 1)), 1
                )

        # プレイヤー1が移動
        elif state.turn == 2:
            try:
                x = float(input("Player1の移動先X: "))
                y = float(input("Player1の移動先Y: "))
                state.player1_pos = (x, y)
            except:
                print("入力エラー。位置変更なし。")
            state.ball_pos = simulate_ball_motion(state)
            state.turn = 3

        # プレイヤー2が打つ（AI）
        elif state.turn == 3:
            print("AIが考え中...")
            _, best_action = minimax(state, MAX_DEPTH, True)
            print("AIがボールを打ちました。", best_action)
            state = apply_action(state, best_action, player=2)

        # プレイヤー2が移動（ランダム）
        elif state.turn == 4:
            bx, by = simulate_ball_motion(state)
            state.ball_pos = (bx, by)
            state.player2_pos = (bx, by)  # 簡略化：ボールの位置へ瞬間移動
            state.turn = 1


# 実行
if __name__ == "__main__":
    main()
