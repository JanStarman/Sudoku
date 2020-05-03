def find_empty(bo):
    for i in range(len(bo[0])):
        for j in range(len(bo)):
            if bo[i][j] == 0:
                return i, j  # row, col
    return None


def check_valid(bo, row, col, num):
    # check Row
    for i in range(len(bo[row])):
        if num == bo[row][i] and col != i:
            return False

    # check column
    for i in range(len(bo)):
        if num == bo[i][col] and row != i:
            return False

    # check square
    x = divmod(row, 3)[0]
    y = divmod(col, 3)[0]
    for i in range(x * 3, x * 3 + 3):
        for j in range(y * 3, y * 3 + 3):
            if num == bo[i][j] and (i, j) != (row, col):
                return False

    return True


def solve(bo, sequence=None):
    if sequence is None:
        sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    empty = find_empty(bo)
    if empty is None:
        return bo

    row, col = empty
    for i in sequence:
        if check_valid(bo, row, col, i):
            bo[row][col] = i

            if solve(bo, sequence):
                return bo

            bo[row][col] = 0

    return False
