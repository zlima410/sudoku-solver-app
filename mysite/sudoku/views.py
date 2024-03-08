import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import Sudoku

# Create your views here.

def generate_puzzle(request):
    # generate a new random puzzle
    def generate_random_puzzle():
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side
        
        def shuffle(s):
            return random.sample(s, len(s))
        
        row_base = range(base)
        rows = [g * base + r for g in shuffle(row_base) for r in shuffle(row_base)]
        cols = [g * base + c for g in shuffle(row_base) for c in shuffle(row_base)]
        nums = shuffle(range(1, base * base + 1))

        # create board using randomized baseline pattern
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = squares * 3 // 4
        for p in random.sample(range(squares), empties):
            board[p // side][p % side] = 0

        return board
    
    # generate a new puzzle
    puzzle = generate_random_puzzle()

    # convert the puzzle to a string
    puzzle_str = ''.join([str(num) for row in puzzle for num in row])

    # save the puzzle to the database
    sudoku = Sudoku.objects.create(puzzle=puzzle_str, solution='')  # no solution present

    # return the puzzle as a JSON response
    return JsonResponse({'status': 'success', 'message': 'Puzzle generated successfully', 'puzzle': puzzle_str})

def solve_puzzle(request, puzzle_id):
    # get the puzzle from the database using the puzzle_id
    try:
        sudoku = Sudoku.objects.get(id=puzzle_id)
    except Sudoku.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Puzzle not found'})
    
    # copy the puzzle to a new object
    puzzle = list(sudoku.puzzle)

    # solve the puzzle using backtracking algorithm
    def is_valid(row, col, num):
        # check if the number is already in the row
        for i in range(9):
            if puzzle.puzzle[row * 9 + i] == str(num):
                return False
        # check if the number is already in the column
        for i in range(9):
            if puzzle.puzzle[i * 9 + col] == str(num):
                return False
        # check if the number is in the 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if puzzle.puzzle[(start_row + i) * 9 + start_col + j] == str(num):
                    return False
        return True
    
    def solve():
        for i in range(81):
            row, col = i // 9, i % 9
            if puzzle.puzzle[i] == '0':
                for num in range(1, 10):
                    if is_valid(row, col, num):
                        puzzle[i] = str(num)
                        if solve():
                            return True
                        puzzle[i] = '0'
                return False
        return True
    
    # solve the puzzle
    if solve():
        # puzzle was solved successfully
        sudoku.solution = ''.join(puzzle)
        sudoku.save()
        return JsonResponse({'status': 'success', 'message': 'Puzzle solved successfully', 'solution': sudoku.solution})
    else:
        # puzzle cannot be solved
        return JsonResponse({'status': 'error', 'message': 'Puzzle cannot be solved'})
    
def get_puzzle(request, puzzle_id):
    try:
        sudoku = Sudoku.objects.get(id=puzzle_id)
        return JsonResponse({'status': 'success', 'message': 'Puzzle retrieved successfully', 'puzzle': sudoku.puzzle})
    except Sudoku.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Puzzle not found'})