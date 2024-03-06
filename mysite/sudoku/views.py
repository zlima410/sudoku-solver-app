from django.shortcuts import render

# Create your views here.

def solve_sudoku(board):
    # check if a number is valid in a cell
    def is_valid(row, col, num):
        # check the row and the column
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
            
        # check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True
    
    # find an empty cell in the board
    def find_empty_cell():
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None, None
    
    # solve the sudoku board using backtracking
    def solve():
        row, col = find_empty_cell()
        if row is None:
            return True # sudoku board is solved
        for num in range(1, 10):
            if is_valid(row, col, num):
                board[row][col] = num
                if solve(): # recursive funciton call
                    return True
                board[row][col] = 0 # backtrack
        return False    # no valid number was found
    
    # convert string representation of sudoku board to 2D array
    board = [[int(c) for c in row] for row in board.split("\n")]

    if solve():
        # convert back to string representation of sudoku board
        solved_board = "\n".join("".join(str(cell) for cell in row) for row in board)
        return solved_board
    else:
        return "No solution exists for the given Sudoku puzzle."