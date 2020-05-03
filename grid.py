import pygame
from solver import solve
from cube import Cube
import generator


class Grid:
    selected = None
    solved_grid = None

    def __init__(self, rows, cols, width, height, difficulty):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.board = generator.generate(difficulty)
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
        self.model_cubes = [[self.cubes[i][j] for j in range(self.cols)] for i in range(self.rows)]

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def solve(self):
        self.solved_grid = solve(self.model)

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

    def check(self):
        if self.selected is None:
            return None

        row, col = self.selected
        val = self.cubes[row][col].value
        if val == 0:
            return None

        if val == self.solved_grid[row][col]:
            self.cubes[row][col].colour = True
            return True
        else:
            self.cubes[row][col].set(0)
            self.cubes[row][col].set_temp(0)
            self.update_model()
            return False

    def check_all(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].given is True:
                    continue
                val = self.cubes[i][j].value
                if val == 0:
                    continue

                if val == self.solved_grid[i][j]:
                    self.cubes[i][j].colour = True

                else:
                    self.cubes[i][j].colour = False
                    self.cubes[i][j].temp = self.cubes[i][j].value
                    self.cubes[i][j].set(0)
        self.update_model()

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
                self.cubes[i][j].colour = None

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].given is False:
            self.cubes[row][col].value = 0
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def is_correct(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value != self.solved_grid[i][j]:
                    return False
        return True

    def show_solved(self):
        self.cubes = \
            [[Cube(self.solved_grid[i][j], i, j, self.width, self.height) for j in range(self.cols)] for i in range(self.rows)]

    def hide_solved(self):
        self.cubes = [[self.model_cubes[i][j] for j in range(self.cols)] for i in range(self.rows)]
