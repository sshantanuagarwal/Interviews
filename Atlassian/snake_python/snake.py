from coordinate import Coordinate

class Snake:
    def __init__(self, x, y, size):
        self.size = size
        self.current_position = [Coordinate(x - i, y) for i in range(size)]
        self.head = self.current_position[0]

    def get_head(self):
        return self.head

    def get_current_position(self):
        return self.current_position

    def set_current_position(self, new_position):
        self.current_position = new_position
        self.size = len(new_position)

    def set_head(self, new_head):
        self.head = new_head

    def is_valid_move(self, num_row, num_col, new_head):
        # Check boundaries
        if not (0 <= new_head.x < num_row and 0 <= new_head.y < num_col):
            return False
        # Check collision with itself
        if new_head in self.current_position:
            return False
        return True

    def __repr__(self):
        return f"Snake(current_position={self.current_position}, head={self.head}, size={self.size})" 