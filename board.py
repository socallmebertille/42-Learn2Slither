import random

import numpy as np


class Board:
    DIRECTIONS = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1),
    }

    def __init__(self):
        self.size = 10
        self.snake = []
        self.green_apples = []
        self.red_apple = None
        self._place_items()
        self._spawn_snake()
        self._place_items()
        for _ in range(2):
            self.green_apples.append(self._spawn_apple())
            self._place_items()
        self.red_apple = self._spawn_apple()
        self._place_items()

    def _free_cells(self):
        """Return the list of free cells, as tuples."""
        return [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i, j] == '0'
        ]

    def _neighbors(self, cell):
        """Return the 4 adjacent cells that are inside the board."""
        i, j = cell
        candidates = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [
            (a, b)
            for a, b in candidates
            if 0 <= a < self.size and 0 <= b < self.size
        ]

    def _spawn_snake(self):
        """Place the head, then grow the body cell by cell."""
        self.snake = [random.choice(self._free_cells())]
        while len(self.snake) < 3:
            candidates = [
                cell
                # -1 : last element of the list
                for cell in self._neighbors(self.snake[-1])
                if cell not in self.snake
            ]
            self.snake.append(random.choice(candidates))

    def _spawn_apple(self):
        """Return a random free cell, or None if the board is full."""
        free_cells = self._free_cells()
        return random.choice(free_cells) if free_cells else None

    def _place_items(self):
        """Redraw the board from the snake and apple positions."""
        self.board = np.full((self.size, self.size), '0')
        for i, pos in enumerate(self.snake):
            if i == 0:
                self.board[pos] = 'H'  # Head of the snake
            else:
                self.board[pos] = 'S'
        for pos in self.green_apples:
            if pos is not None:
                self.board[pos] = 'G'
        if self.red_apple is not None:
            self.board[self.red_apple] = 'R'

    def display(self):
        for row in self.board:
            print(' '.join(row))

    def move(self, direction):
        """Move the snake one cell. Return what happened."""
        di, dj = self.DIRECTIONS[direction]
        i, j = self.snake[0]
        position = (i + di, j + dj)
        if not (0 <= position[0] < self.size and 0 <= position[1] < self.size):
            return 'WALL'
        self.snake.pop()
        if position in self.snake:
            return 'SELF'
        self.snake.insert(0, position)
        self._place_items()
        return 'MOVE'


if __name__ == "__main__":
    keys = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}
    board = Board()
    while True:
        board.display()
        try:
            key = input("Direction (w/a/s/d) : ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye")
            break
        if key not in keys:
            print("Invalid key. Use w/a/s/d for up/left/down/right.")
            continue
        event = board.move(keys[key])
        print(event)
        if event != 'MOVE':
            print("Game over")
            break
