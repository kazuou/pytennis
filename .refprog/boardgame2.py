import numpy as np

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
BALL = 3
NET = -1
MAX_BALL_SPEED = 3

class Game:
    def __init__(self, size=7):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.players = [(0, size // 2), (size - 1, size // 2)]  # プレイヤー1とプレイヤー2の初期位置
        self.ball = None
        self.board[self.players[0]] = PLAYER1
        self.board[self.players[1]] = PLAYER2
        for i in range(size):
            self.board[size // 2, i] = NET  # ネットの位置

    def draw_board(self):
        for row in self.board:
            print(' '.join(['.' if x == EMPTY else '#' if x == NET else '1' if x == PLAYER1 else '2' if x == PLAYER2 else 'O' for x in row]))
        print()

    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x, y] == EMPTY

    def move_player(self, player_index, new_pos):
        current_pos = self.players[player_index]
        if self.is_valid_move(new_pos):
            self.board[current_pos] = EMPTY
            self.players[player_index] = new_pos
            self.board[new_pos] = PLAYER1 if player_index == 0 else PLAYER2

    def throw_ball(self, player_index, target_pos):
        if self.is_valid_move(target_pos) and self.board[target_pos] != NET:
            self.ball = target_pos

    def calculate_move_distance(self, player_index, ball_speed):
        other_player_index = 1 - player_index
        distance_to_other_player = self.manhattan_distance(self.players[player_index], self.players[other_player_index])
        return distance_to_other_player / ball_speed

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def evaluate(self):
        if self.ball:
            player1_distance = self.manhattan_distance(self.players[0], self.ball)
            player2_distance = self.manhattan_distance(self.players[1], self.ball)
        else:
            player1_distance = player2_distance = 0
        return player2_distance - player1_distance

    def is_final_state(self):
        if self.ball is None:
            return False
        p1_distance = self.manhattan_distance(self.players[0], self.ball)
        p2_distance = self.manhattan_distance(self.players[1], self.ball)
        return p1_distance > self.calculate_move_distance(0, MAX_BALL_SPEED) and p2_distance > self.calculate_move_distance(1, MAX_BALL_SPEED)

    def minimax(self, depth, is_maximizing_player, ball_speed):
        if depth == 0 or self.is_final_state():
            return self.evaluate()

        player_index = 1 if is_maximizing_player else 0
        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(player_index, ball_speed):
                board_copy, players_copy, ball_copy = self.get_state()
                self.move_player(player_index, move)
                eval = self.minimax(depth - 1, False, ball_speed)
                self.set_state(board_copy, players_copy, ball_copy)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(player_index, ball_speed):
                board_copy, players_copy, ball_copy = self.get_state()
                self.move_player(player_index, move)
                eval = self.minimax(depth - 1, True, ball_speed)
                self.set_state(board_copy, players_copy, ball_copy)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_possible_moves(self, player_index, ball_speed):
        x, y = self.players[player_index]
        max_move_distance = self.calculate_move_distance(player_index, ball_speed)
        possible_moves = [(x + dx, y + dy) for dx in range(-int(max_move_distance), int(max_move_distance) + 1) for dy in range(-int(max_move_distance), int(max_move_distance) + 1)]
        possible_moves.append((x, y))  # 現在地に留まる動きも有効
        return [move for move in possible_moves if self.is_valid_move(move)]

    def best_move(self, player_index, depth=3):
        best_move = None
        best_throw = None
        best_val = float('-inf') if player_index == 1 else float('inf')
        for ball_speed in range(1, MAX_BALL_SPEED + 1):  # 速度をいくつかの値で試す
            for move in self.get_possible_moves(player_index, ball_speed):
                for dx in range(-ball_speed, ball_speed + 1):
                    for dy in range(-ball_speed, ball_speed + 1):
                        throw_pos = (move[0] + dx, move[1] + dy)
                        if self.is_valid_move(throw_pos) and self.board[throw_pos] != NET:
                            board_copy, players_copy, ball_copy = self.get_state()
                            self.move_player(player_index, move)
                            self.throw_ball(player_index, throw_pos)
                            move_val = self.minimax(depth, player_index == 0, ball_speed)
                            self.set_state(board_copy, players_copy, ball_copy)
                            if (player_index == 1 and move_val > best_val) or (player_index == 0 and move_val < best_val):
                                best_val = move_val
                                best_move = move
                                best_throw = throw_pos
        return best_move, best_throw, ball_speed

    def get_state(self):
        return self.board.copy(), self.players.copy(), self.ball

    def set_state(self, board, players, ball):
        self.board = board
        self.players = players
        self.ball = ball


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
        ball_speed = int(input("Enter ball speed (1 to {}): ".format(MAX_BALL_SPEED)))
        game.move_player(0, move)
        game.throw_ball(0, throw)
        game.draw_board()

        if game.is_final_state():
            print("Player 2 cannot catch the ball. Player 1 wins!")
            break

        # プレイヤー2のターン（コンピュータ）
        print("\nPlayer 2's turn (AI):")
        move, throw, ball_speed = game.best_move(1)
        game.move_player(1, move)
        game.throw_ball(1, throw)
        game.draw_board()

        if game.is_final_state():
            print("Player 1 cannot catch the ball. Player 2 wins!")
            break


if __name__ == "__main__":
    main()