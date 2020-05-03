solutions = 0


def check_valid(grid, row, col, num):
    # check Row
    for i in range(len(grid[row])):
        if num == grid[row][i]:
            return False

    # check column
    for i in range(len(grid)):
        if num == grid[i][col]:
            return False

    # check square
    x = divmod(row, 3)[0]
    y = divmod(col, 3)[0]
    for i in range(x * 3, x * 3 + 3):
        for j in range(y * 3, y * 3 + 3):
            if num == grid[i][j]:
                return False

    return True


def solve(grid):
    global solutions
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for n in range(1, 10):
                    if check_valid(grid, i, j, n):
                        grid[i][j] = n
                        solve(grid)
                        grid[i][j] = 0
                return
    solutions += 1
