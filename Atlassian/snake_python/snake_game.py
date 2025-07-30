from board import Board
from coordinate import Coordinate
from snake import Snake

class SnakeGame:
    def __init__(self, m, n, snake_size):
        self.board = Board(m, n)
        self.snake = Snake(m // 2, n // 2, snake_size)
        self.moves_count = 0
        self.game_over = False

    def is_game_over(self):
        return self.game_over

    def move_snake(self, direction):
        if self.game_over:
            print("Game is already over!")
            return
        delta = self.new_move_delta(direction)
        self.moves_count += 1
        new_head = self.snake.get_head().add(delta)
        if not self.snake.is_valid_move(self.board.get_num_row(), self.board.get_num_col(), new_head):
            self.game_over = True
            print("Invalid Move, Game over")
            return
        snake_new_position = [new_head]
        current_position = self.snake.get_current_position()
        if self.moves_count % 5 == 0:
            snake_new_position.extend(current_position)
        else:
            snake_new_position.extend(current_position[:-1])
        self.snake.set_current_position(snake_new_position)
        self.snake.set_head(new_head)
        print(self.snake)

    def new_move_delta(self, direction):
        if direction == "left":
            return Coordinate(-1, 0)
        elif direction == "right":
            return Coordinate(1, 0)
        elif direction == "up":
            return Coordinate(0, -1)
        elif direction == "down":
            return Coordinate(0, 1)
        else:
            raise ValueError("Incorrect direction")

if __name__ == "__main__":
    # Create a 10x10 board with initial snake size of 3
    game = SnakeGame(10, 10, 3)
    # Test sequence of moves
    moves = ["right", "right", "down", "down", "left", "up"]
    for move in moves:
        print(f"\nMoving {move}")
        game.move_snake(move)
        if game.is_game_over():
            break 