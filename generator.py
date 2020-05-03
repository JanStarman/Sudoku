from solver import solve
import random
import solution_counter


def random_sequence():
    arr = [x for x in range(1, 10)]
    random.shuffle(arr)
    return arr


def prepare_board():
    board = [[0 for x in range(9)] for y in range(9)]
    first_row = random_sequence()
    board[0] = first_row
    return board


def get_filled_board():
    sequence = random_sequence()
    board = prepare_board()
    solve(board, sequence)
    return board


def generate(difficulty):
    board = get_filled_board()
    i = 0
    while True:
        if i == difficulty:
            return board
        posX = random.randrange(0, 9)
        posY = random.randrange(0, 9)

        if board[posY][posX] == 0:
            continue

        current = board[posY][posX]
        board[posY][posX] = 0

        solution_counter.solutions = 0
        solution_counter.solve(board)
        solutions = solution_counter.solutions
        if solutions > 1:
            board[posY][posX] = current
            continue

        i += 1
