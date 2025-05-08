import pygame
import numpy as np
from pygame.locals import *

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
BALL = 3
NET = -1
MAX_BALL_SPEED = 3
CELL_SIZE = 30
WINDOW_WIDTH = 9 * CELL_SIZE
WINDOW_HEIGHT = 26 * CELL_SIZE
LINE_WIDTH = 1

class Game:
    def __init__(self, width=9, height=26):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=int)
        self.players = [(0, width // 2), (height - 1, width // 2)]  # プレイヤー1とプレイヤー2の初期位置
        self.ball = None
        self.board[self.players[0]] = PLAYER1
        self.board[self.players[1]] = PLAYER2
        for i in range(width):
            self.board[height // 2, i] = NET  # ネットの位置

    def draw_board(self, screen):
        screen.fill((255, 255, 255))  # 背景色を白に
        for y in range(self.height):
            for x in range(self.width):
                rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.board[y, x] == EMPTY:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                elif self.board[y, x] == NET:
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                elif self.board[y, x] == PLAYER1:
                    pygame.draw.rect(screen, (0, 0, 255), rect)
                elif self.board[y, x] == PLAYER2:
                    pygame.draw.rect(screen, (255, 0, 0), rect)
                elif self.board[y, x] == BALL:
                    pygame.draw.rect(screen, (0, 255, 0), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, LINE_WIDTH)

    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < self.height and 0 <= y < self.width and self.board[x, y] == EMPTY

    def move_player(self, player_index, new_pos):
        current_pos = self.players[player_index]
        if self.is_valid_move(new_pos):
            self.board[current_pos] = EMPTY
            self.players[player_index] = new_pos
            self.board[new_pos] = PLAYER1 if player_index == 0 else PLAYER2

    def throw_ball(self, player_index, target_pos):
        if self.is_valid_move(target_pos) and self.board[target_pos] != NET:
            self.ball = target_pos
            self.board[target_pos] = BALL

    def calculate_move_distance(self, player_index, ball_speed):
        other_player_index = 1 - player_index
        distance_to_other_player = self.manhattan_distance(self.players[player_index], self.players[other_player_index])
        return distance_to_other_player // ball_speed

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
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Minimax Game with Pygame')

    game = Game()
    clock = pygame.time.Clock()
    turn = PLAYER1

    while True:
        game.draw_board(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                grid_x, grid_y = y // CELL_SIZE, x // CELL_SIZE
                if turn == PLAYER1:
                    move_pos = (grid_x, grid_y)
                    if game.is_valid_move(move_pos):
                        print("Player 1 move selected:", move_pos)
                        game.move_player(0, move_pos)
                        turn = PLAYER2
                        game.draw_board(screen)
                        pygame.display.flip()
                        if game.is_final_state():
                            print("Player 2 cannot catch the ball. Player 1 wins!")
                            pygame.quit()
                            return
                elif turn == PLAYER2:
                    move, throw, ball_speed = game.best_move(1)
                    game.move_player(1, move)
                    game.throw_ball(1, throw)
                    turn = PLAYER1
                    game.draw_board(screen)
                    pygame.display.flip()
                    if game.is_final_state():
                        print("Player 1 cannot catch the ball. Player 2 wins!")
                        pygame.quit()
                        return

        clock.tick(30)

if __name__ == "__main__":
    main()