import numpy as np
import math

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
BALL = 3
NET = -1
MAX_BALL_SPEED = 5
THROW_AREA_WIDTH = 9
THROW_AREA_HEIGHT = 13
BOARD_WIDTH = 18
BOARD_HEIGHT = 19

class Game:
    def __init__(self):
        self.board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.players = [(BOARD_HEIGHT - 1, BOARD_WIDTH // 2), (0, BOARD_WIDTH // 2)]  # プレイヤー1とプレイヤー2の初期位置
        self.ball = None
        self.ball_target = None
        self.ball_speed = 0
        self.ball_angle = 0
        self.ball_steps = 0
        self.board[self.players[0]] = PLAYER1
        self.board[self.players[1]] = PLAYER2
        for i in range(THROW_AREA_WIDTH):
            self.board[BOARD_HEIGHT // 2, (BOARD_WIDTH - THROW_AREA_WIDTH) // 2 + i] = NET  # ネットの位置

    def draw_board(self):
        symbols = {EMPTY: ' ', NET: '|', PLAYER1: 'A', PLAYER2: 'B', BALL: 'O'}
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                print(symbols[self.board[y, x]], end=' ')
            print()
        print()

    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH and self.board[x, y] == EMPTY

    def move_player(self, player_index, new_pos):
        current_pos = self.players[player_index]
        if self.is_valid_move(new_pos):
            self.board[current_pos] = EMPTY
            self.players[player_index] = new_pos
            self.board[new_pos] = PLAYER1 if player_index == 0 else PLAYER2

    def throw_ball(self, player_index, target_pos, speed, angle):
        if self.is_valid_throw(self.players[player_index], target_pos, speed, angle):
            self.ball_target = target_pos
            self.ball_speed = speed
            self.ball_angle = angle
            self.ball_steps = 0
            self.ball = self.players[player_index]  # ボールの初期位置

    def is_valid_throw(self, start_pos, target_pos, speed, angle):
        x0, y0 = start_pos
        x1, y1 = target_pos

        x_center = (BOARD_WIDTH - THROW_AREA_WIDTH) // 2
        y_center = (BOARD_HEIGHT - THROW_AREA_HEIGHT) // 2

        # 投げる範囲内にターゲットがいるか確認
        if not (y_center <= x1 < y_center + THROW_AREA_HEIGHT and x_center <= y1 < x_center + THROW_AREA_WIDTH):
            return False

        # Calculate horizontal and vertical distances
        dx = x1 - x0
        dy = y1 - y0

        if dx == 0 or dy == 0:
            return False

        # Convert angle to radians
        theta = math.radians(angle)

        # Velocity components
        vx = speed * math.cos(theta)
        vy = speed * math.sin(theta)

        t = dx / vx
        y = y0 + vy * t - 0.5 * 9.8 * t ** 2

        net_y = BOARD_HEIGHT // 2

        # Check if ball goes over the net
        if y > net_y:
            return False

        return 0 <= x1 < BOARD_HEIGHT and 0 <= y1 < BOARD_WIDTH and self.board[x1, y1] == EMPTY

    def calculate_max_move_distance(self, player_index, ball_speed):
        other_player_index = 1 - player_index
        distance_to_other_player = self.manhattan_distance(self.players[player_index], self.players[other_player_index])
        return distance_to_other_player // ball_speed

    def get_reachable_position(self, start_pos, target_pos, max_distance):
        if self.manhattan_distance(start_pos, target_pos) <= max_distance:
            return target_pos
        x1, y1 = start_pos
        x2, y2 = target_pos
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            step = max_distance if dx > 0 else -max_distance
            return x1 + step, y1
        else:
            step = max_distance if dy > 0 else -max_distance
            return x1, y1 + step

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def evaluate(self):
        if self.ball_target:
            player1_distance = self.manhattan_distance(self.players[0], self.ball_target)
            player2_distance = self.manhattan_distance(self.players[1], self.ball_target)
        else:
            player1_distance = player2_distance = 0
        return player2_distance - player1_distance

    def is_final_state(self):
        if self.ball_target is None:
            return False
        p1_distance = self.manhattan_distance(self.players[0], self.ball_target)
        p2_distance = self.manhattan_distance(self.players[1], self.ball_target)
        return p1_distance > self.calculate_max_move_distance(0, MAX_BALL_SPEED) and p2_distance > self.calculate_max_move_distance(1, MAX_BALL_SPEED)

    def minimax(self, depth, is_maximizing_player, ball_speed):
        if depth == 0 or self.is_final_state():
            return self.evaluate()

        player_index = 1 if is_maximizing_player else 0
        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(player_index, ball_speed):
                board_copy, players_copy, ball_copy, ball_target_copy, ball_speed_copy, ball_angle_copy, ball_steps_copy = self.get_state()
                self.move_player(player_index, move)
                eval = self.minimax(depth - 1, False, ball_speed)
                self.set_state(board_copy, players_copy, ball_copy, ball_target_copy, ball_speed_copy, ball_angle_copy, ball_steps_copy)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(player_index, ball_speed):
                board_copy, players_copy, ball_copy, ball_target_copy, ball_speed_copy, ball_angle_copy, ball_steps_copy = self.get_state()
                self.move_player(player_index, move)
                eval = self.minimax(depth - 1, True, ball_speed)
                self.set_state(board_copy, players_copy, ball_copy, ball_target_copy, ball_speed_copy, ball_angle_copy, ball_steps_copy)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_possible_moves(self, player_index, ball_speed):
        x, y = self.players[player_index]
        max_move_distance = self.calculate_max_move_distance(player_index, ball_speed)
        possible_moves = [(x + dx, y + dy) for dx in range(-max_move_distance, max_move_distance + 1) for dy in range(-max_move_distance, max_move_distance + 1)]
        possible_moves.append((x, y))  # 現在地に留まる動きも有効
        return [move for move in possible_moves if self.is_valid_move(move)]

    def best_move(self, player_index, depth=3):
        best_move = None
        best_throw = None
        best_val = float('-inf') if player_index == 1 else float('inf')
        for ball_speed in range(1, MAX_BALL_SPEED + 1):  # 速度をいくつかの値で試す
            for angle in range(30, 90, 10):  # 角度もいくつかの値で試す
                for move in self.get_possible_moves(player_index, ball_speed):
                    for dx in range(-ball_speed, ball_speed + 1):
                        for dy in range(-ball_speed, ball_speed + 1):
                            throw_pos = (move[0] + dx, move[1] + dy)
                            if self.is_valid_throw(move, throw_pos, ball_speed, angle):
                                board_copy, players_copy, ball_copy, ball_target_copy, ball_speed_copy, ball_angle_copy, ball_steps_copy = self.get_state()
                                self.move_player(player_index, move)
                                self.throw_ball(player_index, throw_pos, ball_speed, angle)
                                move_val = self.minimax(depth, player_index == 0, ball_speed)
                                self.set_state(board_copy, players_copy, ball_copy, ball_target_copy, ball_speed_copy, ball_angle_copy, ball_steps_copy)
                                if (player_index == 1 and move_val > best_val) or (player_index == 0 and move_val < best_val):
                                    best_val = move_val
                                    best_move = move
                                    best_throw = throw_pos
        return best_move, best_throw, ball_speed

    def update_ball_position(self):
        if self.ball_target is not None:
            x0, y0 = self.ball
            x1, y1 = self.ball_target
            if (x0, y0) == self.ball_target:
                self.ball_target = None
                return

            dx = x1 - x0
            dy = y1 - y0

            theta = math.radians(self.ball_angle)
            vx = self.ball_speed * math.cos(theta)
            vy = self.ball_speed * math.sin(theta)

            self.ball_steps += 1
            t = self.ball_steps / self.ball_speed
            new_y = y0 + vy * t - 0.5 * 9.8 * t ** 2
            new_x = x0 + vx * t

            if 0 <= new_y < BOARD_HEIGHT and 0 <= new_x < BOARD_WIDTH and self.board[int(new_y), int(new_x)] == EMPTY:
                self.board[int(new_y), int(new_x)] = BALL
                self.board[int(y0), int(x0)] = EMPTY
                self.ball = (int(new_y), int(new_x))

    def get_state(self):
        return self.board.copy(), self.players.copy(), self.ball, self.ball_target, self.ball_speed, self.ball_angle, self.ball_steps

    def set_state(self, board, players, ball, ball_target, ball_speed, ball_angle, ball_steps):
        self.board = board
        self.players = players
        self.ball = ball
        self.ball_target = ball_target
        self.ball_speed = ball_speed
        self.ball_angle = ball_angle
        self.ball_steps = ball_steps

def main():
    game = Game()
    turn = PLAYER1
    move_pos = None
    throw_pos = None
    ball_speed = 1  # 投げるスピードの初期値
    throw_angle = 45  # 投げる角度の初期値

    while True:
        game.update_ball_position()
        game.draw_board()

        if turn == PLAYER1:
            # ユーザーの入力待ち
            if move_pos is None:
                move_pos = tuple(map(int, input("Player 1: Enter move position (row col): ").split()))
                continue
            elif throw_pos is None:
                throw_pos = tuple(map(int, input("Player 1: Enter throw position (row col): ").split()))
                max_distance = game.calculate_max_move_distance(0, ball_speed)
                move_pos = game.get_reachable_position(game.players[0], move_pos, max_distance)
                game.move_player(0, move_pos)
                game.throw_ball(0, throw_pos, ball_speed, throw_angle)
                print("Player 1 threw the ball!")
                turn = PLAYER2
                move_pos = throw_pos = None
        elif turn == PLAYER2:
            move, throw, ball_speed = game.best_move(1)
            max_distance = game.calculate_max_move_distance(1, ball_speed)
            move = game.get_reachable_position(game.players[1], move, max_distance)
            game.move_player(1, move)
            game.throw_ball(1, throw, ball_speed, throw_angle)
            print("Player 2 threw the ball!")
            turn = PLAYER1

        if game.is_final_state():
            print(f"Player {1 if turn == PLAYER2 else 2} cannot catch the ball. Player {2 if turn == PLAYER2 else 1} wins!")
            break

        # User input for adjusting throw parameters
        print("Adjust throw: Use 'w' for up, 's' for down, 'a' for slower, 'd' for faster.")
        command = input("Command: ")
        if command == 'w':
            throw_angle = min(throw_angle + 1, 89)
        elif command == 's':
            throw_angle = max(throw_angle - 1, 1)
        elif command == 'a':
            ball_speed = max(ball_speed - 1, 1)
        elif command == 'd':
            ball_speed = min(ball_speed + 1, MAX_BALL_SPEED)

if __name__ == "__main__":
    main()