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
    
    
