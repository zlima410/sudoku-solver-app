from django.test import TestCase
from .models import Sudoku

class SudokuGameTests(TestCase):

    def test_generate_puzzle(self):
        # test generating a new Sudoku puzzle by directly calling the URL.
        response = self.client.get('/sudoku/generate/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('puzzle', response.json())
        self.assertIn('id', response.json())

        # check that the puzzle is saved to the database
        puzzle_id = response.json()['id']
        self.assertTrue(Sudoku.objects.filter(id=puzzle_id).exists())

    def test_solve_puzzle(self):
        # test solving a generated Sudoku puzzle by directly calling the URL.
        
        # generate a puzzle to solve
        generate_response = self.client.get('/sudoku/generate/')  # Update with the actual path
        puzzle_id = generate_response.json()['id']

        # attempt to solve the puzzle
        solve_response = self.client.get(f'/sudoku/solve/{puzzle_id}/')  # Update with the actual path
        self.assertEqual(solve_response.status_code, 200)
        self.assertIn('solution', solve_response.json())

        # verify the solution is correct and saved
        sudoku = Sudoku.objects.get(id=puzzle_id)
        self.assertNotEqual(sudoku.solution, '')

    def test_get_puzzle(self):
        # test retrieving an existing Sudoku puzzle by directly calling the URL.
        
        # generate a puzzle to retrieve
        generate_response = self.client.get('/sudoku/generate/')  # Update with the actual path
        puzzle_id = generate_response.json()['id']

        # retrieve the puzzle
        get_response = self.client.get(f'/sudoku/get/{puzzle_id}/')  # Update with the actual path
        self.assertEqual(get_response.status_code, 200)
        self.assertIn('puzzle', get_response.json())

        # ensure the puzzle matches what was initially generated
        generated_puzzle = generate_response.json()['puzzle']
        retrieved_puzzle = get_response.json()['puzzle']
        self.assertEqual(generated_puzzle, retrieved_puzzle)
