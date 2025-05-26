
def is_terminal(state)  # 相手がボールを取れなければTrue(勝敗が決まった)

def evaluate_terminal(state)  # 勝ち+1 負け-1
def generate_legal_moves(state, player):  # 取れる位置や次の投げ方、移動先を列挙
def apply_move(state, move):  # 新しい状態を作成
    """アクションを適用して新しい状態を作成"""
    new_state = copy.deepcopy(state)
    if player == 1:
        new_state.ball_vel = action
        new_state.turn = 2  # 移動ターンへ
    else:
        new_state.ball_vel = action
        new_state.turn = 4
    return new_state
  
def minimax(state, depth, is_max_player):  # AIが最善手を探索

def simulate_ball_motion(state):
    """ボールの飛びとバウンドを簡略にシミュレート（Z方向無視の例）"""
    x, y, z = state.ball_pos
    vx, vy, vz = state.ball_vel
    return (x + vx, y + vy, z + vz)
