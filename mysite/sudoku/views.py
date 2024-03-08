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