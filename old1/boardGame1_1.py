import numpy as np

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
BALL = 3
NET = -1

class Game:
    def __init__(self, size=7):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.players = [(0, size // 2), (size - 1, size // 2)]  # プレイヤー1とプレイヤー2の初期位置
        self.ball = (size // 2, size // 2)  # ボールの初期位置
        self.board[self.players[0]] = PLAYER1
        self.board[self.players[1]] = PLAYER2
        self.board[self.ball] = BALL
        for i in range(size):
            self.board[size // 2, i] = NET  # ネットの位置

    def draw_board(self):
        for row in self.board:
            print(' '.join(['.' if x == EMPTY else '#' if x == NET else '1' if x == PLAYER1 else '2' if x == PLAYER2 else 'O' for x in row]))
        print()

    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x, y] == EMPTY

    def move_player(self, player_index, new_pos, ball_speed):
        current_pos = self.players[player_index]
        move_distance = self.calculate_move_distance(ball_speed)
        if self.is_valid_move(new_pos) and self.manhattan_distance(current_pos, new_pos) <= move_distance:
            self.board[current_pos] = EMPTY
            self.players[player_index] = new_pos
            self.board[new_pos] = PLAYER1 if player_index == 0 else PLAYER2

    def throw_ball(self, player_index, target_pos, ball_speed):
        if self.is_valid_move(target_pos) and self.board[target_pos] != NET:
            self.board[self.ball] = EMPTY
            self.ball = target_pos
            self.board[target_pos] = BALL

    def calculate_move_distance(self, ball_speed):
        max_distance = self.size // 2  # 最大移動距離の制限（例：ボードの半分）
        return max(1, max_distance - ball_speed)  # 最小は必ず1に

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def evaluate(self, board, players, ball):
        player1_distance = self.manhattan_distance(players[0], ball)
        player2_distance = self.manhattan_distance(players[1], ball)
        return player2_distance - player1_distance

    def minimax(self, depth, is_maximizing_player, board, players, ball):
        if depth == 0:
            return self.evaluate(board, players, ball)

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(1, board, players, ball):
                cloned_board, cloned_players, cloned_ball = self.clone_state(board, players, ball)
                self.move_player_in_cloned_state(1, move, ball_speed=1, cloned_board=cloned_board, cloned_players=cloned_players)
                eval = self.minimax(depth - 1, False, cloned_board, cloned_players, cloned_ball)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(0, board, players, ball):
                cloned_board, cloned_players, cloned_ball = self.clone_state(board, players, ball)
                self.move_player_in_cloned_state(0, move, ball_speed=1, cloned_board=cloned_board, cloned_players=cloned_players)
                eval = self.minimax(depth - 1, True, cloned_board, cloned_players, cloned_ball)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_possible_moves(self, player_index, board, players, ball):
        x, y = players[player_index]
        possible_moves = [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
        valid_moves = [move for move in possible_moves if self.is_valid_move(move)]
        return valid_moves

    def best_move(self, player_index, depth=3):
        best_move = None
        best_throw = None
        best_val = float('-inf') if player_index == 1 else float('inf')
        for ball_speed in range(1, 4):  # 速度をいくつかの値で試す
            for move in self.get_possible_moves(player_index, self.board, self.players, self.ball):
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        throw_pos = (move[0] + dx, move[1] + dy)
                        if self.is_valid_move(throw_pos) and self.board[throw_pos] != NET:
                            cloned_board, cloned_players, cloned_ball = self.clone_state(self.board, self.players, self.ball)
                            self.move_player_in_cloned_state(player_index, move, ball_speed, cloned_board, cloned_players)
                            self.throw_ball_in_cloned_state(player_index, throw_pos, ball_speed, cloned_board, cloned_players, cloned_ball)
                            move_val = self.minimax(depth, player_index == 0, cloned_board, cloned_players, cloned_ball)
                            if (player_index == 1 and move_val > best_val) or (player_index == 0 and move_val < best_val):
                                best_val = move_val
                                best_move = move
                                best_throw = throw_pos
        return best_move, best_throw, ball_speed

    def clone_state(self, board, players, ball):
        return board.copy(), players.copy(), ball

    def move_player_in_cloned_state(self, player_index, new_pos, ball_speed, cloned_board, cloned_players):
        current_pos = cloned_players[player_index]
        cloned_board[current_pos] = EMPTY
        cloned_players[player_index] = new_pos
        cloned_board[new_pos] = PLAYER1 if player_index == 0 else PLAYER2

    def throw_ball_in_cloned_state(self, player_index, target_pos, ball_speed, cloned_board, cloned_players, cloned_ball):
        cloned_board[cloned_ball] = EMPTY
        cloned_ball = target_pos
        cloned_board[target_pos] = BALL

def main():
    game = Game()
    game.draw_board()

    while True:
        # プレイヤー1のターン
        print("\nPlayer 1's turn (Human):")
        move = input("Enter your move (format: x y): ").split()
        move = int(move[0]), int(move[1])
        throw = input("Enter throw target (format: x y): ").split()
        throw = int(throw[0]), int(throw[1])
        ball_speed = int(input("Enter ball speed (1, 2, or 3): "))
        game.move_player(0, move, ball_speed)
        game.throw_ball(0, throw, ball_speed)
        game.draw_board()

        # プレイヤー2のターン（コンピュータ）
        print("\nPlayer 2's turn (AI):")
        move, throw, ball_speed = game.best_move(1)
        game.move_player(1, move, ball_speed)
        game.throw_ball(1, throw, ball_speed)
        game.draw_board()

if __name__ == "__main__":
    main()